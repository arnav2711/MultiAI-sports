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

    # Bing search results links are usually in <li class="b_algo"> with <a href=...>
    for li in soup.find_all('li', class_='b_algo'):
        a_tag = li.find('a', href=True)
        if a_tag:
            results.append(a_tag['href'])
            if len(results) >= num_results:
                break

    return results

if __name__ == "__main__":
    team_name = "Manchester United injuries site:whoscored.com"
    print(f"Searching URLs for: {team_name}")

    urls = bing_search_scraper(team_name)
    if urls:
        for i, url in enumerate(urls, 1):
            print(f"{i}. {url}")
    else:
        print("No URLs found.")
