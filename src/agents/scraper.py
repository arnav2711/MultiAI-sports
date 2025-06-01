import requests
from bs4 import BeautifulSoup
import urllib.parse

def bing_search_scraper(query, num_results=5):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.bing.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch search results: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for li in soup.find_all('li', class_='b_algo'):
        a_tag = li.find('a', href=True)
        if a_tag:
            results.append(a_tag['href'])
            if len(results) >= num_results:
                break

    return results

def fetch_page_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def process_page_content(url, html_content):
    print(f"\nProcessing content from: {url}")
    print(f"Content length: {len(html_content)} characters")
    print(f"First 500 characters:\n{html_content[:500]}")

def scrape_team_injuries(team_name="Manchester United injuries site:whoscored.com", num_results=5):
    print(f"Searching URLs for: {team_name}")

    urls = bing_search_scraper(team_name, num_results)

    all_data = []

    if urls:
        print("\nFound URLs:")
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")

        for url in urls:
            html = fetch_page_html(url)
            if html:
                all_data.append({
                    "url": url,
                    "html": html
                })
                process_page_content(url, html)
            else:
                print(f"Failed to fetch page content for {url}")

    else:
        print("No URLs found.")

    return all_data


if __name__ == "__main__":
    # If you want to run this file standalone
    data = scrape_team_injuries()
    print(f"\nCollected data for {len(data)} pages.")
