from enum import Enum, auto
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler,
                            Filters, CallbackQueryHandler)

from weather_bot.db import Database
import weather_bot.settings as settings
from weather_bot.utils import (get_place_from_coords, get_places_from_text,
                                current_weather_for_coords, kelvin_to_celsius)


logger = logging.getLogger(__name__)


class UserData(Enum):
    POSSIBLE_LOCATIONS = auto()


class Status(Enum):
    WAITING_FOR_LOCATION = auto()
    WAITING_FOR_CLARIFICATION = auto()


class Signal(Enum):
    CANCEL = -1


def build_new_location_message(lat, long, place=None):
    msg = f'Your new location has latitude {round(float(lat), 2)} and longitude {round(float(long), 2)}.'
    if place is not None:
        msg += '\n\nThis point is in {}.'.format(place)
    return msg


def on_error(update, context):
    logger.warning(f'Error {context.error} was caused by update {update}')


def on_set_location(update, context):
    logger.info('Setting user location')
    update.message.reply_text(settings.LOCATION_INQUIRY)
    return Status.WAITING_FOR_LOCATION


def update_location_db(user_id, data):
    db = Database()
    if db.exec_and_fetch(f'SELECT id FROM location WHERE id={user_id};'):
        db.exec("UPDATE location SET lat={}, lon={}, loc='{}' WHERE id={};".format(
            data['lat'],
            data['lon'],
            data['address'],
            user_id,
        ))
    else:
        db.exec("INSERT INTO location (id, lat, lon, loc) VALUES ({}, {}, {}, '{}');".format(
            user_id,
            data['lat'],
            data['lon'],
            data['address']
        ))
    db.connection.commit()


def set_location_by_name(update, context):
    """
    Receives update with location name and initiates search
    """
    logger.info('Received location name')
    place_query = update.message.text
    search_results = get_places_from_text(place_query)
    if search_results is None:
        update.message.reply_text(settings.CANCELLATION_TEXT)
        return ConversationHandler.END
    # Build keyboard for results
    buttons = []
    for i in range(len(search_results)):
        buttons.append([
            InlineKeyboardButton(text=search_results[i]['address'], callback_data=str(i))
        ])
    buttons.append([
        InlineKeyboardButton(text='None of those', callback_data=str(Signal.CANCEL))
    ])
    context.user_data[UserData.POSSIBLE_LOCATIONS] = search_results
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Which one of the following locations is yours?', reply_markup=keyboard)
    return Status.WAITING_FOR_CLARIFICATION


def set_location_by_geotag(update, context):
    """
    Receives update with geolocation
    """
    logger.info('Received location as geotag')
    location = update.message.location
    update_location_db(
        update.effective_user.id,
        {
            'lat': location.latitude,
            'lon': location.longitude,
            'address': get_place_from_coords(location.latitude, location.longitude)
        }
    )
    update.message.reply_text(build_new_location_message(
        location.latitude,
        location.longitude,
        get_place_from_coords(location.latitude, location.longitude)
    ))
    return ConversationHandler.END


def select_location(update, context):
    """
    Sets location based on the option that was selected by user
    """
    if update.callback_query.data == '-1':
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=settings.INCORRECT_SEARCH_RESULT_TEXT)
    else:
        id = int(update.callback_query.data)
        location_data = context.user_data[UserData.POSSIBLE_LOCATIONS][id]
        update_location_db(update.effective_user.id, location_data)
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=build_new_location_message(
                location_data['lat'],
                location_data['lon'],
                location_data['address']
            )
        )
    context.user_data.pop(UserData.POSSIBLE_LOCATIONS)
    return ConversationHandler.END


def on_my_location(update, context):
    db = Database()
    result = db.exec_and_fetch(f'SELECT loc FROM location WHERE id={update.effective_user.id};')
    if not result:
        update.message.reply_text(settings.LOCATION_NOT_SET_TEXT)
    else:
        update.message.reply_text(
            f'Your current location is {result[0][0]}.'
        )


def on_current_weather(update, context):
    """
    Sends a message with current weather in user location
    """
    db = Database()
    result = db.exec_and_fetch(f'SELECT lat, lon FROM location WHERE id={update.effective_user.id};')
    if not result:
        update.message.reply_text(settings.LOCATION_NOT_SET_TEXT)
        return
    lat, lon = result[0]
    weather_data = current_weather_for_coords(lat, lon)
    msg = (
        'Right now weather is {desc}.\n\n'
        'The temperature is {temp:.2f}°C, but it feels like {feel_temp:.2f}°C.'.format(
            desc=weather_data['weather'][0]['main'],
            temp=kelvin_to_celsius(weather_data['main']['temp']),
            feel_temp=kelvin_to_celsius(weather_data['main']['feels_like']),
        )
    )
    update.message.reply_text(msg)


def on_start(update, context):
    return on_set_location(update, context)


def on_cancel(update, context):
    update.message.reply_text(settings.CANCELLATION_TEXT)
    return ConversationHandler.END


def on_timeout(update, context):
    update.message.reply_text(settings.TIMEOUT_TEXT)
    return ConversationHandler.END


def prepare_updater():
    """
    Create the bot and register handlers.
    :return: Updater
    """
    updater = Updater(settings.TG_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', on_start),
            CommandHandler('set_location', on_set_location)
        ],
        states={
            Status.WAITING_FOR_LOCATION: [
                MessageHandler(Filters.text, set_location_by_name),
                MessageHandler(Filters.location, set_location_by_geotag),
            ],
            Status.WAITING_FOR_CLARIFICATION: [
                CallbackQueryHandler(select_location, pattern=r'^-1$|^[0-4]$'),
            ],
            ConversationHandler.TIMEOUT: [
                MessageHandler(Filters.all, on_timeout)
            ]
        },
        fallbacks=[CommandHandler('cancel', on_cancel)],
        conversation_timeout=settings.REPLY_TIMEOUT,
    ))

    dp.add_handler(CommandHandler('my_location', on_my_location))
    dp.add_handler(CommandHandler('current_weather', on_current_weather))
    # Handle errors
    dp.add_error_handler(on_error)

    return updater
