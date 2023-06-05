import requests
from bs4 import BeautifulSoup
from homeassistant.helpers.entity import Entity

def check_offer_and_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check offer
    html_text = str(soup)
    if "promotion-labels" in html_text:
        offer = "Er is een actie"
    else:
        offer = "Er is geen actie"

    # Check price
    price_decimal = soup.find("div", class_="pricebadge__new-price-decimal").text.strip()
    price_fractional = soup.find("div", class_="pricebadge__new-price-fractional").text.strip()
    price = f"{price_decimal}.{price_fractional}"

    return offer, price

def setup_platform(hass, config, add_entities, discovery_info=None):
    url = config['url']
    name = config['name']
    offer, price = check_offer_and_price(url)
    add_entities([KruidvatOfferSensor(name, offer), KruidvatPriceSensor(name, price)])

class KruidvatOfferSensor(Entity):
    def __init__(self, name, offer):
        self._name = f"{name} Offer"
        self._state = offer

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

class KruidvatPriceSensor(Entity):
    def __init__(self, name, price):
        self._name = f"{name} Price"
        self._state = price

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state
