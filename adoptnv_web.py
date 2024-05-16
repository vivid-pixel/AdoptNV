#!/usr/bin/env python3
import math

from adoptnv_core import *
from nicegui import ui


def include_page_top():
    """Shared among all pages and includes title, header text, etc."""

    ui.page_title("AdoptNV - Adopt a pet!")

    with ui.header(elevated=True).style("background-color: #3d3d3d").classes("items-center justify-between"):
        ui.label("AdoptNV")


def include_page_bottom():
    """Shared among all pages and includes footer."""

    with ui.footer().style("background-color: #6c6c6c"):
        ui.label("AdoptNV is not affiliated with any animal shelter")


@ui.page("/", dark=True)
def index_page():
    include_page_top()

    ui.label("AdoptNV Web Test - now using NiceGUI")
    ui.button("Click here to find a pet pal", on_click=lambda: ui.navigate.to(find_pets_page))

    include_page_bottom()

    ui.run()


@ui.page("/pets", dark=True)
def find_pets_page():
    include_page_top()

    with shelve.open(CACHE_FILE) as results_cache:
        # Flag gets later set to True only if the cache file is still empty / was just created
        first_run = False
        # Flag set to True if we detect the cache db is old, otherwise False
        cache_discarded = False

        # We check the time stamp key from the cache file (if no timme stamp, it's a new file)
        try:
            cache_date = results_cache["date_stamp"]

            # We won't use the results if they are too old
            if not cache_is_recent(cache_date):
                cache_discarded = True
        except KeyError:
            # KeyError indicates the file was just made and contains no results yet
            first_run = True
        except Exception as e:
            ui.label(str(e))
        finally:
            if first_run or cache_discarded:
                if first_run:
                    ui.label("Welcome to AdoptNV! I'll help you find the perfect animal companion.")
                elif cache_discarded:
                    ui.label("Welcome back to AdoptNV!")
                    ui.label("You've searched for animals previously, but I'll fetch you some fresh results.")

                animals_list = search_for_animals()
                save_results(animals_list)
            else:
                ui.label("Welcome back to AdoptNV!")
                ui.label("I see you've performed a recent search, so I'll restore those results from the cache.")
                # Load the results cache, but we don't need to save as we aren't updating/changing the cache
                animals_list = load_results(results_cache)

            # We print the list
            display_results(animals_list)

    include_page_bottom()


def display_results(animals_list):
    animals_per_page = 10

    # Divides number of animals by how many animals per page, then rounds it up to nearest int.
    pages_total = math.ceil(len(animals_list) / animals_per_page)

    for animal in animals_list:
        with ui.card():
            with ui.link(target=animal["URL"]):
                with ui.image(animal["Image"]).classes("w-64"):
                    ui.label(animal["Name"]).classes("absolute-bottom text-subtitle2 text-center")
            with ui.grid(columns=2):
                ui.label("Stray: ")
                ui.label(str(animal["Stray"]))
                ui.label("Location: ")
                ui.label(animal["Location"])
                ui.label("Sex: ")
                ui.label(animal["Sex"])
                ui.label("ID: ")
                ui.label(animal["ID"])
                ui.label("Fee: ")
                ui.label(str(animal["Fee"]))


index_page()
