import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ["true", "yes", "on", "1"]
    return False


class Config:

    # CORS
    USE_CORS = as_bool(os.getenv("USE_CORS") or "yes")
    CORS_SUPPORTS_CREDENTIALS = True

    # API documentation
    APIFAIRY_TITLE = "Social Data Scraping API"
    APIFAIRY_VERSION = "1.0"
    APIFAIRY_UI = os.getenv("DOCS_UI", "elements")
    APIFAIRY_TAGS = ["linkedin"]

    # LinkedIn credentials
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")
