#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import shelve

# Global constants
CACHE_FILE = "adoptnv_results"


def load_results(results_cache):
    """Converts the DB of cached results into a list format that we can work with"""

    animals_list = []

    for animal in results_cache["animals_list"]:
        animals_list.append(animal)

    return animals_list


def save_results(animals_list):
    """Write animals_list to a file to save the search results"""

    with shelve.open(CACHE_FILE) as results_cache:
        results_cache["animals_list"] = animals_list
        results_cache["date_stamp"] = datetime.now()


def cache_is_recent(cache_date):
    """Check if cache file is fresh enough to not require an update. Returns true or false"""

    cache_age_limit = timedelta(hours=1)  # Max age of 1 hr for cached results
    date_now = datetime.now()

    if date_now - cache_date <= cache_age_limit:
        return True
    else:
        return False


# def print_results(animals_list):
#     """Print adoptable animal results."""
#     list_length = len(animals_list)
#
#     if list_length == 0:
#         print("Seems like the list failed to populate.")
#     else:
#         print("Printing search results.")
#         spacer = "======"
#         divider = "---"
#         print(f"{spacer} RESULTS ({list_length} animals found) {spacer}")
#         try:
#             for animal in animals_list:
#                 # Name, Stray, Image, URL, Location, Sex, ID, Fee
#                 print(f"Name: {animal["Name"]}")
#                 print(f"Stray: {animal["Stray"]}")
#                 print(f"Image: {animal["Image"]}")
#                 print(f"URL: {animal["URL"]}")
#                 print(f"Location: {animal["Location"]}")
#                 print(f"Sex: {animal["Sex"]}")
#                 print(f"ID: {animal["ID"]}")
#                 print(f"Fee: {animal["Fee"]}")
#                 print(divider)
#         except TypeError:
#             print("Something seems wrong with the list of results. Unable to populate list.")
#         finally:
#             print(f"{spacer} END OF RESULTS {spacer}")


def search_for_animals():
    """Scour the net for cute animals that want to adopt a human. Returns animals_list"""

    # TODO: Nevada SPCA - https://www.shelterluv.com/embed/20674
    # TODO: https://cat.rescueme.org/Nevada https://dog.rescueme.org/Nevada

    # Declare animals_list to store the individual pets
    animals_list = []

    # Load the first page of the adoption search (we'll loop through all pages later)
    url = "https://animalfoundation.com/adopt-a-pet/adoption-search"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find list of pages and define variable with total count.
    pages_element = soup.find("li", class_="next")
    total_pages = int(pages_element.previous)

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
            # Names contain an asterisk if they are strays and were named by the shelter
            pet_name = pet.find("img", class_="lazy").attrs["alt"]
            # If there's an asterisk, mark pet as a stray, then remove the asterisk from its name
            if pet_name[0] == "*":
                # Shelter's current naming convention has the asterisk as the 1st character
                pet_name = pet_name[1:]
                pet_is_stray = True
            else:
                pet_is_stray = False

            pet_image = pet.find("img", class_="lazy").attrs["data-src"]
            pet_url = pet.attrs["href"]
            pet_location = pet.ul.li.text

            # This includes the html tags, so we'll strip when adding to list
            pet_sex = pet.ul.li.find_next_sibling()
            pet_id = pet_sex.find_next_sibling()

            # This shelter's site displays either "FEE-WAIVED" or nothing at all.
            if pet.find("h3").text == "FEE-WAIVED":
                # What a bargain! Animal requires no fee.
                pet_has_fee = False
            else:
                # Fee is not waived, so this cutie-pie will cost you something.
                pet_has_fee = False

            # Append this animal's dictionary to our list.
            animals_list.append({"Name": pet_name,
                                 "Stray": pet_is_stray,
                                 "Image": pet_image,
                                 "URL": pet_url,
                                 "Location": pet_location,
                                 "Sex": pet_sex.text,
                                 "ID": pet_id.text,
                                 "Fee": pet_has_fee})

        # Increment page number before we continue the loop
        current_page += 1

    # Now return the list of animals to the parent method
    return animals_list


if __name__ == "__main__":
    print("This file contains logic for the web app. Try running adoptnv_web.py, instead!")
