import requests
from bs4 import BeautifulSoup
import re
import csv

def extract_episodes(text):
    # Extract numeric value from episode text using regular expressions
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return 0

def extract_date(text):
    # Extract date in the format (Month Year)
    match = re.search(r'(\w+\s\d{4})', text)
    if match:
        return match.group()
    return ''

def scrape_popular_anime(num_anime):
    anime_list = []
    page = 0

    while len(anime_list) < num_anime:
        url = f'https://myanimelist.net/topanime.php?limit={page * 50}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='top-ranking-table')
        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            rank = row.find('td', class_='rank').text.strip()
            title = row.find('div', class_='di-ib clearfix').a.text.strip()
            score = row.find('td', class_='score').text.strip()

            # Extract episode and date information
            information_div = row.find('div', class_='information di-ib mt4')
            episodes_text = information_div.find(text=True, recursive=False).strip()
            episodes = extract_episodes(episodes_text)
            date_element = information_div.find('span', class_='information season')
            date_text = date_element.text.strip() if date_element else ''
            date = extract_date(date_text)
            anime_list.append({'Rank': rank, 'Title': title, 'Score': score, 'Episodes': episodes, 'Date': date})

            if len(anime_list) >= num_anime:
                break

        page += 1

    return anime_list[:num_anime]

# Specify the number of anime to scrape (e.g., 1000)
num_anime_to_scrape = 1000

# Call the function to scrape the popular anime
popular_anime = scrape_popular_anime(num_anime_to_scrape)

# Save the results to a CSV file
csv_file = 'popular_anime.csv'
header = ['Rank', 'Title', 'Score', 'Episodes', 'Date']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(popular_anime)

print(f'Successfully saved {len(popular_anime)} anime entries to {csv_file}.')
