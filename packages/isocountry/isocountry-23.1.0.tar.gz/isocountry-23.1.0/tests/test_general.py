import re

import pytest

import isocountry
from isocountry import db


@pytest.fixture(autouse=True, scope="session")
def logging():
    import logging

    logging.basicConfig(level=logging.DEBUG)


def test_country_list():
    assert len(isocountry.countries) == 249
    assert isinstance(list(isocountry.countries)[0], db.Data)


def test_country_fuzzy_search():
    results = fuzz("England", 1, "GB")
    results = fuzz("Sint Maarten", 2, "NL")
    assert results[1] == isocountry.countries.get(alpha_2="SX")

    results = fuzz("Cote", 3, "CI")
    assert results[1] == isocountry.countries.get(alpha_2="FR")
    assert results[2] == isocountry.countries.get(alpha_2="HN")

    # A somewhat carefully balanced point system allows for a (bias-based)
    # graceful sorting of common substrings being used in multiple matches:
    results = isocountry.countries.search_fuzzy("New")
    assert results[0] == isocountry.countries.get(alpha_2="NC")
    assert results[1] == isocountry.countries.get(alpha_2="NZ")
    assert results[2] == isocountry.countries.get(alpha_2="PG")
    assert results[3] == isocountry.countries.get(alpha_2="GB")
    assert results[4] == isocountry.countries.get(alpha_2="US")
    assert results[5] == isocountry.countries.get(alpha_2="CA")
    assert results[6] == isocountry.countries.get(alpha_2="AU")
    assert results[7] == isocountry.countries.get(alpha_2="BS")
    assert results[8] == isocountry.countries.get(alpha_2="TW")
    assert results[9] == isocountry.countries.get(alpha_2="MH")

    results = fuzz("united states of america", 1, "US")


def fuzz(country, num, alpha_2):
    result = isocountry.countries.search_fuzzy(country)
    assert len(result) == num
    assert result[0] == isocountry.countries.get(alpha_2=alpha_2)

    return result


def test_historic_country_fuzzy_search():
    results = isocountry.historic_countries.search_fuzzy("burma")
    assert len(results) == 1
    assert results[0] == isocountry.historic_countries.get(alpha_4="BUMM")


def test_germany_has_all_attributes():
    germany = isocountry.countries.get(alpha_2="DE")
    assert germany.alpha_2 == "DE"
    assert germany.alpha_3 == "DEU"
    assert germany.numeric == "276"
    assert germany.name == "Germany"
    assert germany.official_name == "Federal Republic of Germany"


def test_subdivisions_directly_accessible():
    assert len(isocountry.subdivisions) == 5127
    assert isinstance(list(isocountry.subdivisions)[0], db.Data)

    de_st = isocountry.subdivisions.get(code="DE-ST")
    assert de_st.code == "DE-ST"
    assert de_st.name == "Sachsen-Anhalt"
    assert de_st.type == "Land"
    assert de_st.parent is None
    assert de_st.parent_code is None
    assert de_st.country is isocountry.countries.get(alpha_2="DE")


def test_subdivisions_have_subdivision_as_parent():
    fr_01 = isocountry.subdivisions.get(code="FR-01")
    assert fr_01.code == "FR-01"
    assert fr_01.name == "Ain"
    assert fr_01.type == "Metropolitan department"
    assert fr_01.parent_code == "FR-ARA"
    assert fr_01.parent is isocountry.subdivisions.get(code="FR-ARA")
    assert fr_01.parent.name == "Auvergne-Rhône-Alpes"


def test_query_subdivisions_of_country():
    assert len(isocountry.subdivisions.get(country_code="DE")) == 16
    assert len(isocountry.subdivisions.get(country_code="US")) == 57


def test_scripts():
    assert len(isocountry.scripts) == 182
    assert isinstance(list(isocountry.scripts)[0], db.Data)

    latin = isocountry.scripts.get(name="Latin")
    assert latin.alpha_4 == "Latn"
    assert latin.name == "Latin"
    assert latin.numeric == "215"


def test_currencies():
    assert len(isocountry.currencies) == 181
    assert isinstance(list(isocountry.currencies)[0], db.Data)

    argentine_peso = isocountry.currencies.get(alpha_3="ARS")
    assert argentine_peso.alpha_3 == "ARS"
    assert argentine_peso.name == "Argentine Peso"
    assert argentine_peso.numeric == "032"


def test_languages():
    assert len(isocountry.languages) == 7910
    assert isinstance(list(isocountry.languages)[0], db.Data)

    aragonese = isocountry.languages.get(alpha_2="an")
    assert aragonese.alpha_2 == "an"
    assert aragonese.alpha_3 == "arg"
    assert aragonese.name == "Aragonese"

    bengali = isocountry.languages.get(alpha_2="bn")
    assert bengali.name == "Bengali"
    assert bengali.common_name == "Bangla"

    # this tests the slow search path in lookup()
    bengali2 = isocountry.languages.lookup("bAngLa")
    assert bengali2 == bengali


def test_language_families():
    assert len(isocountry.language_families) == 115
    assert isinstance(list(isocountry.language_families)[0], db.Data)

    aragonese = isocountry.languages.get(alpha_3="arg")
    assert aragonese.alpha_3 == "arg"
    assert aragonese.name == "Aragonese"


def test_removed_countries():
    ussr = isocountry.historic_countries.get(alpha_3="SUN")
    assert isinstance(ussr, db.Data)
    assert ussr.alpha_4 == "SUHH"
    assert ussr.alpha_3 == "SUN"
    assert ussr.name == "USSR, Union of Soviet Socialist Republics"
    assert ussr.withdrawal_date == "1992-08-30"


def test_repr():
    assert re.match(
        "Country\\(alpha_2=u?'DE', "
        "alpha_3=u?'DEU', "
        "flag='..', "
        "name=u?'Germany', "
        "numeric=u?'276', "
        "official_name=u?'Federal Republic of Germany'\\)",
        repr(isocountry.countries.get(alpha_2="DE")),
    )


def test_dir():
    germany = isocountry.countries.get(alpha_2="DE")
    for n in "alpha_2", "alpha_3", "name", "numeric", "official_name":
        assert n in dir(germany)


def test_get():
    c = isocountry.countries
    with pytest.raises(TypeError):
        c.get(alpha_2="DE", alpha_3="DEU")
    assert c.get(alpha_2="DE") == c.get(alpha_3="DEU")
    assert c.get(alpha_2="Foo") is None
    tracer = object()
    assert c.get(alpha_2="Foo", default=tracer) is tracer


def test_lookup():
    c = isocountry.countries
    g = c.get(alpha_2="DE")
    assert g == c.get(alpha_2="de")
    assert g == c.lookup("de")
    assert g == c.lookup("DEU")
    assert g == c.lookup("276")
    assert g == c.lookup("germany")
    assert g == c.lookup("Federal Republic of Germany")
    # try a generated field
    bqaq = isocountry.historic_countries.get(alpha_4="BQAQ")
    assert bqaq == isocountry.historic_countries.lookup("atb")
    german = isocountry.languages.get(alpha_2="de")
    assert german == isocountry.languages.lookup("De")
    euro = isocountry.currencies.get(alpha_3="EUR")
    assert euro == isocountry.currencies.lookup("euro")
    latin = isocountry.scripts.get(name="Latin")
    assert latin == isocountry.scripts.lookup("latn")
    fr_ara = isocountry.subdivisions.get(code="FR-ARA")
    assert fr_ara == isocountry.subdivisions.lookup("fr-ara")
    with pytest.raises(LookupError):
        isocountry.countries.lookup("bogus country")
    with pytest.raises(LookupError):
        isocountry.countries.lookup(12345)
    with pytest.raises(LookupError):
        isocountry.countries.get(alpha_2=12345)


def test_subdivision_parent():
    s = isocountry.subdivisions
    sd = s.get(code="CV-BV")
    assert sd.parent_code == "CV-B"
    assert sd.parent is s.get(code=sd.parent_code)


def test_subdivision_missing_code_raises_keyerror():
    s = isocountry.subdivisions
    assert s.get(code="US-ZZ") is None


def test_subdivision_empty_list():
    s = isocountry.subdivisions
    assert len(s.get(country_code="DE")) == 16
    assert len(s.get(country_code="JE")) == 0
    assert s.get(country_code="FOOBAR") is None
