from os import getenv

from emoji import emojize


TG_TOKEN = getenv('TG_TOKEN')
LOCIQ_TOKEN = getenv('LOCIQ_TOKEN')
OWA_TOKEN = getenv('OWA_TOKEN')

MODE = getenv('MODE', 'DEBUG')
PORT = int(getenv('PORT', '8443'))
HEROKU_APP_NAME = getenv('APP_NAME')

DB_CONF = {
    'host': getenv('DB_HOST'),
    'user': getenv('DB_USERNAME'),
    'password': getenv('DB_PASSWORD'),
    'port': getenv('DB_PORT'),
    'database': getenv('DB_DATABASE'),
}

REPLY_TIMEOUT = 10 * 60  # seconds
DUPLICATE_MAX_DISTANCE = 2

LOCATION_INQUIRY = emojize(
    "Let's setup your location! :earth_africa: \n\n"
    "You can either send your location or type the name of the nearest town.",
    use_aliases=True
)

CANCELLATION_TEXT = emojize(
    'Looks like something went wrong. :worried:\n\nTry again later.',
    use_aliases=True
)

TIMEOUT_TEXT = emojize(
    'Okay, no reply.\n\nAnyway, the time is up :alarm_clock:, but you can try again later.',
    use_aliases=True
)

INCORRECT_SEARCH_RESULT_TEXT = emojize(
    'Sorry, looks like I could not find your location. :sweat: \n\n'
    'Try changing your query, it might have typos or be too specific.',
    use_aliases=True
)

LOCATION_NOT_SET_TEXT = emojize(
    'Looks like your location is not set yet :eyes:.\n\nUse /set_location to set it',
    use_aliases=True
)

FORWARD_ENCODING_NECESSARY_FIELDS = [
    'address',
    'lat',
    'lon',
]

ADDRESS_DISPLAY_FIELDS = [
    'village',
    'suburb',
    'city',
    'town',
    'city_level',
    'county',
    'country',
]

ADDRESS_CITY_SUBS = [
    'city',
    'city_district',
    'locality',
    'town',
    'borough',
    'municipality',
    'village',
    'hamlet',
    'quarter',
    'neighbourhood',
]

ADDRESS_COUNTRY_SUBS = [
    'country',
    'name',
]
