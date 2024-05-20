#!/usr/bin/env python3
import requests
import re
import json

from .parser import get_doctors_from_page

from bs4 import BeautifulSoup
from dataclasses import dataclass


base_url = "http://www2.lba.de/webdb/showtab.jsp?table=flareg"
next_url = "http://www2.lba.de/webdb/showtab.jsp?table=flareg&position=next"
position_regex = re.compile(r"(?P<lower>\d+) - (?P<upper>\d+) \/ (?P<total>\d+)")


@dataclass
class Cursor:

    lower: int
    upper: int
    total: int

    def is_end(self):
        return self.upper == self.total


@dataclass
class Page:

    cursor: Cursor
    content: BeautifulSoup


def get_cursor(soup) -> Cursor:
    texts = list(map(lambda e: e.get_text(strip=True) ,soup.find_all("font")))
    position = position_regex.match([text for text in texts if position_regex.match(text)][0])

    total = int(position.group("total"))
    lower = int(position.group("lower"))
    upper = int(position.group("upper"))

    return Cursor(lower, upper, total)


def make_initial_request(session) -> Page:
    resp = session.get(base_url)
    return get_page(resp)


def get_page(resp) -> Page:
    soup = BeautifulSoup(resp.content, "html.parser")
    cursor = get_cursor(soup)

    return Page(cursor, soup)


def get_pages():
    session = requests.Session()
    pages = [make_initial_request(session)]

    while True:

        page = get_page(session.get(next_url))
        pages.append(page)

        if page.cursor.is_end():
            break

    return pages


def main():
    pages = get_pages()

    doctors = []
    for page in pages:
        doctors.extend([doctor.to_json() for doctor in get_doctors_from_page(page)])

    with open('doctors.json', 'w', encoding='utf8') as f:
        json.dump(doctors, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
