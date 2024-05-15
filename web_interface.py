from nicegui import ui
from adoptnv_core import search_for_animals


@ui.page("/")
def index():
    ui.label("AdoptNV Web Test - now using NiceGUI")
    ui.link("Click here to search", results)

    ui.run()


@ui.page("/results")
def results():
    animals_list = search_for_animals()

    for animal in animals_list:
        with ui.link(target=animal["URL"]):
            with ui.image(animal["Image"]).classes("w-64"):
                ui.label(animal["Name"]).classes("absolute-bottom text-subtitle2 text-center")
        ui.label(f"Stray: {animal["Stray"]}")
        ui.label(f"Location: {animal["Location"]}")
        ui.label(f"Sex: {animal["Sex"]}")
        ui.label(f"ID: {animal["ID"]}")
        ui.label(f"Fee: {animal["Fee"]}")


index()
