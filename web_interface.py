from flask import Flask, request
from adoptnv_core import search_for_animals

# Flask essentials
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return """
        <html>
            <body>
                <h1>AdoptNV Web Test</h1>
                <p><a href="/results">Click here to search</a> (and then wait a few seconds)</p>
            </body>
        </html>
    """

@app.route("/results")
def results():
    animals_list = search_for_animals()
    animals_string = ""

    for animal in animals_list:
        animals_string += f'<img src="{animal["Image"]}" width="100" height="100" alt="{animal["Name"]}"><br>'
        animals_string += f'Name: <strong>{animal["Name"]}</strong><br>'
        animals_string += f'Stray: {animal["Stray"]}<br>'
        animals_string += f'URL: <a href="{animal["URL"]}">{animal["URL"]}</a><br>'
        animals_string += f'Location: {animal["Location"]}<br>'
        animals_string += f'Sex: {animal["Sex"]}<br>'
        animals_string += f'ID: {animal["ID"]}<br>'
        animals_string += f'Fee: {animal["Fee"]}<br>'
        animals_string += "<hr>"

    return f"{animals_string}"
