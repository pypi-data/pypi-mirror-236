"""pycountry"""

__version__ = "23.2.0"

import contextlib
import os.path
import unicodedata

from isocountry import db as data

try:
    import importlib_resources
except ModuleNotFoundError:
    from importlib import resources as importlib_resources


def resource_filename(package_or_requirement, resource_name):
    return str(importlib_resources.files(package_or_requirement) / resource_name)


LOCALES_DIR = resource_filename("isocountry", "locales")
DATABASE_DIR = resource_filename("isocountry", "databases")


def remove_accents(input_str):
    # Borrowed from https://stackoverflow.com/a/517974/1509718
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


class ExistingCountries(data.Database):
    """Provides access to an ISO 3166 database (Countries)."""

    data_class_name = "Country"
    root_key = "3166-1"

    def search_fuzzy(self, query):
        query = remove_accents(query.strip().lower())

        # A country-code to points mapping for later sorting countries
        # based on the query's matching incidence.
        results = {}

        def add_result(country, points):
            results.setdefault(country.alpha_2, 0)
            results[country.alpha_2] += points

        # Prio 1: exact matches on country names
        with contextlib.suppress(LookupError):
            add_result(self.lookup(query), 50)
        # Prio 2: exact matches on subdivision names
        for candidate in subdivisions:
            for v in candidate._fields.values():
                if v is None:
                    continue
                v = remove_accents(v.lower())
                # Some names include alternative versions which we want to
                # match exactly.
                for v in v.split(";"):
                    if v == query:
                        add_result(candidate.country, 49)
                        break

        # Prio 3: partial matches on country names
        for candidate in self:
            # Higher priority for a match on the common name
            for v in [
                candidate._fields.get("name"),
                candidate._fields.get("official_name"),
                candidate._fields.get("comment"),
            ]:
                if v is None:
                    continue
                v = remove_accents(v.lower())
                if query in v:
                    # This prefers countries with a match early in their name
                    # and also balances against countries with a number of
                    # partial matches and their name containing 'new' in the
                    # middle
                    add_result(candidate, max([5, 30 - (2 * v.find(query))]))
                    break

        # Prio 4: partial matches on subdivision names
        for candidate in subdivisions:
            v = candidate._fields.get("name")
            if v is None:
                continue
            v = remove_accents(v.lower())
            if query in v:
                add_result(candidate.country, max([1, 5 - v.find(query)]))

        if not results:
            raise LookupError(query)

        results = [
            self.get(alpha_2=x[0])
            # sort by points first, by alpha2 code second, and to ensure stable
            # results the negative value allows us to sort reversely on the
            # points but ascending on the country code.
            for x in sorted(results.items(), key=lambda x: (-x[1], x[0]))
        ]
        return results


class HistoricCountries(ExistingCountries):
    """Provides access to an ISO 3166-3 database
    (Countries that have been removed from the standard)."""

    data_class_name = "Country"
    root_key = "3166-3"


class Scripts(data.Database):
    """Provides access to an ISO 15924 database (Scripts)."""

    data_class_name = "Script"
    root_key = "15924"


class Currencies(data.Database):
    """Provides access to an ISO 4217 database (Currencies)."""

    data_class_name = "Currency"
    root_key = "4217"


class Languages(data.Database):
    """Provides access to an ISO 639-1/2T/3 database (Languages)."""

    no_index = ["status", "scope", "type", "inverted_name", "common_name"]
    data_class_name = "Language"
    root_key = "639-3"


class LanguageFamilies(data.Database):
    """Provides access to an ISO 639-5 database
    (Language Families and Groups)."""

    data_class_name = "LanguageFamily"
    root_key = "639-5"


class Subdivision(data.Data):
    def __init__(self, **kw):
        kw["parent_code"] = kw.get("parent", None)
        super().__init__(**kw)
        self.country_code = self.code.split("-")[0]
        if self.parent_code is not None:
            self.parent_code = f"{self.country_code}-{self.parent_code}"

    @property
    def country(self):
        return countries.get(alpha_2=self.country_code)

    @property
    def parent(self):
        return subdivisions.get(code=self.parent_code) if self.parent_code else None


class Subdivisions(data.Database):
    # Note: subdivisions can be hierarchical to other subdivisions. The
    # parent_code attribute is related to other subdivisons, *not*
    # the country!

    data_class_base = Subdivision
    data_class_name = "Subdivision"
    no_index = ["name", "parent_code", "parent", "type"]
    root_key = "3166-2"

    def _load(self, *args, **kw):
        super()._load(*args, **kw)

        # Add index for the country code.
        self.indices["country_code"] = {}
        for subdivision in self:
            divs = self.indices["country_code"].setdefault(
                subdivision.country_code.lower(), set()
            )
            divs.add(subdivision)

    def get(self, **kw):
        default = kw.setdefault("default", None)
        subdivisions = super().get(**kw)
        if (
            subdivisions is default
            and "country_code" in kw
            and countries.get(alpha_2=kw["country_code"]) is not None
        ):
            return []
        return subdivisions


countries = ExistingCountries(os.path.join(DATABASE_DIR, "iso3166-1.json"))
subdivisions = Subdivisions(os.path.join(DATABASE_DIR, "iso3166-2.json"))
historic_countries = HistoricCountries(os.path.join(DATABASE_DIR, "iso3166-3.json"))

currencies = Currencies(os.path.join(DATABASE_DIR, "iso4217.json"))

languages = Languages(os.path.join(DATABASE_DIR, "iso639-3.json"))
language_families = LanguageFamilies(os.path.join(DATABASE_DIR, "iso639-5.json"))

scripts = Scripts(os.path.join(DATABASE_DIR, "iso15924.json"))
