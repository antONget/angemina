from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_main_menu():
    logging.info("keyboards_main_menu")
    button_1 = KeyboardButton(text='Получить 💰 за отзыв')
    button_2 = KeyboardButton(text='🏆 Розыгрыш')
    button_3 = KeyboardButton(text='💼 Перейти в магазин',
                              web_app=WebAppInfo(url='https://www.wildberries.ru/brands/22192417-angemina'))
    button_4 = KeyboardButton(text='👤 Поддержка')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3], [button_4]],
                                   resize_keyboard=True)
    return keyboard


def keyboards_feedback():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Да',  callback_data='yes_feedback')
    button_2 = InlineKeyboardButton(text='Нет',  callback_data='no_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2, button_1]],)
    return keyboard


def keyboards_get_many():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв без фото',  callback_data='feedback_not_foto')
    button_2 = InlineKeyboardButton(text='Отзыв с фото',  callback_data='feedback_is_foto')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboards_150_condition():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв соответствует условиям',  callback_data='feedback_good_150')
    button_2 = InlineKeyboardButton(text='Как изменить отзыв?', callback_data='feedback_edit')
    button_3 = InlineKeyboardButton(text='💰 Получить 250 ₽ за отзыв',  callback_data='feedback_is_foto')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard


def keyboards_250_condition():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв соответствует условиям',  callback_data='feedback_good_250')
    button_2 = InlineKeyboardButton(text='Как изменить отзыв?', callback_data='feedback_edit')
    button_3 = InlineKeyboardButton(text='💰 Получить 150 ₽ за отзыв',  callback_data='feedback_not_foto')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard



def get_contact_():
    logging.info("get_contact")
    button_1 = InlineKeyboardButton(text='Отмена', callback_data='back')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
    return keyboard


def get_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                             request_contact=True)]])
    return keyboard


def keyboards_continue_screen_bay():
    logging.info("keyboards_continue_screen_bay")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_screen_bay')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_screen_feedback():
    logging.info("keyboards_continue_screen")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_screen_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_photo():
    logging.info("keyboards_continue_photo")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='continue_screen_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_all_done():
    logging.info("keyboards_all_done")
    button_1 = InlineKeyboardButton(text='Все верно',  callback_data='all_good')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='yes_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]],)
    return keyboard


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

def keyboards_support():
    logging.info("keyboards_support")
    button_2 = InlineKeyboardButton(text='Поддержка', url='https://t.me/four4five')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2]],)
    return keyboard
