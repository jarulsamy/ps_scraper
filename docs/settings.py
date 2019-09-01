import os

REPO_NAME = "ps_scraper"
DEBUG = True
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def parent_dir(path):
    """ Return parent of a directory """
    return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)

FREEZER_DESTINATION = PROJECT_ROOT
FREEZER_BASE_URL = f"http://localhost/{REPO_NAME}"

FREEZER_REMOVE_EXTRA_FILES = False

FLATPAGES_MARDOWN_EXTENSIONS = ["codehilite"]
FLATPAGES_ROOT = os.path.join(APP_DIR, "pages")
FLATPAGES_EXTENSION = ".md"
