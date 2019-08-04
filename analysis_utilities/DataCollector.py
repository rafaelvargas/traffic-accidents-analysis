import requests
import os
import sys


class DataCollector:
    def __init__(self):
        self.create_data_directory()
        self.accidents_data_urls = self.collect_accidents_data_urls()

    def create_data_directory(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def collect_accidents_data_urls(self):
        package_url = "https://ckan-hom.procempa.com.br/api/3/action/package_show?id=099a3d7d-dbbe-4d72-9094-d51825b21f30"
        response = requests.get(package_url)
        urls = []
        for resource in response.json()["result"]["resources"]:
            if "csv" in resource["mimetype"]:
                urls.append(resource["url"])
        return urls

    def collect_accidents_data(self):
        for url in self.accidents_data_urls:
            year = url[-8:-4]
            print("Downloading {} data.".format(year))
            if not os.path.isfile("data/" + year + ".csv"):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    with open(
                        "data/" + year + ".csv", "w", encoding="utf-8"
                    ) as csv_file:
                        csv_file.write(response.text)
                except requests.exceptions.HTTPError as error:
                    print(error)
                    sys.exit(1)

    def collect_fuel_sale_data(self, first_year, last_year):
        for year in range(first_year, last_year + 1):
            diesel_url = (
                "http://dados.fee.tche.br/ckan-download/fee-"
                + str(year)
                + "-mun-vendas-de-combustiveis-oleo-diesel-102126.csv"
            )
            gasoline_url = (
                "http://dados.fee.tche.br/ckan-download/fee-"
                + str(year)
                + "-mun-vendas-de-combustiveis-gasolina-automotiva-102424.csv"
            )
            alcohol_url = (
                "http://dados.fee.tche.br/ckan-download/fee-"
                + str(year)
                + "-mun-vendas-de-combustiveis-alcool-hidratado-102422.csv"
            )
            try:
                diesel_response = requests.get(diesel_url)
                gasoline_response = requests.get(gasoline_url)
                # alcohol_response = request.get(alcohol_url)
                with open("data/diesel-sale-" + str(year) + ".csv", "wb") as csv_file:
                    csv_file.write(diesel_response.content)
            except:
                sys.exit(1)

    def collect_vehicles_data():
        pass
