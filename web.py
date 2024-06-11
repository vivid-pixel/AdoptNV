#!/usr/bin/env python3
import math
from adoptnv import results_io
from nicegui import ui
import shelters


def include_page_top():
    """Shared among all pages and includes header text."""

    with ui.header(elevated=True).style("background-color: #2a2a2a").classes("items-center justify-between"):
        with ui.row().classes("w-full"):
            ui.link("AdoptNV", "/")
            ui.label("Your pet companion awaits you")


def include_page_bottom():
    """Shared among all pages and includes footer."""

    with ui.footer().style("background-color: #1f1f1f"):
        with ui.row():
            ui.markdown("AdoptNV uses [Python 3](https://www.python.org/), "
                        "[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), "
                        "and [NiceGUI](https://nicegui.io/). "
                        "This application has no affiliation with any shelters.")


@ui.page("/")
def index_page():
    include_page_top()

    animal_foundation = shelters.AnimalFoundation()
    available_filters = animal_foundation.get_filter_options()

    with ui.row().classes("w-full"):
        for category in available_filters:
            with ui.dropdown_button(category, auto_close=True):
                # https://github.com/zauberzeug/nicegui/wiki/FAQs#why-do-all-my-elements-have-the-same-value
                for option in available_filters[category]:
                    ui.item(option, on_click=lambda filter_category=category, filter_option=option: ui
                            .notify(f'You clicked "{filter_option}" from category "{filter_category}"'))

    ui.label("Filter options are currently just for show, but the search button works:")
    ui.link("Find a pet pal!", pets_page)

    include_page_bottom()


@ui.page('/pets')
async def pets_page():
    include_page_top()
    # spinner = ui.spinner(size="lg")
    results_io()
    # await ui.context.client.connected()
    # spinner.visible = False

    @ui.refreshable
    def show_results(selected_page=1):
        pets_list = shelters.Results.get_pets()
        return_flags = shelters.Results.get_flags()

        with ui.row():
            # Check return flags to create tailored greeting
            # FLAGS: first_run == cache file empty; cache_discarded == file too old; exception: unrecoverable error
            if return_flags["exception"] is not None:
                # Don't try to print the list if we had an unrecoverable exception.
                ui.label(return_flags["exception"])
            elif return_flags["first_run"]:
                ui.label("Here are some potential matches: ")
            elif return_flags["cache_discarded"]:
                ui.label("Welcome back! You've searched for animals previously, but I'll fetch you some fresh results.")
            else:
                ui.label("I see you've performed a recent search, so I'll restore those results from the cache.")

        # Set per-page limit for number of pets to display
        pets_per_page = 10

        # Divides number of animals by how many animals per page, then rounds it up to nearest int.
        pages_total = math.ceil(len(pets_list) / pets_per_page)

        # Create a list of page numbers for the page selector
        page_numbers = []
        for this_page in range(1, pages_total):
            page_numbers.append(this_page)

        # Display page selector above results
        with ui.select(page_numbers, value=selected_page, label="Page").classes('w-20') as page_selector:
            page_selector.on_value_change(lambda: show_results.refresh(page_selector.value))

        # Begin iterating and printing pets. Uses list slicing to skip pets from previous pages
        with ui.row().classes('w-full'):
            # Count pets as we display them on the page, so we know when to stop
            pets_on_page = 0

            # Skip pets that should be on previous pages
            starting_from = selected_page * 10
            for animal in pets_list[starting_from:]:
                if pets_on_page < pets_per_page:
                    pets_on_page += 1

                    with ui.card():
                        # The clickable picture of the pet, along with its name
                        with ui.link(target=animal["URL"]):
                            with ui.image(animal["Image"]).classes("w-64"):
                                ui.label(animal["Name"]).classes("absolute-bottom text-subtitle2 text-center")
                        # The rest of the pet's attributes
                        with ui.card_section():
                            ui.label(f"Stray: {animal["Stray"]}")
                            ui.label(f"Location: {animal["Location"]}")
                            ui.label(f"Sex: {animal["Sex"]}")
                            ui.label(f"ID: {animal["ID"]}")
                            ui.label(f"Fee: {animal["Fee"]}")

    include_page_bottom()

    return show_results()


ui.run(reload=False, title="AdoptNV :: Find pets in Nevada!", dark=True)
