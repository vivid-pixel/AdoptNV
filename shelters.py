#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class AnimalShelter:
    name = str
    base_url = str
    filter_options = dict
    filters = dict
    filter_url = str
    page_number = 1
    total_pages = int

    def get_name(self):
        return self.name

    def get_base_url(self):
        return self.base_url

    def get_filter_options(self):
        return self.filter_options.items()

    def get_filter_url(self):
        return self.filter_url

    def get_page_number(self):
        return self.page_number

    def get_active_filters(self):
        return self.active_filters

    def get_total_pages(self):
        return self.total_pages

    def set_page_number(self, page_number):
        self.page_number = page_number

    def set_total_pages(self, total_pages):
        self.total_pages = total_pages

    def set_active_filter(self, filter_name, filter_value):
        self.active_filters[filter_name] = filter_value


class AnimalFoundation(AnimalShelter):
    """The Animal Foundation"""

    def __init__(self):
        self.base_url = "https://animalfoundation.com/adopt-a-pet/adoption-search/"
        # First item in each list is blank but means "Any" animal. (blank = filter off)
        self.name = "The Animal Foundation"
        self.filter_options = {"type": ["", "BIRD", "CAT", "DOG", "FISH", "SMALL+MAMMAL"],
                               "sex": ["", "MALE", "FEMALE"],
                               "size": ["", "KITTN", "LARGE", "MED", "PUPPY", "SMALL", "TOY", "X-LRG"],
                               "location": ["", "At+an+Offsite+Location", "Campus+Adoption+Center", "En+Route",
                                            "In+Foster", "Lied+Animal+Shelter"],
                               "status": ["", "1"],  # "1" is Fee Waived
                               "age": ["", "Unknown", "Under+6+Months", "6+Months+to+3+Years", "3+years+"],
                               "id": ""
                               }
        self.active_filters = {"type": "",
                        "sex": "",
                        "size": "",
                        "location": "",
                        "status": "",  # "1" is Fee Waived
                        "age": "",
                        "id": ""
                        }
        self.filter_url = \
            (f"https://animalfoundation.com/adopt-a-pet/adoption-search?animalType={self.active_filters["type"]}"
             f"&animalSex={self.active_filters["sex"]}&animalSize={self.active_filters["size"]}&filter=Search&location="
             f"{self.active_filters["location"]}&animalStatus={self.active_filters["status"]}&animalAge="
             f"{self.active_filters["age"]}&animalID={self.active_filters["id"]}&ccm_paging_p={self.page_number}")


class NevadaSPCA:
    """Nevada Society for the Prevention of Cruelty to Animals"""

    def __init__(self):
        self.base_url = "https://www.shelterluv.com/embed/20674"
        self.name = "Nevada Society for the Prevention of Cruelty to Animals"
        # self.filters
        # self.filter_url


class RescueMe:
    """Rescue Me! Animal Rescue Network"""

    def __init__(self):
        self.base_url = "https://cat.rescueme.org/Nevada"
        self.name = "Rescue Me! Animal Rescue Network"
        self.filter_options = {
            "type": ["dog", "cat", "horse", "rabbit", "farmanimal", "rodent", "reptile", "bird", "wildbird", "wildlife"]
        }
        self.filter_url = f"https://{self.filters["type"]}.rescueme.org/Nevada"
