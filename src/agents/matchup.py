import requests
from bs4 import BeautifulSoup
import urllib.parse

def bing_search_scraper(query, num_results=5):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.bing.com/search?q={query}"

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
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
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


if __name__ == "__main__":
    team1 = "Manchester United"
    team2 = "Chelsea"

    # Strong prompt to get detailed info on past matchups, morale, form:
    prompt = (f"recent matches between {team1} and {team2}, "
              f"latest match results, team morale, current form, "
              f"player performance, injury updates, expert analysis")

    print(f"Searching URLs for: {prompt}")

    urls = bing_search_scraper(prompt)
    if urls:
        print("\nFound URLs:")
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")

        for url in urls:
            print(f"\nProcessing content from: {url}")
            html = fetch_page_html(url)
            if html:
                print(f"Content length: {len(html)} characters")
                print(f"First 500 characters:\n{html[:500]}")
            else:
                print(f"Failed to fetch page content for {url}")
    else:
        print("No URLs found.")
