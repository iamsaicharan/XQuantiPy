from pathlib import Path

with open("utils/templates/styles.css") as file:
    data = file.read()

styling = "<style>" + data + "</style>"
