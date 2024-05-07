from flask import Flask, request
from adoptnv_core import animal_search

# Flask essentials
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    # result = flask_test()
    # return f"Well, Flask [still] works and provided a test result of: {result}"
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
    animals_list = animal_search()
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
