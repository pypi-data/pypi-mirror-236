from archive_strategy.archiver import Archiver

BASE_DIR = "/backups"
ARCHIVE_DIR = "/archives"
ARCHIVE_USER = "root"
ARCHIVE_GROUP = "root"
TEST_MODE = False
DELETE = False


def main():
    archiver = Archiver(
        archive_dir=ARCHIVE_DIR,
        base_dir=BASE_DIR,
        archive_user=ARCHIVE_USER,
        archive_group=ARCHIVE_GROUP,
        test_mode=TEST_MODE,
        delete=DELETE,
    )
    archiver.archive()
    archiver.organise()
