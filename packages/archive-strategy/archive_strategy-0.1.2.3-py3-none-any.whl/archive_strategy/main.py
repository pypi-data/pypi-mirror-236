import os
import ast
from archive_strategy.archiver import Archiver


BASE_DIR = os.environ.get("ARCHIVE_BASE_DIR", "/backups")
ARCHIVE_DIR = os.environ.get("ARCHIVE_DIR", "/archives")
ARCHIVE_USER = os.environ.get("ARCHIVE_USER", "root")
ARCHIVE_GROUP = os.environ.get("ARCHIVE_GROUP", "root")
TEST_MODE = ast.literal_eval(os.environ.get("ARCHIVE_TEST_MODE", "True"))
DELETE = ast.literal_eval(os.environ.get("ARCHIVE_DELETE", "False"))


def main():
    archiver = Archiver(
        archive_dir=ARCHIVE_DIR,
        base_dir=BASE_DIR,
        archive_user=ARCHIVE_USER,
        archive_group=ARCHIVE_GROUP,
        test_mode=TEST_MODE,
        delete=DELETE,
    )
    archiver.show_info()
    archiver.archive()
    # archiver.organise()
