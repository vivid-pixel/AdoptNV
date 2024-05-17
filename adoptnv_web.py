#!/usr/bin/env python3
import math

from adoptnv_core import build_results
from nicegui import ui


def include_page_top():
    """Shared among all pages and includes header text."""

    with ui.header(elevated=True).style("background-color: #3d3d3d").classes("items-center justify-between"):
        ui.link("AdoptNV :: Find pets in Nevada","/")


def include_page_bottom():
    """Shared among all pages and includes footer."""

    with ui.footer().style("background-color: #6c6c6c"):
        ui.label("AdoptNV uses Python, NiceGUI, BeautifulSoup. Not affiliated with any animal shelter.")


@ui.page("/")
def index_page():
    include_page_top()

    ui.label("Welcome to AdoptNV.")
    ui.button("Click here to find a pet pal", on_click=lambda: ui.navigate.to(find_pets_page))

    include_page_bottom()

    # TODO: Disable auto-reload / Resolve "asyncio.run() cannot be called from a running event loop"
    ui.run(reload=True, title="AdoptNV :: Adopt a pet!", dark=True)


@ui.page("/pets")
def find_pets_page():
    include_page_top()

    pet_results, return_flags = build_results()

    # Explanation of flags: first_run: cache file empty; cache_discarded: file too old; exception: unrecoverable error
    if return_flags["exception"] is not None:
        # Don't try to print the list if we had an unrecoverable exception.
        ui.log(return_flags["exception"])
    else:
        # List was successfully created. Check the other flags for a tailored greeting
        if return_flags["first_run"]:
            ui.label("Welcome to AdoptNV! I'll help you find the perfect animal companion.")
        elif return_flags["cache_discarded"]:
            ui.label("Welcome back to AdoptNV!")
            ui.label("You've searched for animals previously, but I'll fetch you some fresh results.")
        else:
            ui.label("Welcome back to AdoptNV!")
            ui.label("I see you've performed a recent search, so I'll restore those results from the cache.")

        # Done with greetings; now show the pet results.
        display_results(pet_results)

    include_page_bottom()


def display_results(animals_list):
    animals_per_page = 10

    # Divides number of animals by how many animals per page, then rounds it up to nearest int.
    pages_total = math.ceil(len(animals_list) / animals_per_page)

    # Create a list of page numbers for the page selector
    page_numbers_list = []
    for page_number in range(1, pages_total):
        page_numbers_list.append(page_number)

    # Display page selector and start on page 1
    # TODO: Make page selection functional
    ui.toggle(page_numbers_list, value=1)

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
