
import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


import logging
import re
from config_data.config import Config, load_config
from keyboards.keyboards_user import keyboards_main_menu
from keyboards.keyboards_ozon import keyboards_feedback, keyboards_get_many, \
    keyboards_150_condition, keyboards_250_condition, get_contact, keyboards_continue_screen_bay, \
    keyboards_continue_screen_feedback, keyboards_all_done, keyboards_continue_photo, keyboards_350_condition

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    link_product = State()
    link_video = State()
    screenshot_bay_ozon = State()
    screenshot_feedback_ozon = State()
    phone_user_ozon = State()
    photo_ozon = State()


user_dict = {}


def validate_russian_phone_number(phone_number):
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')

    # Проверка соответствия паттерну
    match = pattern.match(phone_number)

    return bool(match)


@router.callback_query(F.data == 'ozon')
async def process_mp_ozon(callback: CallbackQuery) -> None:
    logging.info(f'process_mp_ozon: {callback.message.chat.id}')
    await callback.message.answer(text=f'Вы уже оставили отзыв о покупке на OZON?',
                                  reply_markup=keyboards_feedback())


@router.callback_query(F.data == 'ozonyes_feedback')
async def process_yes_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_yes_feedback: {callback.message.chat.id}')
    await callback.message.answer(text='Нам важна обратная связь от наших покупателей, и мы особенно ценим тех, кто'
                                       ' оставляет подробные отзывы с качественными фотографиями. Они помогают другим'
                                       ' покупателям определиться с выбором.\n\n'
                                       'У вас есть возможность получить 150₽-350₽ за отзыв ⭐️⭐️⭐️⭐️⭐️ о каждом'
                                       ' заказанном и выкупленном товаре с OZON.')
    await state.update_data(raffle='no')
    await callback.message.answer(text=f'Вы оставили: отзыв без фото, с фото, с видео?',
                                  reply_markup=keyboards_get_many())


@router.callback_query(F.data == 'ozonfeedback_not_foto')
async def process_yes_feedback(callback: CallbackQuery) -> None:
    logging.info(f'process_feedback_not_foto: {callback.message.chat.id}')
    await callback.message.answer(text=f'За отзыв без фото вы можете получить 150₽.\n'  
                                       f' 1. Проверьте, что ваш отзыв содержит не менее двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f' 2. Отзыв был оставлен через мобильное приложение OZON.\n'
                                       f' 3. В отзыве вы не упоминали нашу визитку и не размещали ее на '
                                       f'фотографиях.\n\n'
                                       f'Все условия должны быть выполнены, иначе мы оставляем за собой право'
                                       f' отказать в вознаграждении.')
    await asyncio.sleep(2)
    await callback.message.answer(text=f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽'
                                       f' за отзыв с фото, 350₽ за отзыв с видео. Вознаграждения не суммируются.\n\n'
                                       f'Отзыв не должен быть анонимным. '
                                       f'Выплата производится только на номера российских операторов связи.',
                                  reply_markup=keyboards_150_condition())


@router.callback_query(F.data == 'ozonfeedback_is_foto')
async def process_feedback_is_foto(callback: CallbackQuery) -> None:
    logging.info(f'process_feedback_is_foto: {callback.message.chat.id}')
    await callback.message.answer(text=f'За отзыв с фото вы можете получить 250₽.\n' 
                                       f'1. Проверьте, что ваш отзыв содержит не менее двух предложений, с оценкой 5 ⭐️'
                                       f' звезд.\n'
                                       f'К нему прикреплены не менее 5 качественных фотографий.\n'
                                       f'Одежду на фотографиях должно быть хорошо видно! Изображения чёткие, вещи' 
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. Фотографии с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n' 
                                       f'2. Отзыв был оставлен через мобильное приложение OZON.\n'
                                       f'3. В отзыве вы не упоминали нашу визитку и не размещали ее на фотографиях.\n'
                                       f'Все условия должны быть выполнены, иначе мы оставляем за собой право'
                                       f' отказать в вознаграждении.')
    await asyncio.sleep(1)
    await callback.message.answer(text=f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽'
                                       f' за отзыв с фото, 350₽ за отзыв с видео. Вознаграждения не суммируются.\n\n'
                                       f'Отзыв не должен быть анонимным. '
                                       f'Выплата производится только на номера российских операторов связи.',
                                  reply_markup=keyboards_250_condition())


@router.callback_query(F.data == 'ozonfeedback_is_video')
async def process_feedback_is_foto(callback: CallbackQuery) -> None:
    logging.info(f'process_feedback_is_foto: {callback.message.chat.id}')
    await callback.message.answer(text=f'За отзыв с видео вы можете получить 350₽.\n'
                                       f' 1. Напишите отзыв не менее, чем из двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f'Прикрепите к отзыву не менее 1 видео. Не более 10 мин. Максимум -3 видео.\n'
                                       f'Одежду на видео должно быть хорошо видно! Изображения чёткие, вещи'
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. На видео вещи'
                                       f' засняты с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n'
                                       f' 2. Разместите отзыв через мобильное приложение OZON.\n'
                                       f' 3. В отзыве не упоминайте нашу визитку и не размещайте ее на видео.\n\n')
    await asyncio.sleep(1)
    await callback.message.answer(text=f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽'
                                       f' за отзыв с фото, 350₽ за отзыв с видео. Вознаграждения не суммируются.\n\n'
                                       f'Отзыв не должен быть анонимным. '
                                       f'Выплата производится только на номера российских операторов связи.',
                                  reply_markup=keyboards_350_condition())


@router.callback_query(F.data.startswith('ozonfeedback_good_'))
async def process_get_feedback_good(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_get_feedback_good: {callback.message.chat.id}')
    await state.update_data(feedback=callback.data.split('_')[-1])

    image1 = 'AgACAgIAAxkBAAIHU2YRqlbBXWGUFVsKTWkmJ7Igop7UAAJr3TEbDVeJSKQ2XsoNe_4VAQADAgADeQADNAQ'
    media = []
    media.append(InputMediaPhoto(media=image1))
    await callback.message.answer_media_group(media=media)
    await callback.message.answer(text='Пришлите ссылку на товар:')
    await state.set_state(User.link_product)


@router.message(StateFilter(User.link_product), F.text(conatains=['Получить 💰 за отзыв', '🏆 Розыгрыш', '💼 Перейти в магазин', '👤 Поддержка']))
async def process_get_article_(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_article_: {message.chat.id}')
    if message.text in ['Получить 💰 за отзыв', '🏆 Розыгрыш', '💼 Перейти в магазин', '👤 Поддержка']:
        await state.set_state(default_state)
        await message.answer(text='Вы прервали ввод данных, вы можете продолжить позже')


@router.message(F.text, StateFilter(User.link_product))
async def process_get_link_product(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_link_product: {message.chat.id}')
    await state.update_data(link_product=message.text)
    media = []
    user_dict[message.chat.id] = await state.update_data()
    image_1 = 'AgACAgIAAxkBAAIHVGYRqo5GwxoWiegVCUJC9EDFwz4_AAJs3TEbDVeJSL-ER-MMTafFAQADAgADeQADNAQ'
    media.append(InputMediaPhoto(media=image_1))
    await message.answer_media_group(media=media)
    await message.answer(text='Пришлите скриншот вашего заказа из ЛК OZON, где видно товар и статус «получен».')
    await state.set_state(User.screenshot_bay_ozon)


@router.message(F.photo, StateFilter(User.screenshot_bay_ozon))
async def get_screenshot_bay(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_bay: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_bay' in user_dict[message.chat.id].keys():
        image_id_list = user_dict[message.chat.id]['image_id_list_bay']
        image_id_list.append(image_id)
        await state.update_data(image_id_list_bay=image_id_list)
    else:
        await state.update_data(image_id_list_bay=[image_id])
    await message.answer(text='Добавьте еще скриншот или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_screen_bay())


@router.callback_query(F.data == 'ozoncontinue_screen_bay')
async def process_continue_screen(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_screen: {callback.message.chat.id}')
    await state.set_state(default_state)
    media = []
    user_dict[callback.message.chat.id] = await state.update_data()
    if user_dict[callback.message.chat.id]['feedback'] == '150':
        image_1 = 'AgACAgIAAxkBAAIHVWYRqsxC_i69rA3ABXqWljL3_YGWAAJu3TEbDVeJSCyrEVEIvYwuAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        await callback.message.answer_media_group(media=media)
        await callback.message.answer(text='Пришлите скриншот вашего отзыва:')
        await state.set_state(User.screenshot_feedback_ozon)
    if user_dict[callback.message.chat.id]['feedback'] == '250':
        image_1 = 'AgACAgIAAxkBAAIHVWYRqsxC_i69rA3ABXqWljL3_YGWAAJu3TEbDVeJSCyrEVEIvYwuAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        await callback.message.answer_media_group(media=media)
        await callback.message.answer(text='Пришлите скриншот вашего отзыва:')
        await state.set_state(User.screenshot_feedback_ozon)
    if user_dict[callback.message.chat.id]['feedback'] == '350':
        image_1 = 'AgACAgIAAxkBAAIHhGYRrYy3EBgCLwpO32xq2Yp9MgOFAAJ53TEbDVeJSG7jLfykWkliAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        await callback.message.answer_media_group(media=media)
        await callback.message.answer(text='Пришлите cсылку на видеоотзыв:')
        await state.set_state(User.link_video)


@router.message(F.photo, StateFilter(User.screenshot_feedback_ozon))
async def get_screenshot_feedback(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_feedback: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_feedback' in user_dict[message.chat.id].keys():
        image_id_list_feedback = user_dict[message.chat.id]['image_id_list_feedback']
        image_id_list_feedback.append(image_id)
        await state.update_data(image_id_list_feedback=image_id_list_feedback)
    else:
        await state.update_data(image_id_list_feedback=[image_id])
    await message.answer(text='Добавьте еще скриншот или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_screen_feedback())


@router.message(F.text, StateFilter(User.link_video))
async def get_screenshot_feedback(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_feedback: {message.chat.id}')
    await state.update_data(link_video=message.text)
    await message.answer(text='Пришлите фотографии товара из отзыва:')
    await state.set_state(User.photo_ozon)


@router.message(F.photo, StateFilter(User.photo_ozon))
async def get_screenshot_photo(message: Message, state: FSMContext) -> None:
    logging.info(f'get_screenshot_photo: {message.chat.id}')
    image_id = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    if 'image_id_list_photo' in user_dict[message.chat.id].keys():
        image_id_list_photo = user_dict[message.chat.id]['image_id_list_photo']
        image_id_list_photo.append(image_id)
        await state.update_data(image_id_list_photo=image_id_list_photo)
    else:
        await state.update_data(image_id_list_photo=[image_id])
    await message.answer(text='Добавьте еще фото или нажмите «Продолжить».',
                         reply_markup=keyboards_continue_photo())
    await state.update_data(feedback='150')


@router.callback_query(F.data == 'ozoncontinue_screen_feedback')
async def process_continue_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_feedback: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.update_data()
    print(user_dict[callback.message.chat.id]['feedback'])
    if user_dict[callback.message.chat.id]['feedback'] == '150':
        await state.set_state(User.phone_user_ozon)
        await callback.message.answer(text='Введите номер телефона для получения подарка, в международном формате:\n'
                                           '+7ХХХХХХХХХХ, или нажмите "Поделиться".\n',
                                      reply_markup=get_contact())
        await state.set_state(User.phone_user_ozon)
    else:
        await callback.message.answer(text='Пришлите фотографии товара из отзыва:')
        await state.set_state(User.photo_ozon)


@router.message(StateFilter(User.phone_user_ozon))
async def get_phone_user(message: Message, state: FSMContext) -> None:
    logging.info(f'get_phone_user: {message.chat.id}')
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера. Повторите ввод:")
            return
    await state.update_data(phone=phone)
    await state.set_state(default_state)

    await message.answer(text=f'Проверьте корректность введенных данных:'
                              f'Ссылка на товар: {user_dict[message.chat.id]["link_product"]}\n'
                              f'Телефон: {phone}',
                         reply_markup=keyboards_all_done())


@router.callback_query(F.data == 'ozonall_good')
async def process_all_good(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Отправка в канал данных пользователя
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_get_phone: {callback.message.chat.id}')
    # обновляем словарь с данными
    user_dict[callback.message.chat.id] = await state.update_data()
    # пустой список для медиа
    media = []
    if 'image_id_list_feedback' in user_dict[callback.message.chat.id]:
        # формируем список изображений со скриншотами отзыва
        for image_id in user_dict[callback.message.chat.id]['image_id_list_feedback']:
            media.append(InputMediaPhoto(media=image_id))
    if user_dict[callback.message.chat.id]['feedback'] == '350':
        # создаем подпись с альбому с фото
        caption = f'Пользователь: {callback.from_user.username}\n' \
                  f'Ссылка на товар: {user_dict[callback.message.chat.id]["link_product"]}\n' \
                  f'Ссылка на видео: {user_dict[callback.message.chat.id]["link_video"]}\n' \
                  f'Телефон: {user_dict[callback.message.chat.id]["phone"]}'
    else:
        caption = f'Пользователь: {callback.from_user.username}\n' \
                  f'Ссылка на товар: {user_dict[callback.message.chat.id]["link_product"]}\n' \
                  f'Телефон: {user_dict[callback.message.chat.id]["phone"]}'
    # формируем альбом для отправки
    for i, image_id in enumerate(user_dict[callback.message.chat.id]['image_id_list_bay']):
        if i == 0:
            media.append(InputMediaPhoto(media=image_id, caption=caption))
        else:
            media.append(InputMediaPhoto(media=image_id))
    # если есть фотогорафии товара, то добавляем и их
    if 'image_id_list_photo' in user_dict[callback.message.chat.id]:
        if len(user_dict[callback.message.chat.id]['image_id_list_photo']):
            for image_id in user_dict[callback.message.chat.id]['image_id_list_photo']:
                media.append(InputMediaPhoto(media=image_id))
        user_dict[callback.message.chat.id]['image_id_list_photo'] = []
    # если сюда пришли не из цепочки розыгрыш
    if user_dict[callback.message.chat.id]['raffle'] == 'no':
        # в альбоме не может быть более 10 фото
        if len(media) <= 10:
            await bot.send_media_group(chat_id=config.tg_bot.channel,
                                       media=media)
        else:
            await bot.send_media_group(chat_id=config.tg_bot.channel,
                                       media=media[:10])
            await bot.send_media_group(chat_id=config.tg_bot.channel,
                                       media=media[10:])

        await callback.message.answer(text='В течение 5 рабочих дней наши менеджеры проверят ваш отзыв и сделают'
                                           ' вам перевод.',
                                      reply_markup=keyboards_main_menu())
    elif user_dict[callback.message.chat.id]['raffle'] == 'yes':
        if len(media) <= 10:
            await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                       media=media)
        else:
            await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                       media=media[:10])
            await bot.send_media_group(chat_id=config.tg_bot.channel_raffle,
                                       media=media[10:])
        await callback.message.answer(text='Благодарим за заявку! Вы стали участником конкурса фотографий бренда'
                                           ' Angimina. В начале каждого месяца мы'
                                           ' объявляем призеров за предыдущий. С победителями связываемся в личных'
                                           ' сообщениях.',
                                      reply_markup=keyboards_main_menu())


@router.callback_query(F.data == 'ozonno_feedback')
async def process_no_feedback(callback: CallbackQuery) -> None:
    logging.info(f'process_no_feedback: {callback.message.chat.id}')
    await callback.message.answer(text='Нам важна обратная связь от наших покупателей, и мы особенно ценим тех, кто'
                                       ' оставляет подробные отзывы с качественными фотографиями. Они помогают другим'
                                       ' покупателям определиться с выбором.\n\n'
                                       'У вас есть возможность получить 150₽-350₽ за отзыв ⭐️⭐️⭐️⭐️⭐️ о каждом'
                                       ' заказанном и выкупленном товаре с OZON.')
    await asyncio.sleep(1)
    image_1 = 'AgACAgIAAxkBAAIHUWYRqQsM0tAQKZ3mxplwR9JTQ1WoAAJn3TEbDVeJSPN7kUK3uSsaAQADAgADeQADNAQ'
    image_2 = 'AgACAgIAAxkBAAIDcWYJvn6-FiwIhtAj9iSLZ7uBkiMDAALD1TEbwqNRSNqi48nalwXmAQADAgADeQADNAQ'
    media = []
    media.append(InputMediaPhoto(media=image_1))
    media.append(InputMediaPhoto(media=image_2))

    await asyncio.sleep(3)
    await callback.message.answer(text=f'<b>За отзыв без фото вы можете получить 150₽.</b>\n'  
                                       f' 1. Напишите отзыв не менее, чем из двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f' 2. Разместите отзыв через мобильное приложение OZON.\n'
                                       f' 3. В отзыве не упоминайте нашу визитку и не размещайте ее на '
                                       f'фотографиях.\n\n',
                                  parse_mode='html')
    await asyncio.sleep(3)
    await callback.message.answer(text=f'<b>За отзыв с фото вы можете получить 250₽.</b>\n' 
                                       f'1. Проверьте, что ваш отзыв содержит не менее двух предложений, с оценкой 5 ⭐️'
                                       f' звезд.\n'
                                       f'К нему прикреплены не менее 5 качественных фотографий.\n'
                                       f'Одежду на фотографиях должно быть хорошо видно! Изображения чёткие, вещи' 
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. Фотографии с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n' 
                                       f'2. Отзыв был оставлен через мобильное приложение OZON.\n'
                                       f'3. В отзыве вы не упоминали нашу визитку и не размещали ее на фотографиях.\n'
                                       f'Все условия должны быть выполнены, иначе мы оставляем за собой право'
                                       f' отказать в вознаграждении.',
                                  parse_mode='html')
    await callback.message.answer_media_group(media=media)
    await asyncio.sleep(3)
    await callback.message.answer(text=f'<b>За отзыв с видео вы можете получить 350₽.</b>\n'
                                       f' 1. Напишите отзыв не менее, чем из двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f'Прикрепите к отзыву не менее 1 видео. Не более 10 мин. Максимум -3 видео.\n'
                                       f'Одежду на видео должно быть хорошо видно! Изображения чёткие, вещи'
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. На видео вещи '
                                       f'засняты с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n'
                                       f' 2. Разместите отзыв через мобильное приложение OZON.\n'
                                       f' 3. В отзыве не упоминайте нашу визитку и не размещайте ее на видео.\n\n',
                                  parse_mode='html')
    await asyncio.sleep(3)
    await callback.message.answer(text=f'В случае невыполнения всех условий, мы оставляем за собой право отказать '
                                       f'в вознаграждении.\n\n'
                                       f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽ '
                                       f'за отзыв с фото, либо 350₽ за отзыв с видео. Вознаграждения не суммируются.\n\n'
                                       f'Отзыв не должен быть анонимным.\n\n'
                                       f'Выплата производится только на номера российских операторов связи.')


@router.callback_query(F.data == 'feedback_edit')
async def process_no_feedback(callback: CallbackQuery) -> None:
    logging.info(f'process_no_feedback: {callback.message.chat.id}')
    # await callback.message.answer(text='Редактирование отзывов на WB сейчас не доступно.'
    #                                    ' Рекомендуем удалить отзыв, не соответствующий условиям, и написать новый.')
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAIDUmYJuB1GmJnBZC8sD3-GvQKg1aNZAAKR1TEbwqNRSP8PsRsnYhyKAQADAgADeQADNAQ',
                                        caption='Редактирование отзывов на WB сейчас недоступно.'
                                                ' Рекомендуем удалить отзыв, не соответствующий условиям, и написать'
                                                ' новый.')


@router.callback_query(F.data == 'ozonfeedback_edit')
async def process_ozonfeedback_edit(callback: CallbackQuery) -> None:
    logging.info(f'process_ozonfeedback_edit: {callback.message.chat.id}')
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAIHUmYRqbSnU5cYRRdDsUfgw_eBG88tAAJp3TEbDVeJSIgG4PDKrRtGAQADAgADeQADNAQ',
                                        caption='Перейдите в приложение OZON и следуйте инструкции на картинке выше.')
