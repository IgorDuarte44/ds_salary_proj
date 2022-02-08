# Import necessary libraries
# standard libraries
from time import time

# custom functions
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse


# extracts the desired data from each of the listing banner, used by the extract_listing function defined below
def extract_listingBanner(listing_soup):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"
        # alt + shift + below arrow to copy the above line of code multiple times, ctrl+d to match a given word and change all its occurrences

    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find(
                "span", class_="css-1pmc6te e11nt52q4"
            ).getText()
        except:
            company_starRating = "NA"
        if company_starRating != "NA":
            try:
                companyName = (
                    listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1")
                    .getText()
                    .replace(company_starRating, "")
                )
            except:
                companyName = "NA"
            # company_starRating.replace("★", "") alternative way
            # just to remove the start sign and keep just the number
            # not remove before to use it to extract the companyName
            company_starRating = company_starRating[:-1]
        # becomes simpler to try to extract the company name
        # if company_starRating == "NA", not need use- to replace(company_starRating, "")
        else:
            try:
                companyName = listing_bannerGroup.find(
                    "div", class_="css-16nw49e e11nt52q1"
                ).getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find(
                "div", class_="css-17x2pwl e11nt52q6"
            ).getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find(
                "div", class_="css-1v5elnn e11nt52q2"
            ).getText()
        except:
            company_roleLocation = "NA"

    return companyName, company_starRating, company_offeredRole, company_roleLocation


# extracts and processes the desired data present in the
# listing description of the job present in each url
def extract_listingDesc(listing_soup):
    # extract_listingDesc_tmpList = []
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            JobDescriptionContainer_found = True
        else:
            JobDescriptionContainer_found = False
            listing_jobDesc = "NA"
    except Exception as e:
        print("[ERROR] {} in extract_Job_listingDescription".format(e))
        JobDescriptionContainer_found = False
        listing_jobDesc = "NA"

    if JobDescriptionContainer_found:
        # jobDesc_items = listing_jobDesc_raw.findAll("li")
        # for jobDesc_item in jobDesc_items:
        # extract_listingDesc_tmpList.append(jobDesc_item.text)
        # listing_jobDesc = " ".join(extract_listingDesc_tmpList)

        extract_listingDesc_tmpList = [
            jobDesc_item.text for jobDesc_item in listing_jobDesc_raw.findAll("li")
        ]
        listing_jobDesc = " ; ".join(extract_listingDesc_tmpList)

        # if it was just one phrase we can just return the
        # getText command from the listing_jobDesc_raw
        if len(listing_jobDesc) <= 10:
            listing_jobDesc = listing_jobDesc_raw.getText()

    return listing_jobDesc


# extract data from each of the links which will be present
# in the listing_set build trough the page.py file
def extract_listing(url):
    request_success = False
    try:
        listing_soup, requested_url = requestAndParse(url)
        request_success = True
    except Exception as e:
        print(
            "[ERROR] Error occurred in extract_listing, requested url: {} is unavailable.".format(
                url
            )
        )
        return ("NA", "NA", "NA", "NA", "NA", "NA")
    # just fils this row with NA values, if some error occurs
    if request_success:
        (
            companyName,
            company_starRating,
            company_offeredRole,
            company_roleLocation,
        ) = extract_listingBanner(listing_soup)
        listing_jobDesc = extract_listingDesc(listing_soup)
        # otherwise just fills the tuple with each entry with the corresponding
        # colum name with the values return by the extract_listingBanner
        # then for the colum listing_jobDesc, return the output
        # of the extract_listingDesc, because this features requires
        # extra processing, at the end also return the request_url
        return (
            companyName,
            company_starRating,
            company_offeredRole,
            company_roleLocation,
            listing_jobDesc,
            requested_url,
        )


if __name__ == "__main__":

    # url = "https://www.glassdoor.sg/job-listing/senior-software-engineer-java-scala-nosql-rakuten-asia-pte-JV_KO0,41_KE42,58.htm?jl=1006818844403&pos=104&ao=1110586&s=58&guid=00000179d5112735aff111df641c01be&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_c8e7e727&cb=1622777342179&jobListingId=1006818844403&cpc=AF8BC9077DDDE68D&jrtk=1-1f7ah29sehimi801-1f7ah29t23ogm000-80a84208d187d367&jvt=aHR0cHM6Ly9zZy5pbmRlZWQuY29tL3JjL2dkL3BuZz9hPUh5MlI4ekNxUWl3d19sM3FuaUJHaFh3RlZEYUJyUWlpeldIM2VBR1ZHTUVSeUk5VEo1ZTEzWWl5dU1sLWJWX0NIeGU4NjBDc3o0dE5sV3ZLT2pRTHFIZU5KTHpPLUhLeEFRSERmeE5CdHNUTUc1RV9FSFR2VW5FNldmWWxJQVp5dXIzNFRZZjIzLWNWNXE0NnRhSTF3V1pKeW54dHhNUkxVRlhEekI2djYwMVZGWl9vbGU5andSYjVhX3BvT0cza0JJb0NYQXo0TVZhNWdvUFY4dXY3WVJTYlMySUpZTVpyR252dEc3ZFM1aXlFQ09icHI0YVRKU2ZLUzkzMUxmLXpyQjFlZHZxbHBxbElZMXhpRksxZmdIMEhFLTJBN2pySHRZa1g0aDJCWGRxTzBCdDM0bDNzWlJDLWIxaUlCT0xnZFh6bjg4cnNjZ1N0V1BHdVhNVm5xT3A3Q0s1UEEtb0QxWDl0WFhkY19WM3Fic0dSS0tfZi1oVUZyUUlrc0o2ZV9yVHNjaFpRVkIyV2V1bmRBejNYQWVPcFZNb3lqZFlONWpLUTdVbDUxTlU5LXFVWnZIT19VWlNEWDVtdVYwR3dNbWpXVDFyaHhMM3ZkcUZqcnM4WDZuc3BYYUhYcHg1dXNUVTVJODdzQk12Q2owaXkxTmRjUmhNXzU2TF9KbXNlY0VzajNWWmFOMDQ3QmNSWU5HSGNFNmctcXUzRUV4bHJrdjQxQ3QteW02ZFo5bE45XzBfb3prR2NBVkdqQU9kaS1UNWRwVnllYzA1OU53Q3Aya2QwdHdoRU5kUnU5UzNlTUR5WmJOSFZGb0t3MnR6V1lKbTllaGxuS3hTMEdoMDhLekVBWGg4OW9BblZGR2U2ajRtMUw3T29CSVNvZWVZaC0wRHRoSTV4eUV0ODJCRERkeTV3QlREUVNTUUZ1Mkp3WUEyRE9qZk5udk5xbzQwaVZKRmF0VWFlVDc2TFl6bnIwQTB2RWRGZlNORE41QmlUaHI3VmgyUWs3bkRGaVFibmUzcWlqZE1ZYzR5TmVYZUhnUFFmOHEwc1Q2aHJrX0hPX1RwbWI5M21hd2hxOEd6a2lEaFMtUQ&ctt=1622777391568"
    url = "https://www.glassdoor.com/job-listing/junior-data-scientist-nyc-or-remote-viacomcbs-JV_IC1132348_KO0,35_KE36,45.htm?jl=1007577263374&pos=101&ao=1136043&s=58&guid=0000017ed4c3c36bb3de3dedd8e4d253&src=GD_JOB_AD&t=SR&vt=w&cs=1_31414865&cb=1644247107013&jobListingId=1007577263374&jrtk=3-0-1frac7gsj3ojb001-1frac7gssu1lk800-c71b72157f64f825-&ctt=1644304962911"
    start_time = time()
    # returns the tuple which will be used to buil a row in the csv output file in the main.py
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] returned in {} seconds".format(time_taken))
