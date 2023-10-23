# Isocountry

<p align="center">
<a href="https://github.com/yezz123/isocountry/actions/workflows/ci.yaml" target="_blank">
    <img src="https://github.com/yezz123/isocountry/actions/workflows/ci.yaml/badge.svg" alt="CI">
</a>
<a href="https://pypi.org/project/isocountry" target="_blank">
    <img src="https://img.shields.io/pypi/v/isocountry?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://codecov.io/gh/yezz123/isocountry">
    <img src="https://codecov.io/gh/yezz123/isocountry/branch/main/graph/badge.svg"/>
</a>
<a href="https://pepy.tech/project/isocountry" target="_blank">
    <img src="https://static.pepy.tech/badge/isocountry" alt="stats">
</a>
</p>
</p>


## ⛔️⛔️ pycountry Hard Fork

This is a hard fork of the `pycountry` library, which we've undertaken due to the lack of active maintenance in the original repository. The purpose of this fork is to ensure the continued functionality and support of `pycountry` within the [Pydantic-extra-types](https://github.com/pydantic/pydantic-extra-types) project. Our goals include maintaining, bug fixing, enhancing, and seamlessly integrating this fork into the Pydantic ecosystem. Your contributions and support are appreciated as we strive to keep this vital resource alive and thriving.

## Features

Isocountry provides the ISO databases for the standards:

* [639-3](https://en.wikipedia.org/wiki/ISO_639-3) -  Languages
* [3166](https://en.wikipedia.org/wiki/ISO_3166) - Countries
* [3166-3](https://en.wikipedia.org/wiki/ISO_3166-3) - Deleted countries
* [3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) - Subdivisions of countries
* [4217](https://en.wikipedia.org/wiki/ISO_4217) - Currencies
* [15924](https://en.wikipedia.org/wiki/ISO_15924) - Scripts

The package includes a copy from Debian's [pkg-isocodes](https://salsa.debian.org/iso-codes-team/iso-codes) and makes the data
accessible through a Python API.

Translation files for the various strings are included as well.

### Data update policy

No changes to the data will be accepted into isocountry. This is a pure wrapper
around the ISO standard using the `pkg-isocodes` database from Debian *as is*.
If you need changes to the political situation in the world, please talk to
the ISO or Debian people, not me.

#### Countries (ISO 3166-1)

Countries are accessible through a database object that is already configured
upon import of isocountry and works as an iterable:

```py

  >>> import isocountry
  >>> len(isocountry.countries)
  249
  >>> list(isocountry.countries)[0]
  Country(alpha_2='AF', alpha_3='AFG', name='Afghanistan', numeric='004', official_name='Islamic Republic of Afghanistan')
```

Specific countries can be looked up by their various codes and provide the
information included in the standard as attributes:

```py

  >>> germany = isocountry.countries.get(alpha_2='DE')
  >>> germany
  Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276', official_name='Federal Republic of Germany')
  >>> germany.alpha_2
  'DE'
  >>> germany.alpha_3
  'DEU'
  >>> germany.numeric
  '276'
  >>> germany.name
  'Germany'
  >>> germany.official_name
  'Federal Republic of Germany'
```

There's also a "fuzzy" search to help people discover "proper" countries for
names that might only actually be subdivisions. The fuzziness also includes
normalizing unicode accents. There's also a bit of prioritization included
to prefer matches on country names before subdivision names and have countries
with more matches be listed before ones with fewer matches:

```py
  >>> isocountry.countries.search_fuzzy('England')
  [Country(alpha_2='GB', alpha_3='GBR', name='United Kingdom', numeric='826', official_name='United Kingdom of Great Britain and Northern Ireland')]

  >>> isocountry.countries.search_fuzzy('Cote')
  [Country(alpha_2='CI', alpha_3='CIV', name="Côte d'Ivoire", numeric='384', official_name="Republic of Côte d'Ivoire"),
   Country(alpha_2='FR', alpha_3='FRA', name='France', numeric='250', official_name='French Republic'),
   Country(alpha_2='HN', alpha_3='HND', name='Honduras', numeric='340', official_name='Republic of Honduras')]
```

#### Historic Countries (ISO 3166-3)

The `historic_countries` database contains former countries that have been
removed from the standard and are now included in ISO 3166-3, excluding
existing ones:

```py

 >>> ussr = isocountry.historic_countries.get(alpha_3='SUN')
 >>> ussr
 Country(alpha_3='SUN', alpha_4='SUHH', withdrawal_date='1992-08-30', name='USSR, Union of Soviet Socialist Republics', numeric='810')
 >>> ussr.alpha_4
 'SUHH'
 >>> ussr.alpha_3
 'SUN'
 >>> ussr.name
 'USSR, Union of Soviet Socialist Republics'
 >>> ussr.withdrawal_date
 '1992-08-30'
```

#### Country subdivisions (ISO 3166-2)

The country subdivisions are a little more complex than the countries itself
because they provide a nested and typed structure.

All subdivisons can be accessed directly:

```py
  >>> len(isocountry.subdivisions)
  4847
  >>> list(isocountry.subdivisions)[0]
  Subdivision(code='AD-07', country_code='AD', name='Andorra la Vella', parent_code=None, type='Parish')
```

Subdivisions can be accessed using their unique code and provide at least
their code, name and type:

```py
  >>> de_st = isocountry.subdivisions.get(code='DE-ST')
  >>> de_st.code
  'DE-ST'
  >>> de_st.name
  'Sachsen-Anhalt'
  >>> de_st.type
  'State'
  >>> de_st.country
  Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276', official_name='Federal Republic of Germany')
```

Some subdivisions specify another subdivision as a parent:

```py
  >>> al_br = isocountry.subdivisions.get(code='AL-BU')
  >>> al_br.code
  'AL-BU'
  >>> al_br.name
  'Bulqiz\xeb'
  >>> al_br.type
  'District'
  >>> al_br.parent_code
  'AL-09'
  >>> al_br.parent
  Subdivision(code='AL-09', country_code='AL', name='Dib\xebr', parent_code=None, type='County')
  >>> al_br.parent.name
  'Dib\xebr'
```

The divisions of a single country can be queried using the country_code index:

```py
  >>> len(isocountry.subdivisions.get(country_code='DE'))
  16

  >>> len(isocountry.subdivisions.get(country_code='US'))
  57
```

#### Scripts (ISO 15924)

Scripts are available from a database similar to the countries:

```py
  >>> len(isocountry.scripts)
  169
  >>> list(isocountry.scripts)[0]
  Script(alpha_4='Afak', name='Afaka', numeric='439')

  >>> latin = isocountry.scripts.get(name='Latin')
  >>> latin
  Script(alpha_4='Latn', name='Latin', numeric='215')
  >>> latin.alpha4
  'Latn'
  >>> latin.name
  'Latin'
  >>> latin.numeric
  '215'
```

#### Currencies (ISO 4217)

The currencies database is, again, similar to the ones before:

```py
  >>> len(isocountry.currencies)
  182
  >>> list(isocountry.currencies)[0]
  Currency(alpha_3='AED', name='UAE Dirham', numeric='784')
  >>> argentine_peso = isocountry.currencies.get(alpha_3='ARS')
  >>> argentine_peso
  Currency(alpha_3='ARS', name='Argentine Peso', numeric='032')
  >>> argentine_peso.alpha_3
  'ARS'
  >>> argentine_peso.name
  'Argentine Peso'
  >>> argentine_peso.numeric
  '032'
```

#### Languages (ISO 639-3)

The languages database is similar too:

```py
  >>> len(isocountry.languages)
  7874
  >>> list(isocountry.languages)[0]
  Language(alpha_3='aaa', name='Ghotuo', scope='I', type='L')

  >>> aragonese = isocountry.languages.get(alpha_2='an')
  >>> aragonese.alpha_2
  'an'
  >>> aragonese.alpha_3
  'arg'
  >>> aragonese.name
  'Aragonese'

  >>> bengali = isocountry.languages.get(alpha_2='bn')
  >>> bengali.name
  'Bengali'
  >>> bengali.common_name
  'Bangla'
```

#### Locales

Locales are available in the `isocountry.LOCALES_DIR` subdirectory of this
package. The translation domains are called `isoXXX` according to the standard
they provide translations for. The directory is structured in a way compatible
to Python's gettext module.

Here is an example translating language names:

```py
  >>> import gettext
  >>> german = gettext.translation('iso3166-1', isocountry.LOCALES_DIR,
  ...                              languages=['de'])
  >>> german.install()
  >>> _('Germany')
  'Deutschland'
```

#### Lookups

For each database (countries, languages, scripts, etc.), you can also look up
entities case insensitively without knowing which key the value may match.  For
example:

```py
  >>> isocountry.countries.lookup('de')
 (isocountry.db.Country object at 0x...>
```

The search ends with the first match, which is returned.

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
# Install dependencies
pip install -e .[test,lint]
```

### Run tests 🌝

You can run all the tests with:

```bash
bash scripts/tests.sh
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
bash scripts/format.sh
```
