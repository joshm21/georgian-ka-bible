import os
import time
import random
import requests
from bs4 import BeautifulSoup

def get_chapter_urls():
    base_url = 'https://www.orthodoxy.ge/tserili/biblia_sruli/'
    index_url = base_url + 'sarchevi.php'
    response = requests.get(index_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    matching_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('dzveli') or href.startswith('akhali'):
            matching_links.append(base_url + href)
    print(f'found {len(matching_links)} chapter urls')
    return matching_links

def save_chapter_html(url, file_path):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'skipping. {response.status_code} error for {url}')
        return
    with open(file_path, "wb") as f:
        f.write(response.content)

if __name__ == '__main__':
    os.makedirs('html_pages', exist_ok=True)
    urls = get_chapter_urls()
    for i, url in enumerate(urls):

        filename = url.rsplit('/', 1)[-1].replace('htm', 'html')
        file_path = os.path.join('html_pages', filename)

        if os.path.exists(file_path):
            print(f'{filename} already saved, continuing to next file')
            continue

        save_chapter_html(url, file_path)
        print(f"Saved {file_path} ({i+1}/{len(urls)})")
        time.sleep(random.uniform(5, 10))

