#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class AnimalShelter:
    name = str
    filters = str
    filter_url = str

    def get_name(self):
        return self.name

    def get_filters(self):
        return self.filters

    def get_filter_url(self):
        return self.filter_url


class AnimalFoundation(AnimalShelter):
    """The Animal Foundation"""

    def __init__(self):
        # self.base_url = "https://animalfoundation.com/adopt-a-pet/adoption-search/"
        # First item in each list is blank but means "Any" animal. (blank = filter off)
        self.name = "The Animal Foundation"
        self.filters = {"type": ["", "BIRD", "CAT", "DOG", "FISH", "SMALL+MAMMAL"],
                        "sex": ["", "MALE", "FEMALE"],
                        "size": ["", "KITTN", "LARGE", "MED", "PUPPY", "SMALL", "TOY", "X-LRG"],
                        "location": ["", "At+an+Offsite+Location", "Campus+Adoption+Center", "En+Route", "In+Foster",
                                     "Lied+Animal+Shelter"],
                        "status": ["", "1"],  # "1" is Fee Waived
                        "age": ["", "Unknown", "Under+6+Months", "6+Months+to+3+Years", "3+years+"],
                        "id": ""

                        }
        self.filter_url = \
            (f"https://animalfoundation.com/adopt-a-pet/adoption-search?animalType={self.filters["type"]}&animalSex="
             f"{self.filters["sex"]}&animalSize={self.filters["size"]}&filter=Search&location="
             f"{self.filters["location"]}&animalStatus={self.filters["status"]}&animalAge={self.filters["age"]}"
             f"&animalID={self.filters["id"]}")


class NevadaSPCA:
    """Nevada Society for the Prevention of Cruelty to Animals"""

    def __init__(self):
        # self.base_url = "https://www.shelterluv.com/embed/20674"
        self.name = "Nevada Society for the Prevention of Cruelty to Animals"
        # self.filters
        # self.filter_url


class RescueMe:
    """Rescue Me! Animal Rescue Network"""

    def __init__(self):
        # self.base_url = "https://cat.rescueme.org/Nevada"
        self.name = "Rescue Me! Animal Rescue Network"
        self.filters = {
            "type": ["dog", "cat", "horse", "rabbit", "farmanimal", "rodent", "reptile", "bird", "wildbird", "wildlife"]
        }
        self.filter_url = f"https://{self.filters["type"]}.rescueme.org/Nevada"
