from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_feedback():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Да',  callback_data='ozonyes_feedback')
    button_2 = InlineKeyboardButton(text='Нет',  callback_data='ozonno_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2, button_1]],)
    return keyboard


def keyboards_get_many():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв без фото ',  callback_data='ozonfeedback_not_foto')
    button_2 = InlineKeyboardButton(text='Отзыв с фото',  callback_data='ozonfeedback_is_foto')
    button_3 = InlineKeyboardButton(text='Отзыв с видео', callback_data='ozonfeedback_is_video')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard


def keyboards_150_condition():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв соответствует условиям',  callback_data='ozonfeedback_good_150')
    button_2 = InlineKeyboardButton(text='Как изменить отзыв?', callback_data='ozonfeedback_edit')
    button_3 = InlineKeyboardButton(text='💰 Получить 250 ₽ за отзыв c 📸',  callback_data='ozonfeedback_is_foto')
    button_4 = InlineKeyboardButton(text='💰 Получить 350 ₽ за отзыв с 🎥', callback_data='ozonfeedback_is_video')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def keyboards_250_condition():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв соответствует условиям',  callback_data='ozonfeedback_good_250')
    button_2 = InlineKeyboardButton(text='Как изменить отзыв?', callback_data='ozonfeedback_edit')
    button_3 = InlineKeyboardButton(text='💰 Получить 150 ₽ за отзыв без 📸',  callback_data='ozonfeedback_not_foto')
    button_4 = InlineKeyboardButton(text='💰 Получить 350 ₽ за отзыв с 🎥', callback_data='ozonfeedback_is_video')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def keyboards_350_condition():
    logging.info("keyboards_start")
    button_1 = InlineKeyboardButton(text='Отзыв соответствует условиям',  callback_data='ozonfeedback_good_350')
    button_2 = InlineKeyboardButton(text='Как изменить отзыв?', callback_data='ozonfeedback_edit')
    button_3 = InlineKeyboardButton(text='💰 Получить 150 ₽ за отзыв без 📸',  callback_data='ozonfeedback_not_foto')
    button_4 = InlineKeyboardButton(text='💰 Получить 250 ₽ за отзыв c 📸', callback_data='ozonfeedback_is_foto')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def get_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                             request_contact=True)]])
    return keyboard


def keyboards_continue_screen_bay():
    logging.info("keyboards_continue_screen_bay")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='ozoncontinue_screen_bay')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_screen_feedback():
    logging.info("keyboards_continue_screen")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='ozoncontinue_screen_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_continue_photo():
    logging.info("keyboards_continue_photo")
    button_1 = InlineKeyboardButton(text='Продолжить',  callback_data='ozoncontinue_screen_feedback')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboards_all_done():
    logging.info("keyboards_all_done")
    button_1 = InlineKeyboardButton(text='Все верно',  callback_data='ozonall_good')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='ozonyes_feedback')
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
    button_2 = InlineKeyboardButton(text='Поддержка', url='https://t.me/AngeminaKids')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2]],)
    return keyboard
