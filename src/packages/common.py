# Import necessary libraries
# standard libraries
import time
from urllib.parse import urlparse

# 3rd-party libraries
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup as soup

# this py is just to define the functions capable of verifying the URL provided at each time and ensure that we can load the webpage and
# pass it html code through the beautiful soup library

# checks and corrects the scheme of the requested url
def checkURL(requested_url):
    # it scheme is empty, the if condition becomes True
    if not urlparse(requested_url).scheme:
        requested_url = "https://" + requested_url
    return requested_url


# fetches data from requested url and parses it through beautifulsoup
def requestAndParse(requested_url):
    # adds https:// if necessary
    requested_url = checkURL(requested_url)
    try:
        # define headers to be provided for request authentication

        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }

        request_obj = Request(url=requested_url, headers=headers)
        opened_url = urlopen(request_obj)
        page_html = opened_url.read()
        opened_url.close()
        page_soup = soup(page_html, "html.parser")
        return page_soup, requested_url

    except Exception as e:
        print(e)


if __name__ == "__main__":

    url = "https://www.glassdoor.com/Job/jobs.htm?sc.generalKeyword=%22data+scientist%22&sc.locationSeoString=san+francisco&locId=1147401&locT=C&radius=100"
    start_time = time.time()
    page_soup, requested_url = requestAndParse(url)
    time_taken = time.time() - start_time
    print(page_soup)
    print("[INFO] returned in {} seconds".format(time_taken))
