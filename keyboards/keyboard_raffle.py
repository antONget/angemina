from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_raffle():
    logging.info("keyboards_raffle")
    button_1 = InlineKeyboardButton(text='Условия конкурса',  callback_data='what_raffle')
    button_2 = InlineKeyboardButton(text='Участвовать!', callback_data='yes_raffle')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]],)
    return keyboard


def keyboards_raffle_():
    logging.info("keyboards_raffle_")
    button_2 = InlineKeyboardButton(text='Участвовать', callback_data='yes_raffle')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2]],)
    return keyboard


def keyboards_continue_screen_bay_raffle():
    logging.info("keyboards_continue_screen_bay_raffle")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_screen_bay_raffle')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_screen_feedback_raffle():
    logging.info("keyboards_continue_screen_feedback_raffle")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_screen_feedback_raffle')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_photo_raffle():
    logging.info("keyboards_continue_photo_raffle")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_photo_feedback_raffle')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def get_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                             request_contact=True)]])
    return keyboard