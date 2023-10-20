from archive_strategy.archiver import Archiver

BASE_DIR = "/Users/pieterpaulussen/Desktop/backup_test"
ARCHIVE_DIR = "/Users/pieterpaulussen/Desktop/archive"
ARCHIVE_USER = "pieterpaulussen"
ARCHIVE_GROUP = "staff"
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
