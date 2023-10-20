import os
import pathlib
import pickle
import sys
import warnings
from urllib.parse import SplitResult

import pytest

from upath import UPath
from upath.implementations.cloud import GCSPath
from upath.implementations.cloud import S3Path

from .cases import BaseTests
from .utils import only_on_windows
from .utils import skip_on_windows


@skip_on_windows
def test_posix_path(local_testdir):
    assert isinstance(UPath(local_testdir), pathlib.PosixPath)


@only_on_windows
def test_windows_path(local_testdir):
    assert isinstance(UPath(local_testdir), pathlib.WindowsPath)


def test_UPath_untested_protocol_warning():
    with warnings.catch_warnings(record=True) as w:
        _ = UPath("mock:/")
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "mock" in str(w[-1].message)


def test_UPath_file_protocol_no_warning():
    with warnings.catch_warnings(record=True) as w:
        _ = UPath("file:/")
        assert len(w) == 0


class TestUpath(BaseTests):
    @pytest.fixture(autouse=True)
    def path(self, local_testdir):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # On Windows the path needs to be prefixed with `/`, because
            # `UPath` implements `_posix_flavour`, which requires a `/` root
            # in order to correctly deserialize pickled objects
            root = "/" if sys.platform.startswith("win") else ""
            self.path = UPath(f"mock:{root}{local_testdir}")

    def test_fsspec_compat(self):
        pass

    def test_cwd(self):
        pth = type(self.path).cwd()
        assert str(pth) == os.getcwd()
        assert isinstance(pth, pathlib.Path)
        assert isinstance(pth, UPath)

    def test_home(self):
        pth = type(self.path).home()
        assert str(pth) == os.path.expanduser("~")
        assert isinstance(pth, pathlib.Path)
        assert isinstance(pth, UPath)


def test_multiple_backend_paths(local_testdir):
    path = f"s3:{local_testdir}"
    s3_path = UPath(path, anon=True)
    assert s3_path.joinpath("text.txt")._url.scheme == "s3"
    path = f"file://{local_testdir}"
    UPath(path)
    assert s3_path.joinpath("text1.txt")._url.scheme == "s3"


def test_constructor_accept_path(local_testdir):
    path = UPath(pathlib.Path(local_testdir))
    assert str(path) == str(pathlib.Path(local_testdir))


def test_constructor_accept_upath(local_testdir):
    path = UPath(UPath(local_testdir))
    assert str(path) == str(pathlib.Path(local_testdir))


def test_subclass(local_testdir):
    class MyPath(UPath):
        pass

    path = MyPath(local_testdir)
    assert str(path) == str(pathlib.Path(local_testdir))
    assert issubclass(MyPath, UPath)
    assert isinstance(path, pathlib.Path)


def test_subclass_with_gcs():
    path = UPath("gcs://bucket", anon=True)
    assert isinstance(path, UPath)
    assert isinstance(path, pathlib.Path)


def test_instance_check(local_testdir):
    upath = UPath(local_testdir)
    # test instance check passes
    assert isinstance(upath, pathlib.Path)
    assert isinstance(upath, UPath)


def test_instance_check_local_uri(local_testdir):
    upath = UPath(f"file://{local_testdir}")
    assert isinstance(upath, pathlib.Path)
    assert isinstance(upath, UPath)


def test_new_method(local_testdir):
    path = UPath.__new__(pathlib.Path, local_testdir)
    assert str(path) == str(pathlib.Path(local_testdir))
    assert isinstance(path, pathlib.Path)
    assert isinstance(path, UPath)


PATHS = (
    ("path", "storage_options", "module", "object_type"),
    (
        ("/tmp/abc", {}, None, pathlib.Path),
        ("s3://bucket/folder", {"anon": True}, "s3fs", S3Path),
        ("gs://bucket/folder", {"token": "anon"}, "gcsfs", GCSPath),
    ),
)


@pytest.mark.parametrize(*PATHS)
def test_create_from_type(path, storage_options, module, object_type):
    """Test that derived paths use same fs instance."""
    if module:
        # skip if module cannot be imported
        pytest.importorskip(module)
    try:
        upath = UPath(path, **storage_options)
        # test expected object type
        assert isinstance(upath, object_type)
        cast = type(upath)
        parent = upath.parent
        # test derived object is same type
        assert isinstance(parent, cast)
        # test that created fs uses fsspec instance cache
        assert not hasattr(upath, "fs") or upath.fs is parent.fs
        new = cast(str(parent), **storage_options)
        # test that object cast is same type
        assert isinstance(new, cast)
    except ImportError:
        # fs failed to import
        pass


def test_list_args():
    path_a = UPath("gcs://bucket", "folder")
    path_b = UPath("gcs://bucket") / "folder"

    assert str(path_a) == str(path_b)
    assert path_a._root == path_b._root
    assert path_a._drv == path_b._drv
    assert path_a._parts == path_b._parts
    assert path_a._url == path_b._url


def test_child_path():
    path_a = UPath("gcs://bucket/folder")
    path_b = UPath("gcs://bucket") / "folder"

    assert str(path_a) == str(path_b)
    assert path_a._root == path_b._root
    assert path_a._drv == path_b._drv
    assert path_a._parts == path_b._parts
    assert path_a._url == path_b._url


def test_pickling():
    path = UPath("gcs://bucket/folder", token="anon")
    pickled_path = pickle.dumps(path)
    recovered_path = pickle.loads(pickled_path)

    assert type(path) == type(recovered_path)
    assert str(path) == str(recovered_path)
    assert path.storage_options == recovered_path.storage_options


def test_pickling_child_path():
    path = UPath("gcs://bucket", token="anon") / "subfolder" / "subsubfolder"
    pickled_path = pickle.dumps(path)
    recovered_path = pickle.loads(pickled_path)

    assert type(path) == type(recovered_path)
    assert str(path) == str(recovered_path)
    assert path._drv == recovered_path._drv
    assert path._root == recovered_path._root
    assert path._parts == recovered_path._parts
    assert path.storage_options == recovered_path.storage_options


def test_copy_path():
    path = UPath("gcs://bucket/folder", token="anon")
    copy_path = UPath(path)

    assert type(path) == type(copy_path)
    assert str(path) == str(copy_path)
    assert path._drv == copy_path._drv
    assert path._root == copy_path._root
    assert path._parts == copy_path._parts
    assert path.storage_options == copy_path.storage_options


def test_copy_path_posix():
    path = UPath("/tmp/folder")
    copy_path = UPath(path)

    assert type(path) == type(copy_path)
    assert str(path) == str(copy_path)
    assert path._drv == copy_path._drv
    assert path._root == copy_path._root
    assert path._parts == copy_path._parts


def test_copy_path_append():
    path = UPath("/tmp/folder")
    copy_path = UPath(path, "folder2")

    assert type(path) == type(copy_path)
    assert str(path / "folder2") == str(copy_path)

    path = UPath("/tmp/folder")
    copy_path = UPath(path, "folder2/folder3")

    assert str(path / "folder2" / "folder3") == str(copy_path)

    path = UPath("/tmp/folder")
    copy_path = UPath(path, "folder2", "folder3")

    assert str(path / "folder2" / "folder3") == str(copy_path)


@pytest.mark.parametrize(
    "urlpath",
    [
        os.getcwd(),
        pathlib.Path.cwd().as_uri(),
        "mock:///abc",
    ],
)
def test_access_to_private_kwargs_and_url(urlpath):
    # fixme: this should be deprecated...
    pth = UPath(urlpath)
    assert isinstance(pth._kwargs, dict)
    assert pth._kwargs == {}
    assert isinstance(pth._url, SplitResult)
    assert pth._url.scheme == "" or pth._url.scheme in pth.fs.protocol
    assert pth._url.path == pth.path
    subpth = pth / "foo"
    assert subpth._kwargs == {}
    assert isinstance(subpth._url, SplitResult)
    assert subpth._url.scheme == "" or subpth._url.scheme in subpth.fs.protocol
    assert subpth._url.path == subpth.path


def test_copy_path_append_kwargs():
    path = UPath("gcs://bucket/folder", anon=True)
    copy_path = UPath(path, anon=False)

    assert type(path) == type(copy_path)
    assert str(path) == str(copy_path)
    assert not copy_path._kwargs["anon"]
    assert path._kwargs["anon"]


def test_relative_to():
    assert "s3://test_bucket/file.txt" == str(
        UPath("s3://test_bucket/file.txt").relative_to(UPath("s3://test_bucket"))
    )

    with pytest.raises(ValueError):
        UPath("s3://test_bucket/file.txt").relative_to(UPath("gcs://test_bucket"))

    with pytest.raises(ValueError):
        UPath("s3://test_bucket/file.txt", anon=True).relative_to(
            UPath("s3://test_bucket", anon=False)
        )


def test_uri_parsing():
    assert (
        str(UPath("http://www.example.com//a//b/")) == "http://www.example.com//a//b/"
    )


NORMALIZATIONS = (
    ("unnormalized", "normalized"),
    (
        # Expected normalization results according to curl
        ("http://example.com", "http://example.com/"),
        ("http://example.com/", "http://example.com/"),
        ("http://example.com/a", "http://example.com/a"),
        ("http://example.com//a", "http://example.com//a"),
        ("http://example.com///a", "http://example.com///a"),
        ("http://example.com////a", "http://example.com////a"),
        ("http://example.com/a/.", "http://example.com/a/"),
        ("http://example.com/a/./", "http://example.com/a/"),
        ("http://example.com/a/./b", "http://example.com/a/b"),
        ("http://example.com/a/.//", "http://example.com/a//"),
        ("http://example.com/a/.//b", "http://example.com/a//b"),
        ("http://example.com/a//.", "http://example.com/a//"),
        ("http://example.com/a//./", "http://example.com/a//"),
        ("http://example.com/a//./b", "http://example.com/a//b"),
        ("http://example.com/a//.//", "http://example.com/a///"),
        ("http://example.com/a//.//b", "http://example.com/a///b"),
        ("http://example.com/a/..", "http://example.com/"),
        ("http://example.com/a/../", "http://example.com/"),
        ("http://example.com/a/../.", "http://example.com/"),
        ("http://example.com/a/../..", "http://example.com/"),
        ("http://example.com/a/../../", "http://example.com/"),
        ("http://example.com/a/../..//", "http://example.com//"),
        ("http://example.com/a/..//", "http://example.com//"),
        ("http://example.com/a/..//.", "http://example.com//"),
        ("http://example.com/a/..//..", "http://example.com/"),
        ("http://example.com/a/../b", "http://example.com/b"),
        ("http://example.com/a/..//b", "http://example.com//b"),
        ("http://example.com/a//..", "http://example.com/a/"),
        ("http://example.com/a//../", "http://example.com/a/"),
        ("http://example.com/a//../.", "http://example.com/a/"),
        ("http://example.com/a//../..", "http://example.com/"),
        ("http://example.com/a//../../", "http://example.com/"),
        ("http://example.com/a//../..//", "http://example.com//"),
        ("http://example.com/a//..//..", "http://example.com/a/"),
        ("http://example.com/a//../b", "http://example.com/a/b"),
        ("http://example.com/a//..//", "http://example.com/a//"),
        ("http://example.com/a//..//.", "http://example.com/a//"),
        ("http://example.com/a//..//b", "http://example.com/a//b"),
        # Normalization with and without an authority component
        ("memory:/a/b/..", "memory:/a/"),
        ("memory:/a/b/../..", "memory:/"),
        ("memory:/a/b/../../..", "memory:/"),
        ("memory://a/b/..", "memory://a/"),
        ("memory://a/b/../..", "memory://a/"),
        ("memory://a/b/../../..", "memory://a/"),
    ),
)


@pytest.mark.parametrize(*NORMALIZATIONS)
def test_normalize(unnormalized, normalized):
    expected = str(UPath(normalized))
    # Normalise only, do not attempt to follow redirects for http:// paths here
    result = str(UPath.resolve(UPath(unnormalized)))
    assert expected == result
