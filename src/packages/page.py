# Import necessary libraries
# standard libraries
import re
from time import time

# 3rd-party libraries
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse

# this py file is just to build the auxiliary functions capable of extracting from the html code in the first web page after the user
# searchs what we wants, the maximum number of jobs provided by the glassdoor site which match what was search bu the user, this is important
# because it defined what is the maximum number of jobs possible to return as output in the csv file

# extract maximum number of jobs stated and the number of pages needed by the glassdor site to display
# all the found jobs matching what was searched by the user, only applicable for the "base" url
def extract_maximums(base_url):
    # from the common.py file
    page_soup, _ = requestAndParse(base_url)
    # tmp_match variable saves the number of jobs found [0] because is the 1 in the webpage
    tmp_match_1 = [
        item for item in page_soup.find_all("p") if "data-test" in item.attrs
    ][0]
    # [-1] to grab the number of pages, the last contem of data-test type in the web_page
    # tmp_match_2 = [
    # item for item in page_soup.find_all("div") if "data-test" in item.attrs
    # ][-1]
    maxJobs_raw = tmp_match_1.get_text()  # e.g. '9940 jobs' in this case
    # e.g. 'Page 1 of 30' in this case, the original method to extract maxPages
    # was not working, i just commented it
    maxPages_raw = page_soup.select("div.paginationFooter")[0].get_text()
    try:
        assert "jobs" in maxJobs_raw
        assert "Page" in maxPages_raw
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")
    # to convert them from strings into numbers
    maxJobs = re.sub(r"\D", "", maxJobs_raw)
    maxPages = maxPages_raw.split(" ")[-1]
    # maxPages = re.sub(r"\D", "", maxPages_raw)[1:]

    return (int(maxJobs), int(maxPages))


# extract listing urls
def extract_listings(page_soup):
    # this is slower but more robust:
    # get all links regardless of type and extract those that match
    # the desired type, all links of the other pages that contained all
    # the remaining job search results

    # listings_list = list()
    # for a in page_soup.find_all("a", href=True):
    # if "/partner/jobListing.htm?" in a["href"]:
    # print("Found the URL:", a['href'])
    # listings_list.append("www.glassdoor.com" + a["href"])
    # all in a list comprehension
    listings_list = [
        "www.glassdoor.com" + link["href"]
        for link in page_soup.find_all("a", href=True)
        if "/partner/jobListing.htm?" in link["href"]
    ]

    # remove all the duplicated links (there is 3 or 4 for job listing)
    listings_set = set(listings_list)
    # should be more than 0, return the number of unique links to visit
    # 30 per page
    jobCount = len(listings_set)

    try:
        assert jobCount != 0
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    # all the unique links containing the remaining job search results
    # and the number of
    return listings_set, jobCount


if __name__ == "__main__":

    url = "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
    start_time = time()
    maxJobs, maxPages = extract_maximums(url)
    time_taken = time() - start_time
    print(
        "[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(
            maxJobs, maxPages
        )
    )
    print("[INFO] returned in {} seconds".format(time_taken))

    url = "https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm"
    start_time = time()
    page_soup, requested_url = requestAndParse(url)
    listings_set, jobCount = extract_listings(page_soup)
    time_taken = time() - start_time
    print(listings_set)
    print(jobCount)
    print("[INFO] returned in {} seconds".format(time_taken))
