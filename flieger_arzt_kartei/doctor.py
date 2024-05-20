#!/usr/bin/env python3


from dataclasses import dataclass
import logging


class FederalState:

    _name_map = {
        'BW': 'Baden-Württemberg',
        'HE': 'Hessen',
        'RP': 'Rheinland Pfalz',
        'BY': 'Bayern',
        'SN': 'Sachsen',
        'TH': 'Thüringen',
        'NW': 'Nordrhein-Westfalen',
        'NI': 'Niedersachsen',
        'SL': 'Saarland',
        'SH': 'Schleswig-Holstein',
        'MV': 'Mecklenburg-Vorpommern',
        'HH': 'Hamburg',
        'ST': 'Sachsen-Anhalt',
        'BB': 'Brandeburg',
        'BE': 'Berlin',
        'HB': 'Bremen'
    }

    @property
    def name(self):
        if self.short_name not in self._name_map:
            logging.warning(f"{self.short_name} is not a federal state")
        return self._name_map.get(self.short_name, self.short_name)

    def __init__(self, short_name):
        self.short_name = short_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


@dataclass
class Address:
    street: str
    zip: str
    city: str
    federal_state: FederalState

    def to_json(self):
        return {
            'city': self.city,
            'street': self.street,
            'zip': self.zip,
            'federal_state': self.federal_state.name
        }


@dataclass
class Doctor:
    name: str
    telefon: str
    address: Address

    def to_json(self):
        return {
            'name': self.name,
            'telefon': self.telefon,
            'address': self.address.to_json()
        }
