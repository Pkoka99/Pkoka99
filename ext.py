import requests
from bs4 import BeautifulSoup

def extract_text_from_rentry(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main text area (Rentry.co stores text in a textarea or div with specific class)
        # Try different selectors as Rentry might change their HTML structure
        text_area = soup.find('textarea', {'id': 'text'})
        if not text_area:
            text_area = soup.find('div', {'class': 'entry-text-container'})
        
        if text_area:
            # Get the text and clean it up
            text = text_area.get_text().strip()
            return text
        else:
            return "Could not find the text content on the page."

    except requests.RequestException as e:
        return f"Error fetching the URL: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

# URL to extract text from
gg = input("code : ")
url = f"https://rentry.co/{gg}"

# Extract and print the text
extrac = extract_text_from_rentry(url)
with open("acc.txt", "a") as file:
     file.write(f"{extrac}")
