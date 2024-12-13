import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Initialize visited set and depth tracking
visited = set()
data_folder = "data"
MAX_PAGES_PER_SITE = 200
KEYWORDS = ["skin", "hair", "acne", "derma", "cosmetic", "beauty"]  # Add more relevant terms as needed

# Ensure the data folder exists
os.makedirs(data_folder, exist_ok=True)

def save_page_content(driver, url):
    """
    Save the text content of the page to a file named site#title.txt inside the data folder.
    """
    title = driver.title or "untitled"
    sanitized_title = title.replace(" ", "_").replace("/", "_")
    parsed_url = urlparse(url)
    filename = os.path.join(data_folder, f"{parsed_url.netloc}#{sanitized_title}.txt")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(driver.find_element(By.TAG_NAME, "body").text)

def site_already_scraped(domain):
    """
    Check if there is already a file with the prefix of the domain in the data folder.
    """
    for filename in os.listdir(data_folder):
        if filename.startswith(domain):
            print(f"Checkpoint: {domain} already scraped, skipping.")
            return True
    return False

def is_relevant_link(link):
    """
    Check if the link contains any keyword in the route (path after '/').
    """
    parsed_url = urlparse(link)
    route = parsed_url.path.lower()
    for keyword in KEYWORDS:
        if keyword in route:
            return True
    return False

def scrape_site(driver, url, depth, max_depth, page_counter):
    """
    Recursive function to scrape a site up to a specified depth and limit of pages.
    """
    if depth > max_depth or url in visited or page_counter[0] >= MAX_PAGES_PER_SITE:
        return

    # Visit the URL
    print(f"Visiting: {url}, Depth: {depth}, Pages Scraped: {page_counter[0]}")
    try:
        driver.get(url)
        visited.add(url)
        save_page_content(driver, url)
        page_counter[0] += 1
    except Exception as e:
        print(f"Error visiting {url}: {e}")
        return

    # Collect all same-site links
    current_domain = urlparse(url).netloc
    links = set()
    try:
        for a_tag in driver.find_elements(By.TAG_NAME, "a"):
            href = a_tag.get_attribute("href")
            if href and urlparse(href).netloc == current_domain and is_relevant_link(href):
                full_url = urljoin(url, href)
                links.add(full_url)
    except Exception as e:
        print(f"Error collecting links on {url}: {e}")

    # Recursively scrape each link
    for link in links:
        if page_counter[0] >= MAX_PAGES_PER_SITE:
            print(f"Reached maximum pages ({MAX_PAGES_PER_SITE}) for {current_domain}.")
            break
        scrape_site(driver, link, depth + 1, max_depth, page_counter)

def main():
    # Read root links from file
    with open("root_links.txt", "r") as file:
        root_links = [line.strip() for line in file.readlines()]

    try:
        for root_link in root_links:
            parsed_root = urlparse(root_link)
            domain = parsed_root.netloc

            # Checkpoint: Skip if the site is already scraped
            if site_already_scraped(domain):
                continue

            # Initialize a page counter for the site
            page_counter = [0]

            # Start scraping
            scrape_site(driver, root_link, depth=0, max_depth=4, page_counter=page_counter)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
