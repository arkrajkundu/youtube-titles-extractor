import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv('Links.csv')
youtube_links = df['Link'].tolist()

def get_youtube_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text

        # Clean up the title (YouTube adds " - YouTube" to the title)
        if title.endswith(" - YouTube"):
            title = title[:-10]

        return title
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_titles_for_urls(url_list):
    data = []
    for url in url_list:
        title = get_youtube_title(url)
        data.append({'URL': url, 'Title': title})
    return data

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

data = get_titles_for_urls(youtube_links) # Get the video titles for all URLs
save_to_excel(data, 'youtube_titles.xlsx')

print(f"Excel sheet 'youtube_titles.xlsx' has been created with the video titles.")