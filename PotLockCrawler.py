import bs4
from playwright.sync_api import sync_playwright

# crawl the potlock website
def launch_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    return playwright, browser

def close_browser(playwright, browser):
    """Closes the browser and Playwright."""
    browser.close()
    playwright.stop()

def get_page_content(url, browser):
    """Fetches the HTML content of the page."""
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)  # Wait for 5 seconds or adjust as necessary
    html = page.content()
    return html

# get soup
def get_soup(html):
    """Parses the HTML and returns a BeautifulSoup object."""
    return bs4.BeautifulSoup(html, 'html.parser')

def get_github_link(soup):
    """Parses the HTML and finds a GitHub link."""
    github_link = soup.find('a', href=lambda href: href and "github.com" in href)
    return github_link['href'] if github_link else None

# get twitter link
def get_twitter_link(soup):
    twitter_link = soup.find('a', href=lambda href: href and "twitter.com" in href)
    return twitter_link['href'] if twitter_link else None

# get members
def get_members(soup):
    members = soup.find_all('a', href=lambda href:href and "profile&accountId" in href)
    return [member['href'] for member in members]

