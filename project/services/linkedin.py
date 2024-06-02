import time
import re
import os
import pickle

from flask import abort
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Path to store cookies
COOKIES_PATH = "linkedin_cookies.pkl"


def initialize_driver(browser):
    """Initializes the webdriver with headless options."""

    if browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Edge(options=options)
    elif browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Firefox(options=options)
    else:
        abort(500, "Unsupported browser!")

    return driver


def save_cookies(driver, path):
    """Saves cookies to a file."""

    with open(path, "wb") as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookies(driver, path):
    """Loads cookies from a file."""
    with open(path, "rb") as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def linkedin_login(driver, email, password):
    """Logs into LinkedIn and saves cookies."""

    driver.get("https://www.linkedin.com/login")
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    #
    time.sleep(20)

    save_cookies(driver, COOKIES_PATH)
    return driver


def linkedin_login_with_cookies(driver):
    """Logs into LinkedIn using saved cookies."""

    driver.get("https://www.linkedin.com")
    load_cookies(driver, COOKIES_PATH)
    driver.refresh()
    time.sleep(5)
    return driver


def scroll_to_bottom(driver, target_posts):
    """Scrolls to the bottom of the page to load all posts."""

    last_height = driver.execute_script("return document.body.scrollHeight")
    posts_loaded = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        posts = driver.find_elements(By.XPATH, "//div[@data-urn]")
        posts_loaded = len(posts)
        if posts_loaded >= target_posts or new_height == last_height:
            break
        last_height = new_height


def extract_likers_data(driver, post_id):
    """Extracts the likers data for a given post."""

    try:
        likers_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@data-urn='{post_id}']//button[contains(@class, 't-black--light') and contains(@class, 'display-flex') and contains(@class, 'align-items-center') and contains(@class, 'social-details-social-counts__count-value-hover')]",
                )
            )
        )

        driver.execute_script("arguments[0].click();", likers_button)
        time.sleep(3)

        likers_soup = BeautifulSoup(driver.page_source, "html.parser")
        likers = likers_soup.select("li.social-details-reactors-tab-body-list-item")

        likers_data = []
        for liker in likers:
            name_tag = liker.select_one(
                ".artdeco-entity-lockup__title span[aria-hidden='true']"
            )
            name = name_tag.get_text(strip=True) if name_tag else "Unknown"
            profile_link = liker.select_one("a")["href"]
            liker_id = re.search(r"/in/([^/]+)", profile_link).group(1)
            title_tag = liker.select_one(".artdeco-entity-lockup__caption")
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            likers_data.append({"id": liker_id, "name": name, "title": title})

        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-test-modal-close-btn]")
            )
        )
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)

        return likers_data
    except Exception as e:
        print(f"Could not process post {post_id}: {e}")
        return []


def get_linkedin_activity_data(driver, linkedin_user_id, posts_limit=30):
    """Retrieves the recent activity data for the given LinkedIn user."""

    try:
        driver.get(
            f"https://www.linkedin.com/in/{linkedin_user_id}/recent-activity/all/"
        )
        scroll_to_bottom(driver, posts_limit)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        posts = soup.find_all("div", {"data-urn": True})

        activity_data = []
        for post in posts[:posts_limit]:
            post_id = post["data-urn"]
            likers_data = extract_likers_data(driver, post_id)
            activity_data.append({"post_id": post_id, "likers": likers_data})
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return activity_data
