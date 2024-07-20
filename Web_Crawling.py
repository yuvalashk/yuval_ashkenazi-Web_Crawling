import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(url):
    """
    Sends an HTTP request to the given URL and returns the page content if the request is successful.

    Args:
    url (str): The URL of the page to fetch.

    Returns:
    str: The content of the page if the request is successful, otherwise None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def extract_info(url):
    """
    Parses the page content and extracts the page title, URL, and main text content.

    Args:
    url (str): The URL of the page to parse.

    Returns:
    tuple: A tuple containing the page title, URL, and main text content.
    """
    content = get_page_content(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        if soup.title:
            page_title = soup.title.string
        else:
            page_title = 'No Title'
        page_text = ''
        for p in soup.find_all('p'):
            page_text += p.get_text() + ' '
        page_text = page_text.strip()
        return page_title, url, page_text
    return None, None, None


def get_links(url):
    """
    Fetches the page content and extracts all HTTP links from the page.

    Args:
    url (str): The URL of the page to fetch and parse.

    Returns:
    list: A list of URLs found on the page.
    """
    content = get_page_content(url)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
        return links
    return []


def save_to_excel(data, filename):
    """
    Saves the extracted data to an Excel file.

    Args:
    data (list): The list of extracted data.
    filename (str): The name of the Excel file to save the data to.
    """
    df = pd.DataFrame(data, columns=['Page Title', 'Page URL', 'Page Content'])
    df.to_excel(filename, index=False)


if __name__ == "__main__":
    # Define the starting URL for crawling
    start_url = 'http://example.com'
    links = get_links(start_url)
    data = []
    page_title, page_url, page_content = extract_info(start_url)
    if page_title and page_url and page_content:
        data.append([page_title, page_url, page_content])

    for link in links:
        page_title, page_url, page_content = extract_info(link)
        if page_title and page_url and page_content:
            data.append([page_title, page_url, page_content])

    # Save the data to an Excel file
    save_to_excel(data, r"Path_to_file\file_name.xlsx")
