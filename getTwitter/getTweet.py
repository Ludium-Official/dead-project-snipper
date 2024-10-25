import bs4
from playwright.sync_api import sync_playwright
from pprint import pprint

def launch_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    return playwright, browser

def close_browser(playwright, browser):
    """Closes the browser and Playwright."""
    browser.close()
    playwright.stop()

def scroll_and_crawl(handle, browser, page=None, max_scrolls=10, crawl_interval=2):
    url = f"https://x.com/{handle}"
    """Scrolls a bit and crawls data at each step, removing duplicates."""
    if page is None:
        page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the page loads

    all_tweets = []
    seen_tweets = set()  # Track seen tweet text to avoid duplicates

    for scroll_count in range(max_scrolls):
        # Scroll down a bit
        scroll_script = """
            window.scrollBy(0, 500);  // Scroll down by 500 pixels
        """
        page.evaluate(scroll_script)

        # Wait for content to load
        page.wait_for_timeout(crawl_interval * 1000)  # Wait for crawl_interval seconds
        
        # Get page content and parse it
        html = page.content()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        # Crawl the tweets
        new_tweets = get_tweet(soup)

        # Add new tweets, skipping duplicates
        for tweet in new_tweets:
            tweet_text = tweet['text']
            
            if tweet_text not in seen_tweets:
                all_tweets.append(tweet)
                seen_tweets.add(tweet_text)  # Add to set to track duplicates

        # print(f"Scroll {scroll_count + 1}/{max_scrolls}: Collected {len(new_tweets)} new tweets.")
    
    return all_tweets

# get soup
def get_soup(html):
    """Parses the HTML and returns a BeautifulSoup object."""
    return bs4.BeautifulSoup(html, 'html.parser')

def get_tweet(soup):
    """Extracts tweets from the parsed HTML."""
    tweet_data = soup.find_all('article', attrs={'data-testid': 'tweet'})
    
    tweet_list = []
    if tweet_data:
        for tweet in tweet_data:
            date_time = tweet.find('time')

            # get reply count
            reply_count = tweet.find('button', attrs={'data-testid': 'reply'}) #.find_all('span', attrs={'data-testid': '"app-text-transition-container"'})
            reply_count = reply_count.get('aria-label') if reply_count else "N/A"

            # get retweet count
            retweet_count = tweet.find('button', attrs={'data-testid': 'retweet'})
            retweet_count = retweet_count.get('aria-label') if retweet_count else "N/A"

            # get like count
            like_count = tweet.find('button', attrs={'data-testid': 'like'})
            like_count = like_count.get('aria-label') if like_count else "N/A"

            # get watch count
            watch_count = tweet.find('a', href=lambda href: href and "analytics" in href)
            watch_count = watch_count.get('aria-label') if watch_count else "N/A"

            tweet_list.append({
                "date_time": date_time['datetime'] if date_time else "N/A",
                "reply_count": reply_count.split()[0] if reply_count.split()[0].isdigit() else None,
                "retweet_count": retweet_count.split()[0] if retweet_count.split()[0].isdigit() else None,
                "watch_count": watch_count.split()[0] if watch_count.split()[0].isdigit() else None,
                "like_count": like_count.split()[0] if like_count.split()[0].isdigit() else None,
                "text": tweet.text.strip()
            })
    
    return tweet_list