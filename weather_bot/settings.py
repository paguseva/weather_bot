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

LOCATION_INQUIRY_MSG = emojize(
    "Let's setup your location! :earth_africa: \n\n"
    "You can either send your location or type the name of the nearest town.",
    use_aliases=True
)

CANCELLATION_MSG = emojize(
    'Looks like something went wrong. :worried:\n\nTry again later.',
    use_aliases=True
)

TIMEOUT_MSG = emojize(
    'Okay, no reply.\n\nAnyway, the time is up :alarm_clock:, but you can try again later.',
    use_aliases=True
)

INCORRECT_SEARCH_RESULT_MSG = emojize(
    'Sorry, looks like I could not find your location. :sweat: \n\n'
    'Try changing your query, it might have typos or be too specific.',
    use_aliases=True
)

LOCATION_NOT_SET_MSG = emojize(
    'Looks like your location is not set yet :eyes:.\n\nUse /set_location to set it',
    use_aliases=True
)

WEATHER_TEXT_MSG = emojize(
    'Weather status: {desc} {emoji}\n\n'
    'The temperature is {temp:.1f}°C, but it feels like {feel_temp:.1f}°C.\n'
    'The wind has speed of {wind_speed} m/s.\n\n'
    '{advice}',
    use_aliases=True
)

CURRENT_LOCATION_MSG = (
    'Your current location is {location}.'
)

LOCATION_SELECTION_MSG = (
    'Which one of the following locations is yours?'
)

CANCEL_SELECTION_MSG = (
    'Okay, try /set_location again and make you query a little bit more specific.'
)

NEW_LOCATION_COORDS_MSG = (
    'Your new location has latitude {lat} and longitude {lon}.'
)

NEW_LOCATION_PLACE_MSG = (
    '\n\nThis point is in {place}.'
)

ADVICE_TEMPLATE_MSG = (
    'My advice is to wear {clothes_type}.'
)

RAIN_WARNING = emojize(
    "\n\n:closed_umbrella: It is raining, so don't forget your umbrella.",
    use_aliases=True
)

DANGER_WARNING = emojize(
    '\n\n:warning: The weather seems dangerous. Consider staying home.',
    use_aliases=True
)

UV_WARNING = emojize(
    '\n\n:high_brightness: Note that UV index is high right now, hence it is highly recommended to use sunscreen.'
)

TEMP_ADVICE = [
    # (upper bound, advice)
    ( -15, 'an extra-thick insulatet puffer coat'),
    (   5, 'a thick winter coat or a puffer jacket'),
    (  13, 'a coat or a jacket with a sweater underneath'),
    (  21, 'a light jacket or a sweater'),
    (  30, 'light clothes like a t-shirt or a thin shirt with a pair of loose-fitted pants'),
    (None, 'extra light clothes like a tank top or a short-sleeved shirt, a pair of shorts or a skirt, and sandals'),
]

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

WEATHER_TO_EMOJI = {
    'Clear': emojize(':sunny:', use_aliases=True),
    'Snow': emojize(':snowflake:', use_aliases=True),
    'Clouds': {
        'few clouds': emojize(':partly_sunny:', use_aliases=True),
        'scattered clouds': emojize(u'\u26C5'),  # sun behind cloud
        'broken clouds': emojize(u'\U0001F325'),  # sun behind large cloud
        'overcast clouds': emojize(':cloud:', use_aliases=True)
    },
    'Rain': emojize(u'\U0001F327'),  # cloud with rain
    'Drizzle': emojize(':umbrella:', use_aliases=True),
    'Thunderstorm': emojize(u'\u26C8'),  # cloud with lightning and rain
    'Tornado': emojize(u'\U0001F32A'),  # tornado
}
