#!/usr/bin/env python3
import math
from adoptnv import build_results
from nicegui import ui
import shelters


def include_page_top():
    """Shared among all pages and includes header text."""

    with ui.header(elevated=True).style("background-color: #3d3d3d").classes("items-center justify-between"):
        ui.link("AdoptNV", "/")


def include_page_bottom():
    """Shared among all pages and includes footer."""

    with ui.footer().style("background-color: #6c6c6c"):
        ui.label("AdoptNV uses Python, NiceGUI, BeautifulSoup. Not affiliated with any animal shelter.")


@ui.page("/")
def index_page():
    include_page_top()

    ui.label("Welcome to AdoptNV. :-)")

    animal_foundation = shelters.AnimalFoundation()
    available_filters = animal_foundation.get_filters()


    with ui.row().classes('w-full'):
        for filter in available_filters:
            # filter[0] is the filter key/category, and filter[1] is a list of the possible values for it.
            with ui.dropdown_button(filter[0], auto_close=True):
                for filter_value in filter[1]:
                    # https://github.com/zauberzeug/nicegui/wiki/FAQs#why-do-all-my-elements-have-the-same-value
                    ui.item(filter_value, on_click=lambda selected_value=filter_value: ui.notify(f"{selected_value}"))

    ui.label("Filter options are currently just for show, but the search button works:")
    ui.button("Click here to find a pet pal", on_click=lambda: ui.navigate.to(find_pets_page))

    include_page_bottom()


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
        display_results(pet_results, 1)

    include_page_bottom()


@ui.refreshable
def display_results(pets_list, selected_page=1):
    pets_per_page = 10

    # Divides number of animals by how many animals per page, then rounds it up to nearest int.
    pages_total = math.ceil(len(pets_list) / pets_per_page)

    # Create a list of page numbers for the page selector
    page_numbers = []
    for page in range(1, pages_total):
        page_numbers.append(page)

    # Display page selector above results
    with ui.select(page_numbers, value=selected_page, label="Page").classes('w-20') as page_selector:
        page_selector.on_value_change(lambda: display_results.refresh(pets_list, page_selector.value))

    # Count pets as we display them on the page, so we know when to stop
    pets_on_page = 0

    # Skip pets that should be on previous pages
    starting_from = selected_page * 10

    # Begin iterating and printing pets. Uses list slicing to skip pets from previous pages
    for animal in pets_list[starting_from:]:
        if pets_on_page < pets_per_page:
            pets_on_page += 1

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


ui.run(reload=False, title="AdoptNV :: Find pets in Nevada!", dark=True)
