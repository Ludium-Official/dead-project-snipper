import time
import random
import bs4
import json
from datetime import datetime
from datetime import timedelta
from pprint import pprint   
from playwright.sync_api import sync_playwright

def random_sleep(min_time=1, max_time=3):
    """Sleep for a random period between min_time and max_time seconds."""
    sleep_time = random.uniform(min_time, max_time)
    time.sleep(sleep_time)

def save_cookies(context):
    import os
    # Save cookies to a JSON file
    cookies = context.cookies()
    json_file_path = os.path.join(os.path.dirname(__file__), 'config', 'cookies.json')
    with open(json_file_path, "w") as f:
        json.dump(cookies, f)
    print("Cookies saved!")

def load_cookies(context):
    import os

    json_file_path = os.path.join(os.path.dirname(__file__), 'config', 'cookies.json')
    with open(json_file_path, "r") as f:
        cookies = json.load(f)

        # Correct the 'sameSite' value for each cookie
        for cookie in cookies:
            if cookie.get('sameSite') not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'None'  # Set to a valid value like 'None'

        # Add corrected cookies to the browser context
        context.add_cookies(cookies)

def check_cookies():
    import os

    json_file_path = os.path.join(os.path.dirname(__file__), 'config', 'cookies.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            is_valid_cookies = json.load(f)
            today = datetime.now()
            for cookie in is_valid_cookies:
                
                expires = cookie.get('expirationDate')
                if expires is not None:
                    valid_date =  datetime.utcfromtimestamp(expires)
                    if valid_date < today - timedelta(days=2):
                        return False
        return True
    else:
        return False

def  launch_browser():
    # Launch the browser (headless or headful based on your preference)
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)  # Set to True if you want headless mode
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        viewport={'width': 1280, 'height': 720},
        locale="ko-KR"  # Set the locale to Korean (Korea)
    )
    

    return browser, context

def close_browser(browser):
    browser.close()

def login_x(username, password, useremail):
    '''
    parameters
    ----------
    username: str
        The XHandle used for logging into X.

    password: str
        The password for the XHandle.

    handle: str

    returns
    -------
    Browser and Page objects

    '''

    # Launch the browser
    browser, context = launch_browser()

    if check_cookies():
        # Load cookies if they exist
        load_cookies(context)
        page = context.new_page()
        page.goto("https://x.com/home")
        print("Already logged in using cookies!")
        return browser, page
    else:
        page = context.new_page()

        # Go to the X (Twitter) homepage
        page.goto("https://x.com")
        random_sleep(2, 4)

        # Step 1: Click on the login button
        login_button_selector = 'a[data-testid="loginButton"]'
        page.click(login_button_selector)
        random_sleep(2, 4)

        # Step 2: Wait for navigation to the login page
        page.wait_for_url("https://x.com/i/flow/login")
        random_sleep(1, 3)

        # Step 3: Enter the username (X ID)
        username_input_selector = 'input[name="text"]'
        page.fill(username_input_selector, username)
        random_sleep(1, 2)

        # Step 4: Click the 'Next' or '다음' button
        next_button_selector = 'span:has-text("다음")'
        page.click(next_button_selector)
        random_sleep(2, 4)

        # step 4.1 : check the input field for the user-email
        if page.query_selector('input[name="text"]') is not None:
            # step 5: fill user-email info
            user_email_selector = 'input[name="text"]'
            page.fill(user_email_selector, useremail)
            random_sleep(1, 2)

            page.click(next_button_selector)
            random_sleep(2, 4)

        # Step 6: Wait for the password input field to be visible
        password_input_selector = 'input[name="password"]'
        page.wait_for_selector(password_input_selector)
        page.fill(password_input_selector, password)
        random_sleep(1, 2)

        # Step 7: Click the '로그인하기' button to submit
        login_button_selector = 'span:has-text("로그인하기")'
        page.click(login_button_selector)
        random_sleep(2, 4)

        # Optional: Wait for login completion and user profile or home page to load
        page.wait_for_url("https://x.com/home")
        print("Login successful!")

        # Save cookies after login
        save_cookies(context)

    return browser, page