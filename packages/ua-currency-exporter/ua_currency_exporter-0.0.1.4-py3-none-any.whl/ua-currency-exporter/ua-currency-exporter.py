import time

from prometheus_client import start_http_server, Gauge
import requests
import json
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',filename='currency_exporter.log',filemode='w')

usd = Gauge("usd", "Number of stars for a GitHub repository", ["owner", "repo"])
eur = Gauge("eur", "Number of stars for a GitHub repository", ["owner", "repo"])

api_endpoint = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

def currency_rate(code):
    response = requests.get(api_endpoint)
    json_data = json.loads(response.text)
    for item in json_data:
        if item['cc'] == code:
            return (item['rate'])


usd_value = currency_rate('USD')
eur_value = currency_rate('EUR')
usd.labels("usd", "nbu").set(usd_value)
eur.labels("eur", "nbu").set(eur_value)
start_http_server(8000)

if __name__ == '__main__':
    while True:
        print("Server is running")
        currency_rate('USD')
        currency_rate('EUR')
        time.sleep(600)
        