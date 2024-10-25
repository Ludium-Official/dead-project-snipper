import requests
from playwright.sync_api import sync_playwright


def close_browser(playwright, browser):
    """Closes the browser and Playwright."""
    browser.close()
    playwright.stop()

def intercept_request(user_name, browser, page=None):

    # page
    if page is None:
        page = browser.new_page()

    # to define the request URL and headers in the scope of the function
    request_url = None 
    request_headers = None

    # Handle request interception
    def handle_route(route):

        nonlocal request_url, request_headers
        
        request = route.request
        if "graphql" in request.url and 'UserByScreenName' in request.url:  # Looking for GraphQL calls
            # pprint(f"Intercepted GraphQL URL: {request.url}")
            # pprint(f"Header of the Intercepted URL : {request.headers}")
            request_url = request.url
            request_headers = request.headers
            
        route.continue_()

    page.route("**/*", handle_route)

    # Adjust timeout and wait for a specific element or event instead of full load
    page.set_default_timeout(60000)  # Set timeout to 60 seconds
    try:
        page.goto(f"https://x.com/{user_name}", wait_until="networkidle")  # Wait until network is idle
        print("Page loaded successfully!")
    except Exception as e:
        print(f"Navigation error: {e}")

    # Give time for requests to appear
    page.wait_for_timeout(20000)  # Wait for 15 seconds to intercept GraphQL requests

    return request_url, request_headers

def getUserProfile(url, header):
    response = requests.get(url, headers=header)
    response = response.json()

    return response['data']
