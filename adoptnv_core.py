#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import shelve

# Global constants
CACHE_FILE = "adoptnv_results"


def main():
    """AdoptNV's goal is to encourage animal adoption in the US state of Nevada."""

    # Check for existing search result cache
    animals_cache = shelve.open(CACHE_FILE)

    if animals_cache:
        cache_date = animals_cache["date_stamp"]
        print(f"Found previous search results in local cache (Time stamp: {cache_date})")

        if cache_is_valid(cache_date):
            print("Previous results are still fresh. Building list.")
            animals_list = animals_cache["animals_list"]
        else:
            print("Cached results are stale (> 1 hr). Updating!")
            animals_list = animal_search()
            # Pass the list to save_results to update the cache
            save_results(animals_list)

    print_results(animals_list)


def save_results(animals_list):
    """Write animals_list to a file to save the search results"""

    with shelve.open(CACHE_FILE) as animals_cache:
        animals_cache["animals_list"] = animals_list
        animals_cache["date_stamp"] = datetime.now()

        return True


def flask_test():
    calculation = 5 * 5
    return calculation


def cache_is_valid(cache_date):
    """Check if cache file is recent enough to not require an update
    Returns True or False
    """

    cache_age_limit = timedelta(hours=1)  # Max age of 1 hr for cached results
    date_now = datetime.now()

    if date_now - cache_date <= cache_age_limit:
        print(f"TRUE - {date_now}, {cache_date}, {cache_age_limit}")
        return True
    else:
        print(f"FALSE - {date_now}, {cache_date}, {cache_age_limit}")
        return False


def print_results(animals_list):
    """Print adoptable animal results."""

    print("Printing search results.")
    spacer = "======"
    divider = "---"
    print(f"{spacer} RESULTS ({len(animals_list)} animals found) {spacer}")
    for animal in animals_list:
        # Name, Image, URL, Location, Sex, ID, Fee
        print(f"Name: {animal["Name"]}")
        print(f"Image: {animal["Image"]}")
        print(f"URL: {animal["URL"]}")
        print(f"Location: {animal["Location"]}")
        print(f"Sex: {animal["Sex"]}")
        print(f"ID: {animal["ID"]}")
        print(f"Fee: {animal["Fee"]}")
        print(divider)
    print(f"{spacer} END OF RESULTS {spacer}")


def animal_search():
    """Scour the 'net for cute animals that want to adopt a human"""

    # Declare animals_list to store the individual pets
    animals_list = []

    # Load the first page of the adoption search (we'll loop through all pages later)
    url = "https://animalfoundation.com/adopt-a-pet/adoption-search"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find list of pages and define variable with total count.
    pages_element = soup.find("li", class_="next")
    total_pages = int(pages_element.previous_element)

    print(f"Processing {total_pages} pages of adoption results.")
    current_page = 1  # Declare and define page counter

    # Keep scraping adoption results until we've parsed the final page
    while current_page <= total_pages:
        # Eliminate redundant request parsing (we already downloaded the first page)
        if not current_page == 1:
            url = f"https://animalfoundation.com/adopt-a-pet/adoption-search?ccm_paging_p={current_page}"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

        # Grab the results from this page
        results = soup.find(id="list-results")

        # The rest of this loop will run regardless of which page we're on.
        pet_elements = results.find_all("a", class_="item")
        for pet in pet_elements:
            pet_name = pet.find("img", class_="lazy").attrs["alt"]
            pet_image = pet.find("img", class_="lazy").attrs["data-src"]
            pet_url = pet.attrs["href"]
            pet_location = pet.ul.li.text

            # This includes the html tags, so we'll strip when adding to list
            pet_sex = pet.ul.li.find_next_sibling()
            pet_id = pet_sex.find_next_sibling()

            # This site displays either "FEE-WAIVED" or nothing at all
            if pet.find("h3").text != "FEE-WAIVED":
                pet_fee_waived = False
            else:
                pet_fee_waived = True

            # Append this animal's dictionary to our list
            animals_list.append({"Name": pet_name,
                                 "Image": pet_image,
                                 "URL": pet_url,
                                 "Location": pet_location,
                                 "Sex": pet_sex.text,
                                 "ID": pet_id.text,
                                 "Fee": pet_fee_waived})

        # Increment page number before we continue the loop
        current_page += 1

    # Now return the list of animals to the parent method
    return animals_list

if __name__ == "__main__":
    main()
