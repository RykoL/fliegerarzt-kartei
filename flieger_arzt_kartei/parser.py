#!/usr/bin/env python3
import bs4

from .doctor import Doctor, Address, FederalState
from typing import List

def get_doctors_from_page(page) -> List[Doctor]:
    content_table = page.content.select_one("table:nth-of-type(2)")
    doctors = []
    for row in content_table.children:

        if type(row) is bs4.element.NavigableString:
            continue

        if is_header_row(row):
            continue

        doctors.append(parse_doctor(row))

    return doctors

def parse_doctor(row):
    name = row.contents[1].string.get_text(strip=True)
    address = parse_address(row)
    telefon = row.contents[5].string
    return Doctor(name, telefon, address)


def parse_address(row) -> Address:
    street, _zip, city = [address_part.string.get_text(strip=True) for address_part in row.contents[3].find_all('font')]
    federal_state = row.contents[7].string
    return Address(street, _zip, city, FederalState(federal_state))


def is_header_row(row) -> bool:
    return any([col.string == 'Name' for col in row.children])
