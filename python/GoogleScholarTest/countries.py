import bs4
import csv
from dataclasses import dataclass, astuple
import requests

COUNTRIES_FILE = 'countries.csv'
RAW_DATA_SOURCE = 'https://countrycode.org/'


@dataclass
class Country:
    name: str
    country_code: str
    iso_code: str
    iso_code_long: str
    population: str = 'Unknown'
    area: str = 'Unknown'
    gdp: str = 'Unknown'
    scholar_status: str = 'Unknown'

    def __post_init__(self):
        if not self.name or not self.country_code or not self.iso_code or not self.iso_code_long:
            raise ValueError('Missing param for country.')

    def csv_items(self):
        return astuple(self)

    @property
    def scholar_url(self):
        return f'https://scholar.google.com.{self.iso_code}'


class Countries:
    def __init__(self):
        self.country_list = []

    def add_country(self, country):
        self.country_list.append(country)

    def save(self):
        with open(COUNTRIES_FILE, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"')
            writer.writerow(
                ['name', 'country_code', 'iso_code', 'iso_code_long', 'population', 'area', 'gdp', 'scholar_status'])
            for country in self.country_list:
                writer.writerow(country.csv_items())

    @staticmethod
    def load():
        countries = Countries()
        with open(COUNTRIES_FILE, newline='') as f:
            f.readline()  # Eat title row
            for row in csv.reader(f, delimiter=',', quotechar='"'):
                countries.add_country(Country(*row))
        return countries

    @staticmethod
    def load_from_html(file_name):
        countries = Countries()
        with open(file_name) as f:
            rows = bs4.BeautifulSoup(f.read(), 'html.parser').table.tbody.find_all('tr')
            for tr in rows:
                name, country_code, iso_code, population, area, gdp = tr.find_all('td')
                iso_code, iso_code_long = iso_code.text.split(' / ')
                countries.add_country(Country(
                    name=name.text,
                    country_code=country_code.text,
                    iso_code=iso_code.lower(),
                    iso_code_long=iso_code_long.lower(),
                    population=population.text.replace(',', ''),
                    area=area.text.replace(',', ''),
                    gdp=gdp.text.replace(',', '')
                ))
        return countries

    def reset_google_scholar_status(self, skip_unavailable=True):
        for country in self.country_list:
            if skip_unavailable and country.scholar_status == 'Unavailable': continue
            country.scholar_status = 'Unknown'

    def test_google_scholar(self, update_status=False, skip_unavailable=True, skip_known=False, verbose=False):
        try:
            for country in self.country_list:
                prefix = f'{country.name:40s} {country.scholar_url}'
                if (skip_known and country.scholar_status != 'Unknown') or \
                        (skip_unavailable and country.scholar_status == 'Unavailable'):
                    if verbose: print(f'{prefix}    skipped')
                    continue
                try:
                    r = requests.get(url=country.scholar_url)
                    status = str(r.status_code)
                except Exception:
                    status = 'Unavailable'
                print(f'{prefix}    {status}')
                if update_status: country.scholar_status = status
        except KeyboardInterrupt:
            print('Interrupted.')
        finally:
            if update_status:
                self.save()

    def show_available_scholar(self, only_status_200=True):
        for country in self.country_list:
            if country.scholar_status == 'Unavailable' or \
                    (only_status_200 and country.scholar_status != '200'):
                continue
            print(f'{country.name:40s} {country.scholar_url}    {country.scholar_status}')

    def __str__(self):
        return '\n'.join(map(str, self.country_list))

    def __getitem__(self, idx):
        return self.country_list[idx]


def run():
    countries = Countries.load()
    # countries.test_google_scholar(update_status=True, skip_known=True)
    countries.show_available_scholar()


if __name__ == '__main__':
    run()
