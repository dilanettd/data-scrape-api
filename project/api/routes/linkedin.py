import json
import os

from apifairy import response
from flask import Blueprint, abort, current_app
from project.schemas.linkedin import PostSchema
from project.services.linkedin import (
    get_linkedin_activity_data,
    initialize_driver,
    linkedin_login,
    linkedin_login_with_cookies,
)
from config import Config as settings


linkedin = Blueprint("linkedin", __name__)
COOKIES_PATH = "linkedin_cookies.pkl"


@linkedin.route("/activity/<linkedin_user_id>", methods=["GET"])
@response(PostSchema(many=True))
def get_activity(linkedin_user_id):
    """
    Scrape recent activity (latest 20-30 posts) of a LinkedIn user by their
    LinkedIn ID and fetch the engagement data (likers) of each post,
    including their IDs, names, and titles.
    """

    email = settings.LINKEDIN_EMAIL
    password = settings.LINKEDIN_PASSWORD
    browser = settings.BROWSER

    if not email or not password:
        abort(400, "LinkedIn email or password is not set in the configuration.")

    driver = initialize_driver(browser)

    # Check if cookies exist and login using cookies if possible
    try:
        if os.path.exists(COOKIES_PATH):
            driver = linkedin_login_with_cookies(driver)
            print("Logged in with cookies.")
        else:
            driver = linkedin_login(driver, email, password)
            print("Logged in and saved cookies.")
    except Exception as e:
        abort(500, f"An error occurred while logging in: {e}")

    try:
        data = get_linkedin_activity_data(driver, linkedin_user_id)
    except Exception as e:
        abort(500, f"An error occurred while scraping data: {e}")
    finally:
        driver.quit()

    return data
