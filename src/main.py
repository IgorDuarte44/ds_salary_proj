# Import necessary libraries
# standard libraries
import csv
import json
import os

# just to check the time it takes for the scrapping to be perfomed
from datetime import datetime
from time import time

# 3rd-party libraries
import enlighten

# custom functions defined in the py scrips present in the packages folder
from packages.common import requestAndParse
from packages.listing import extract_listing
from packages.page import extract_listings, extract_maximums


# loads user defined parameters present in the congig.json file, base_url and target_num(number of job samples wantes in the final output csv)
def load_configs(path):
    with open(path) as config_file:
        configurations = json.load(config_file)

    base_url = configurations["base_url"]
    target_num = int(configurations["target_num"])
    return base_url, target_num


# appends list of tuples in specified output csv file
# a tuple is written as a single row in csv file (function which writes to the output csv file a line
# all the data previouly scrapped)
def fileWriter(listOfTuples, output_fileName):
    with open(output_fileName, "a", newline="") as out:
        csv_out = csv.writer(out)
        for row_tuple in listOfTuples:
            try:
                csv_out.writerow(row_tuple)
                # can also do csv_out.writerows(data) instead of the for loop
            except Exception as e:
                print("[WARN] In filewriter: {}".format(e))


# updates url according to the page_index desired by the user
# importante to return the url when the user clicks to go to the next page of results
def update_url(prev_url, page_index):
    if page_index == 1:
        prev_substring = ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"
    else:
        prev_substring = "_IP" + str(page_index - 1) + ".htm"
        new_substring = "_IP" + str(page_index) + ".htm"

    new_url = prev_url.replace(prev_substring, new_substring)
    return new_url


# for really output results when this main file is run
if __name__ == "__main__":
    base_url, target_num = load_configs(path="data\config.json")

    # initialises output directory and file
    if not os.path.exists("output"):
        os.makedirs("output")
    now = datetime.now()  # current date and time
    # name for the output csv file
    output_fileName = "./output/output_" + now.strftime("%d-%m-%Y") + ".csv"
    csv_header = [
        (
            "companyName",
            "company_starRating",
            "company_offeredRole",
            "company_roleLocation",
            "listing_jobDesc",
            "requested_url",
        )
    ]
    # writes the first row (the column names) into the csv output file
    fileWriter(listOfTuples=csv_header, output_fileName=output_fileName)

    maxJobs, maxPages = extract_maximums(base_url)
    print(
        "[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(
            maxJobs, maxPages
        )
    )
    if target_num >= maxJobs:
        print(
            "[ERROR] Target number larger than maximum number of jobs. Exiting program...\n"
        )
        os._exit(0)

    # initialises enlighten_manager, just to create sort of a progress bar of the scrapping we are doing at each time
    enlighten_manager = enlighten.get_manager()
    progress_outer = enlighten_manager.counter(
        total=target_num,
        desc="Total progress",
        unit="listings",
        color="green",
        leave=False,
    )

    # initialise variables
    page_index = 1
    # number of jobs scrapped at the beginning is 0
    total_listingCount = 0
    # initialises prev_url as base_url, as it makes sense
    prev_url = base_url

    while total_listingCount <= target_num:
        # clean up buffer, list where will be store all the features of this page job search results
        list_returnedTuple = []

        new_url = update_url(prev_url, page_index)
        page_soup, _ = requestAndParse(new_url)
        # in order to extract all the links of the job searches present in this web page
        listings_set, jobCount = extract_listings(page_soup)
        progress_inner = enlighten_manager.counter(
            total=len(listings_set),
            desc="Listings scraped from page",
            unit="listings",
            color="blue",
            leave=False,
        )

        print("\n[INFO] Processing page index {}: {}".format(page_index, new_url))
        print("[INFO] Found {} links in page index {}".format(jobCount, page_index))
        # go one by one of the job search links and scrape individually all the info needed about each of the jobs found trough the links
        for listing_url in listings_set:

            # to implement cache here
            returned_tuple = extract_listing(listing_url)
            list_returnedTuple.append(returned_tuple)
            # print(returned_tuple)
            progress_inner.update()

        progress_inner.close()
        # writes all the scrapped data, each job as a different row in the output file
        fileWriter(listOfTuples=list_returnedTuple, output_fileName=output_fileName)

        # done with page, moving onto next page
        # but first let s update the total_listingCount varibale in order to then revaluate it in the while loop condition
        total_listingCount = total_listingCount + jobCount
        print(
            "[INFO] Finished processing page index {}; Total number of jobs processed: {}".format(
                page_index, total_listingCount
            )
        )
        # really moving into the next page now
        page_index = page_index + 1
        prev_url = new_url
        progress_outer.update(jobCount)

    progress_outer.close()
