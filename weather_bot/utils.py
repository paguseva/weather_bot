import logging
import requests

from weather_bot.settings import (LOCIQ_TOKEN, OWA_TOKEN, FORWARD_ENCODING_NECESSARY_FIELDS,
                                    ADDRESS_CITY_SUBS, ADDRESS_COUNTRY_SUBS, DUPLICATE_MAX_DISTANCE)


logger = logging.getLogger(__name__)


def build_place_name(data):
    try:
        address = data['address']
    except KeyError:
        logging.warning(f'No address in geo response. {data}')
        return
    result = ''
    for field in ADDRESS_CITY_SUBS:
        if address.get(field) is not None:
            result += address[field] + ', '
            break
    if address.get('state') is not None:
        result += address['state'] + ', '
    for field in ADDRESS_COUNTRY_SUBS:
        if address.get(field) is not None:
            result += address[field]
            break
    if address.get('postcode') is not None:
        result += ' [{}]'.format(address['postcode'])
    return result


def sqr_distance(x_1, y_1, x_2, y_2):
    x_1, y_1 = float(x_1), float(y_1)
    x_2, y_2 = float(x_2), float(y_2)
    return (x_1 - x_2) ** 2 + (y_1 - y_2) ** 2


def remove_duplicates(data):
    results = []
    for entry in data:
        is_duplicate = False
        for existing_result in results:
            if sqr_distance(entry['lat'], entry['lon'],
                            existing_result['lat'], existing_result['lon']) < DUPLICATE_MAX_DISTANCE:
                is_duplicate = True
                break
        if not is_duplicate:
            results.append(entry)
    return results


def farenheit_to_celsius(T):
    return (T - 32) * 5 / 9


def kelvin_to_celsius(T):
    return T - 273.15


def get_place_from_coords(lat, long):
    data = {
        'key': LOCIQ_TOKEN,
        'lat': lat,
        'lon': long,
        'format': 'json',
        'normalizecity': 1,
    }
    response = requests.get('https://us1.locationiq.com/v1/reverse.php', params=data)
    if response.status_code != 200:
        logger.warning(
            'Something is wrong with reverse geocoding. '
            'Got status code {} with input ({}, {})'.format(
                response.status_code, lat, long
            )
        )
        return
    return build_place_name(response.json())


def get_places_from_text(query):
    data = {
        'key': LOCIQ_TOKEN,
        'limit': 5,
        'format': 'json',
        'addressdetails': 1,
        'normalizecity': 1,
        'q': query,
    }
    response = requests.get('https://us1.locationiq.com/v1/search.php', params=data)
    if response.status_code != 200:
        logger.warning(
            'Something is wrong with forward geocoding. '
            'Got status code {} with input ({})'.format(
                response.status_code, query
            )
        )
        return
    raw_results = response.json()
    results = []
    for result in raw_results:
        trimmed_result = dict()
        for field in FORWARD_ENCODING_NECESSARY_FIELDS:
            if result.get(field) is None:
                continue
            trimmed_result[field] = (result[field] if field != 'address' else build_place_name(result))
        results.append(trimmed_result)
    return remove_duplicates(results)


def current_weather_for_coords(lat, long):
    data = {
        'lat': lat,
        'lon': long,
        'appid': OWA_TOKEN,
    }
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=data)
    if response.status_code != 200:
        logger.warning(
            'Something is wrong with weather API. '
            'Got status code {} for input ({}, {})'.format(
                response.status_code, lat, long
            )
        )
        return
    return response.json()
