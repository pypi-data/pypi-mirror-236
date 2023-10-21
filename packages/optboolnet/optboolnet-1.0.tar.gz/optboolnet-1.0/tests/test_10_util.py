import os
import shutil
import zipfile
from optboolnet.util import compress_project

_FPATH = os.path.dirname(__file__)
_BASE_PATH = "src/optboolnet"


def test_compress_project():
    compress_project(_BASE_PATH, _FPATH)
    assert os.path.isfile(f"{_FPATH}/project.zip")
    os.remove(f"{_FPATH}/project.zip")


if __name__ == "__main__":
    test_compress_project()
