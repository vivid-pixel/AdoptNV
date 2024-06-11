#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Results:
    total_pages = int
    page_number = 1
    pets_list = list
    return_flags = dict
    filters = dict

    @staticmethod
    def set_pets(pets_list):
        Results.pets_list = pets_list

    @staticmethod
    def set_flags(return_flags):
        Results.return_flags = return_flags

    @staticmethod
    def set_filters(filters):
        Results.filters = filters

    @staticmethod
    def get_pets():
        return Results.pets_list

    @staticmethod
    def get_flags():
        return Results.return_flags

    @staticmethod
    def get_filters():
        return Results.filters


@dataclass
class AnimalShelter:
    name = str
    base_url = str
    filter_url = str
    filter_options = dict
    page_count = int
    current_page = int

    def get_name(self):
        return self.name

    def get_base_url(self):
        return self.base_url

    def get_filter_url(self):
        return self.filter_url

    def get_filter_options(self):
        return self.filter_options

    def get_page_count(self):
        return self.page_count

    def get_current_page(self):
        return self.current_page

    def set_page_count(self, pages):
        self.page_count = pages

    def set_current_page(self, current):
        self.current_page = current


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
             f"{self.active_filters["age"]}&animalID={self.active_filters["id"]}&ccm_paging_p={self.current_page}")


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
        # self.filter_url = f"https://{self.filters["type"]}.rescueme.org/Nevada"
