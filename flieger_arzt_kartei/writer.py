#!/usr/bin/env python3


import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

print(__package__)
env = Environment(
    loader=FileSystemLoader("./flieger_arzt_kartei/templates/"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")

with open('doctors.json') as f:
    doctors = json.load(f)
    federal_states = sorted({doctor['address']['federal_state'] for doctor in doctors})

with open('index.html', 'w') as f:
    f.write(template.render(doctors = doctors, federal_states=federal_states))
