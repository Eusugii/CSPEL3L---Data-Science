import requests
from bs4 import BeautifulSoup
import csv

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

            # Extract episode information
            episodes = row.find('div', class_='information di-ib mt4').text.strip().split()[0]
            anime_list.append({'Rank': rank, 'Title': title, 'Score': score, 'Episodes': episodes})

            if len(anime_list) >= num_anime:
                break

        page += 1

    return anime_list[:num_anime]

# Specify the number of anime to scrape (e.g., 1000)
num_anime_to_scrape = 8000

# Call the function to scrape the popular anime
popular_anime = scrape_popular_anime(num_anime_to_scrape)

# Save the results to a CSV file
csv_file = 'popular_anime.csv'
header = ['Rank', 'Title', 'Score', 'Episodes']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(popular_anime)

print(f'Successfully saved {len(popular_anime)} anime entries to {csv_file}.')
