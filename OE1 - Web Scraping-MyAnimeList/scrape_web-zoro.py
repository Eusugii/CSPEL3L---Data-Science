import requests
from bs4 import BeautifulSoup
import csv

# Send a GET request to the Crunchyroll Popular page
url = 'https://zoro.to/top-airing'
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the container with the popular anime data
container = soup.find('div',class_='tab-content')

# Open a CSV file in write mode
with open('zoro_anime.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Title', 'Episodes'])

    # Extract data from each anime in the container and write to the CSV file
    count = 0  # Track the number of anime found
    if container:
        for anime in container.find_all('div',class_='flw-item'): #
            title_element = anime.find('a', class_='dynamic-name')
            if title_element:# and duration_element:
                title = title_element.text.strip()
                #duration = episodes_element.text.strip()

                # Write the data to the CSV file
                writer.writerow([title, ''])

                count += 1
                
                if count >= 50:
                    break
                
print('Data saved successfully to zoro_anime.csv')
