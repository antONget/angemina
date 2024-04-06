
import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


import logging
import re
from config_data.config import Config, load_config
from keyboards.keyboard_raffle import keyboards_raffle, keyboards_raffle_, keyboards_continue_screen_bay_raffle, \
    keyboards_continue_screen_feedback_raffle, keyboards_continue_photo_raffle, get_contact
from keyboards.keyboards_user import keyboards_main_menu

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    article_raffle = State()
    phone_user_raffle = State()
    screenshot_bay_raffle = State()
    screenshot_feedback_raffle = State()
    photo_raffle = State()
    data_feedback = State()


user_dict = {}


def validate_russian_phone_number(phone_number):
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')

    # Проверка соответствия паттерну
    match = pattern.match(phone_number)

    return bool(match)


@router.message(F.text == '🏆 Розыгрыш')
async def process_raffle(message: Message, state: FSMContext) -> None:
    logging.info(f'process_raffle: {message.chat.id}')
    await state.set_state(default_state)
    await message.answer(text=f'Прими участие и выиграй до 5000₽ за фото!',
                         reply_markup=keyboards_raffle())


@router.callback_query(F.data == 'what_raffle')
async def process_what_raffle(callback: CallbackQuery) -> None:
    logging.info(f'process_what_raffle: {callback.message.chat.id}')
    await callback.message.answer(text='Раз в месяц среди присланных фотографий мы выбираем лучшие и награждаем их'
                                       ' авторов денежными призами!\n\n'
                                       'Дарим:\n'
                                       '🥇за 1 место — 5000₽\n'
                                       '🥈за 2 место — 3000₽\n'
                                       '🥉за 3 место — 2000₽*\n'
                                       '🏅за 4-10 место — 1000₽*\n'
                                       'А также нами будут выбраны 20 победителей, чьи фотографии мы разместим'
                                       ' в карточках наших товаров🤩в течении 1 месяца.\n'
                                       '*Розыгрывается при наличии 20 и более участников.')
    await callback.message.answer(text='Если вы готовы побороться и выиграть до 5000₽:\n'
                                       '1) Сделайте самое красивое фото нашей одежды.\n'
                                       '2) Оставьте отзыв 5⭐️, прикрепив ваши фотографии.\n'
                                       '3) Нажмите кнопку ниже «Участвовать» и прикрепите скриншот с'
                                       ' вашим отзывом.\n'
                                       '4) Дождитесь результатов! В начале каждого месяца мы объявляем победителей'
                                       ' за предыдущий месяц.\n'
                                       'Если вы победите — мы свяжемся с вами по контактному номеру телефона.',
                                  reply_markup=keyboards_raffle_())


@router.callback_query(F.data == 'yes_raffle')
async def process_what_raffle(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_what_raffle: {callback.message.chat.id}')
    await callback.message.answer(text='Для участия в конкурсе следуйте инструкции.')
    await asyncio.sleep(1)
    await callback.message.answer(text='Укажите дату публикация отзыва в числовом формате вида: число, месяц, год.'
                                       ' Например, 01.01.2024')
    await state.set_state(User.data_feedback)


@router.message(F.text, StateFilter(User.data_feedback))
async def process_get_data_feedback_raffle(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_data_feedback_raffle: {message.chat.id}')
    await state.update_data(data_feedback_raffle=message.text)
    await message.answer(text='Введите артикул товара с WB или прикрепите ссылку на товар OZON')
    await state.set_state(User.article_raffle)


@router.message(StateFilter(User.article_raffle),
                F.text(conatains=['Получить 💰 за отзыв', '🏆 Розыгрыш', '💼 Перейти в магазин', '👤 Поддержка']))
async def process_get_article_(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_article_: {message.chat.id}')
    if message.text in ['Получить 💰 за отзыв', '🏆 Розыгрыш', '💼 Перейти в магазин', '👤 Поддержка']:
        await state.set_state(default_state)
        await message.answer(text='Вы прервали ввод данных, вы можете продолжить позже')


@router.message(StateFilter(User.article_raffle))
async def process_get_article_raffle(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_article_raffle: {message.chat.id}')
    await state.update_data(article_raffle=message.text)
    await message.answer(text='Пришлите скриншот ваших покупок из ЛК, где видно товар и статус «доставлен»'
                              ' или «получен».')
    await state.set_state(User.screenshot_bay_raffle)


@router.message(F.photo, StateFilter(User.screenshot_bay_raffle))
async def get_screenshot_bay_raffle(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_bay_raffle: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_bay_raffle' in user_dict[message.chat.id].keys():
        image_id_list = user_dict[message.chat.id]['image_id_list_bay_raffle']
        image_id_list.append(image_id)
        await state.update_data(image_id_list_bay_raffle=image_id_list)
    else:
        await state.update_data(image_id_list_bay_raffle=[image_id])
    await message.answer(text='Добавьте еще скриншот или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_screen_bay_raffle())


@router.callback_query(F.data == 'continue_screen_bay_raffle')
async def process_continue_screen_raffle(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_screen_raffle: {callback.message.chat.id}')
    await state.set_state(default_state)
    await callback.message.answer(text='Пришлите скриншот вашего отзыва:')
    await state.set_state(User.screenshot_feedback_raffle)


@router.message(F.photo, StateFilter(User.screenshot_feedback_raffle))
async def get_screenshot_feedback(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_feedback: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_feedback_raffle' in user_dict[message.chat.id].keys():
        image_id_list_feedback = user_dict[message.chat.id]['image_id_list_feedback_raffle']
        image_id_list_feedback.append(image_id)
        await state.update_data(image_id_list_feedback_raffle=image_id_list_feedback)
    else:
        await state.update_data(image_id_list_feedback_raffle=[image_id])
    await message.answer(text='Добавьте еще скриншот или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_screen_feedback_raffle())


@router.callback_query(F.data == 'continue_screen_feedback_raffle')
async def process_continue_feedback_raffle(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_feedback_raffle: {callback.message.chat.id}')
    await callback.message.answer(text='Пришлите фотографии товара из отзыва:')
    await state.set_state(User.photo_raffle)


@router.message(F.photo, StateFilter(User.photo_raffle))
async def get_screenshot_photo(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_photo: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_photo_raffle' in user_dict[message.chat.id].keys():
        image_id_list_photo = user_dict[message.chat.id]['image_id_list_photo_raffle']
        image_id_list_photo.append(image_id)
        await state.update_data(image_id_list_photo_raffle=image_id_list_photo)
    else:
        await state.update_data(image_id_list_photo_raffle=[image_id])
    await message.answer(text='Добавьте еще фото или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_photo_raffle())


@router.callback_query(F.data == 'continue_photo_feedback_raffle')
async def process_continue_photo_feedback_raffle(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_photo_feedback_raffle: {callback.message.chat.id}')
    await callback.message.answer(text='Введите номер телефона для получения подарка, в международном формате:\n'
                                       '+7ХХХХХХХХХХ, или нажмите "Поделиться".\n',
                                  reply_markup=get_contact())
    await state.set_state(User.phone_user_raffle)


@router.message(StateFilter(User.phone_user_raffle))
async def get_phone_user(message: Message, state: FSMContext, bot: Bot) -> None:
    logging.info(f'get_phone_user: {message.chat.id}')
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера. Повторите ввод:")
            return
    await state.update_data(phone_raffle=phone)
    await state.set_state(default_state)
    # обновляем словарь с данными
    user_dict[message.chat.id] = await state.update_data()
    # пустой список для медиа
    media = []
    # формируем список изображений со скриншотами отзыва
    for image_id in user_dict[message.chat.id]['image_id_list_feedback_raffle']:
        media.append(InputMediaPhoto(media=image_id))
        # создаем подпись с альбому с фото
    caption = f'Пользователь: {message.from_user.username}\n' \
              f'Ссылка/Артикул на товар: {user_dict[message.chat.id]["article_raffle"]}\n' \
              f'Дата публикации отзыва: {user_dict[message.chat.id]["data_feedback_raffle"]}\n' \
              f'Телефон: {user_dict[message.chat.id]["phone_raffle"]}'
    # формируем альбом для отправки
    for i, image_id in enumerate(user_dict[message.chat.id]['image_id_list_bay_raffle']):
        if i == 0:
            media.append(InputMediaPhoto(media=image_id, caption=caption))
        else:
            media.append(InputMediaPhoto(media=image_id))
    for image_id in user_dict[message.chat.id]['image_id_list_photo_raffle']:
        media.append(InputMediaPhoto(media=image_id))

    if len(media) <= 10:
        await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                   media=media)
    else:
        await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                   media=media[:10])
        await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                   media=media[10:])
    await message.answer(text='Благодарим за заявку! Вы стали участником конкурса фотографий бренда'
                              ' Angimina. В начале каждого месяца мы'
                              ' объявляем призеров за предыдущий. С победителями связываемся в личных'
                              ' сообщениях.',
                         reply_markup=keyboards_main_menu())
