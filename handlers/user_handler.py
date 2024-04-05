import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


import logging
import re
from config_data.config import Config, load_config
from keyboards.keyboards_user import keyboards_main_menu, keyboards_feedback, keyboards_get_many, \
    keyboards_150_condition, keyboards_250_condition, get_contact, keyboards_continue_screen_bay, \
    keyboards_continue_screen_feedback, keyboards_all_done, keyboards_continue_photo, keyboards_raffle, \
    keyboards_raffle_, keyboards_support

router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


class User(StatesGroup):
    article = State()
    phone_user = State()
    screenshot_bay = State()
    screenshot_feedback = State()
    photo = State()
    data_feedback =State()

user_dict = {}


def validate_russian_phone_number(phone_number):
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')

    # Проверка соответствия паттерну
    match = pattern.match(phone_number)

    return bool(match)


@router.message(CommandStart())
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    logging.info(f'process_start_command_user: {message.chat.id}')

    await state.update_data(user_name=message.from_user.username)
    await state.update_data(id_telegram=message.chat.id)

    await message.answer(text=f'Добрый день, {message.from_user.first_name}!'
                              f' Мы благодарим вас за выбор детской одежды Angemina и хотим'
                              f' вознаградить за высокую оценку работы нашего магазина.',
                         reply_markup=keyboards_main_menu())


@router.message(F.text == 'Получить 💰 за отзыв')
async def process_yes_feedback(message: Message, state: FSMContext) -> None:
    logging.info(f'process_yes_feedback: {message.chat.id}')
    await state.set_state(default_state)

    await message.answer(text=f'Вы уже оставили отзыв о покупке на WB?',
                         reply_markup=keyboards_feedback())


@router.callback_query(F.data == 'yes_feedback')
async def process_yes_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_yes_feedback: {callback.message.chat.id}')
    await callback.message.answer(text=f'Нам важна обратная связь от наших покупателей, и мы особенно ценим тех, кто'
                                       f' оставляет подробные отзывы с качественными фотографиями. Они помогают другим'
                                       f' покупателям определиться с выбором.\n\n'
                                       f'У вас есть возможность получить 150₽ или 250₽ за отзыв ⭐️⭐️⭐️⭐️⭐️ о каждом'
                                       f' заказанном и выкупленном товаре с WB.')
    await state.update_data(raffle='no')
    await callback.message.answer(text=f'Вы оставили отзыв с фото или без?',
                                  reply_markup=keyboards_get_many())


@router.callback_query(F.data == 'feedback_not_foto')
async def process_yes_feedback(callback: CallbackQuery) -> None:
    logging.info(f'process_feedback_not_foto: {callback.message.chat.id}')
    await callback.message.answer(text=f'За отзыв без фото вы можете получить 150₽.\n'  
                                       f' 1. Проверьте, что ваш отзыв содержит не менее двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f' 2. Отзыв был оставлен через мобильное приложение WB.\n'
                                       f' 3. В отзыве вы не упоминали нашу визитку и не размещали ее на фотографиях.\n\n'
                                       f'Все условия должны быть выполнены, иначе мы оставляем за собой право'
                                       f' отказать в вознаграждении.')
    await asyncio.sleep(2)
    await callback.message.answer(text=f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽'
                                       f' за отзыв с фото. Вознаграждения не суммируются.\n\n'
                                       f'Выплата производится только на номера российских операторов связи.',
                                  reply_markup=keyboards_150_condition())


@router.callback_query(F.data == 'feedback_is_foto')
async def process_feedback_is_foto(callback: CallbackQuery) -> None:
    logging.info(f'process_feedback_is_foto: {callback.message.chat.id}')
    await callback.message.answer(text=f'За отзыв с фото вы можете получить 250₽.\n' 
                                       f'1. Проверьте, что ваш отзыв содержит не менее двух предложений, с оценкой 5 ⭐️'
                                       f' звезд.\n'
                                       f'К нему прикреплены 5 качественных фотографий.\n'
                                       f'Одежду на фотографиях должно быть хорошо видно! Изображения чёткие, вещи' 
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. Фотографии с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n' 
                                       f'2. Отзыв был оставлен через мобильное приложение WB.\n'
                                       f'3. В отзыве вы не упоминали нашу визитку и не размещали ее на фотографиях.\n'
                                       f'Все условия должны быть выполнены, иначе мы оставляем за собой право'
                                       f' отказать в вознаграждении.')
    await asyncio.sleep(1)
    await callback.message.answer(text=f'Обращаем ваше внимание, что можно получить 150₽ за отзыв без фото либо 250₽'
                                       f' за отзыв с фото. Вознаграждения не суммируются.\n\n'
                                       f'Выплата производится только на номера российских операторов связи.',
                                  reply_markup=keyboards_250_condition())


@router.callback_query(F.data.startswith('feedback_good_'))
async def process_get_feedback_good(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_get_feedback_good: {callback.message.chat.id}')
    await state.update_data(feedback=callback.data.split('_')[-1])
    print(callback.data.split('_')[-1])
    media = []
    if callback.data.split('_')[-1] == '150':
        image_1 = 'AgACAgIAAxkBAAID7WYJyBV0qiDrUw6qvFbev_9eL7E9AALk1TEbwqNRSLVkg940loF5AQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID7mYJyBXGBAgI66GSmEQ1PrmfLbt8AALl1TEbwqNRSDVf_xEY-stMAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID72YJyBU1lT4PKWkG4ddVnt1PtfFgAALm1TEbwqNRSN9mFP6d9iODAQADAgADeQADNAQ'
        image_4 = 'AgACAgIAAxkBAAID8GYJyBWxAiwiNrdSwlxUvrO8l4h1AALn1TEbwqNRSO4rAvtMZAXHAQADAgADeQADNAQ'
        image_5 = 'AgACAgIAAxkBAAID8WYJyBVYbISabks414mCX9Fq6K7aAALo1TEbwqNRSL3YpJ5AzKmDAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
        media.append(InputMediaPhoto(media=image_4))
        media.append(InputMediaPhoto(media=image_5))
    if callback.data.split('_')[-1] == '250':
        image_1 = 'AgACAgIAAxkBAAID7WYJyBV0qiDrUw6qvFbev_9eL7E9AALk1TEbwqNRSLVkg940loF5AQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID7mYJyBXGBAgI66GSmEQ1PrmfLbt8AALl1TEbwqNRSDVf_xEY-stMAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID8mYJyEm6xUENtAABzhBOFsZ73aaWlgAC6dUxG8KjUUgDOAQcpU6SpgEAAwIAA3kAAzQE'
        image_4 = 'AgACAgIAAxkBAAID8GYJyBWxAiwiNrdSwlxUvrO8l4h1AALn1TEbwqNRSO4rAvtMZAXHAQADAgADeQADNAQ'
        image_5 = 'AgACAgIAAxkBAAID8WYJyBVYbISabks414mCX9Fq6K7aAALo1TEbwqNRSL3YpJ5AzKmDAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
        media.append(InputMediaPhoto(media=image_4))
        media.append(InputMediaPhoto(media=image_5))
    await callback.message.answer_media_group(media=media)
    await callback.message.answer(text='Введите артикул товара')
    await state.set_state(User.article)


@router.message(F.text.isdigit(), StateFilter(User.article))
async def process_get_article(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_article: {message.chat.id}')
    await state.update_data(article=message.text)
    media = []
    user_dict[message.chat.id] = await state.update_data()
    if user_dict[message.chat.id]['feedback'] == '150':
        image_1 = 'AgACAgIAAxkBAAID82YJyIto6mrzQ6p0sh5-tFPUIz4FAALq1TEbwqNRSHpjfN-Z0AIpAQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID9GYJyIuKlo34Xz-l0NpdFvwNd58yAALr1TEbwqNRSBfHemzMftKVAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID9WYJyItmIC_rkXtwoAuKF0Rfte58AALs1TEbwqNRSJdkjRqMg-2MAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
    if user_dict[message.chat.id]['feedback'] == '250':
        image_1 = 'AgACAgIAAxkBAAID82YJyIto6mrzQ6p0sh5-tFPUIz4FAALq1TEbwqNRSHpjfN-Z0AIpAQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID9GYJyIuKlo34Xz-l0NpdFvwNd58yAALr1TEbwqNRSBfHemzMftKVAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID9mYJyK_82v2oPUQsVLFx2-sFdM9UAALt1TEbwqNRSCJhTuZmqrUjAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
    await message.answer_media_group(media=media)
    await message.answer(text='Пришлите скриншот ваших покупок из ЛК WB, где видно товар и статус «доставлен»'
                              ' или «получен».')
    await state.set_state(User.screenshot_bay)


@router.message(StateFilter(User.article))
async def process_get_article_(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_article_: {message.chat.id}')
    if message.text in ['Получить 💰 за отзыв', '🏆 Розыгрыш', '💼 Перейти в магазин', '👤 Поддержка']:
        await state.set_state(default_state)
        await message.answer(text='Вы прервали ввод данных, вы можете продолжить позже')
    else:
        await message.answer(text='Артикул некорректный. Повторите ввод:')


@router.message(F.photo, StateFilter(User.screenshot_bay))
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


@router.callback_query(F.data == 'continue_screen_bay')
async def process_continue_screen(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_continue_screen: {callback.message.chat.id}')
    await state.set_state(default_state)
    media = []
    user_dict[callback.message.chat.id] = await state.update_data()
    if user_dict[callback.message.chat.id]['feedback'] == '150':
        image_1 = 'AgACAgIAAxkBAAID92YJyNlFSkF6CtDL5ansWFj3b0bvAALv1TEbwqNRSHU4ONKSHxhjAQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID-GYJyNkSdPKHAkWlghmbEjo_AhgCAALw1TEbwqNRSMTPr4cWJPhnAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID-WYJyNkB3_VGDt90kzN8aBzLcW8zAALx1TEbwqNRSD2zwKt7yU-mAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
    if user_dict[callback.message.chat.id]['feedback'] == '250':
        image_1 = 'AgACAgIAAxkBAAID92YJyNlFSkF6CtDL5ansWFj3b0bvAALv1TEbwqNRSHU4ONKSHxhjAQADAgADeQADNAQ'
        image_2 = 'AgACAgIAAxkBAAID-GYJyNkSdPKHAkWlghmbEjo_AhgCAALw1TEbwqNRSMTPr4cWJPhnAQADAgADeQADNAQ'
        image_3 = 'AgACAgIAAxkBAAID-mYJyQ8RZehQ0SRPRJx26SiLQruSAAL11TEbwqNRSGCQAxxmCLfSAQADAgADeQADNAQ'
        media.append(InputMediaPhoto(media=image_1))
        media.append(InputMediaPhoto(media=image_2))
        media.append(InputMediaPhoto(media=image_3))
    await callback.message.answer_media_group(media=media)
    await callback.message.answer(text='Пришлите скриншот вашего отзыва:')
    await state.set_state(User.screenshot_feedback)


@router.message(F.photo, StateFilter(User.screenshot_feedback))
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


@router.message(F.photo, StateFilter(User.photo))
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


@router.callback_query(F.data == 'continue_screen_feedback')
async def process_continue_feedback(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_continue_feedback: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.update_data()
    print(user_dict[callback.message.chat.id]['feedback'])
    if user_dict[callback.message.chat.id]['feedback'] == '150':
        await state.set_state(User.phone_user)
        await callback.message.answer(text='Введите номер телефона для получения подарка, в международном формате:\n'
                                           '+7ХХХХХХХХХХ, или нажмите "Поделиться".\n',
                                      reply_markup=get_contact())
        await state.set_state(User.phone_user)
    else:
        await callback.message.answer(text='Пришлите фотографии товара из отзыва:')
        await state.set_state(User.photo)


@router.message(StateFilter(User.phone_user))
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
                              f'Артикул: {user_dict[message.chat.id]["article"]}\n'
                              f'Телефон: {phone}',
                         reply_markup=keyboards_all_done())


@router.callback_query(F.data == 'all_good')
async def process_all_good(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_get_phone: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.update_data()
    # await bot.send_message(chat_id=config.tg_bot.channel,
    #                        text=f'Пользователь: {user_dict[callback.message.chat.id]["user_name"]}\n'
    #                             f'Артикул: {user_dict[callback.message.chat.id]["article"]}\n'
    #                             f'Телефон: {user_dict[callback.message.chat.id]["phone"]}')
    media = []
    for image_id in user_dict[callback.message.chat.id]['image_id_list_feedback']:
        media.append(InputMediaPhoto(media=image_id))
    caption = f'Пользователь: {callback.from_user.username}\n' \
              f'Артикул: {user_dict[callback.message.chat.id]["article"]}\n' \
              f'Телефон: {user_dict[callback.message.chat.id]["phone"]}'
    for i, image_id in enumerate(user_dict[callback.message.chat.id]['image_id_list_bay']):
        if i == 0:
            media.append(InputMediaPhoto(media=image_id, caption=caption))
        else:
            media.append(InputMediaPhoto(media=image_id))
    if 'image_id_list_photo' in user_dict[callback.message.chat.id]:
        if len(user_dict[callback.message.chat.id]['image_id_list_photo']):
            for image_id in user_dict[callback.message.chat.id]['image_id_list_bay']:
                media.append(InputMediaPhoto(media=image_id))

    if user_dict[callback.message.chat.id]['raffle'] == 'no':
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
async def process_get_data_feedback(message: Message, state: FSMContext) -> None:
    logging.info(f'process_get_data_feedback: {message.chat.id}')
    await state.update_data(data_feedback=message.text)
    await state.update_data(feedback='250')
    await state.update_data(raffle='yes')
    image_1 = 'AgACAgIAAxkBAAID7WYJyBV0qiDrUw6qvFbev_9eL7E9AALk1TEbwqNRSLVkg940loF5AQADAgADeQADNAQ'
    image_2 = 'AgACAgIAAxkBAAID7mYJyBXGBAgI66GSmEQ1PrmfLbt8AALl1TEbwqNRSDVf_xEY-stMAQADAgADeQADNAQ'
    image_3 = 'AgACAgIAAxkBAAID8mYJyEm6xUENtAABzhBOFsZ73aaWlgAC6dUxG8KjUUgDOAQcpU6SpgEAAwIAA3kAAzQE'
    image_4 = 'AgACAgIAAxkBAAID8GYJyBWxAiwiNrdSwlxUvrO8l4h1AALn1TEbwqNRSO4rAvtMZAXHAQADAgADeQADNAQ'
    image_5 = 'AgACAgIAAxkBAAID8WYJyBVYbISabks414mCX9Fq6K7aAALo1TEbwqNRSL3YpJ5AzKmDAQADAgADeQADNAQ'
    media = []
    media.append(InputMediaPhoto(media=image_1))
    media.append(InputMediaPhoto(media=image_2))
    media.append(InputMediaPhoto(media=image_3))
    media.append(InputMediaPhoto(media=image_4))
    media.append(InputMediaPhoto(media=image_5))
    await message.answer_media_group(media=media)
    await message.answer(text='Введите артикул товара')
    await state.set_state(User.article)


@router.message(F.text == '👤 Поддержка')
async def process_support(message: Message, state: FSMContext) -> None:
    logging.info(f'process_support: {message.chat.id}')
    await state.set_state(default_state)
    await message.answer(text=f'Если у вас возникли вопросы, вы можете задать их менеджеру перейдя по кнопке'
                              f' «Поддержка»',
                         reply_markup=keyboards_support())


@router.callback_query(F.data == 'no_feedback')
async def process_no_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'process_no_feedback: {callback.message.chat.id}')
    await callback.message.answer(text='Нам важна обратная связь от наших покупателей, и мы особенно ценим тех, кто'
                                       ' оставляет подробные отзывы с качественными фотографиями. Они помогают другим'
                                       ' покупателям определиться с выбором.\n\n'
                                       'У вас есть возможность получить 150₽ или 250₽ за отзыв ⭐️⭐️⭐️⭐️⭐️ о каждом'
                                       ' заказанном и выкупленном товаре с WB.')
    await asyncio.sleep(1)
    image_1 = 'AgACAgIAAxkBAAIDcGYJvnvaLNCJ8hBofPpR4vwzZV_5AALC1TEbwqNRSC2D_nR17iYCAQADAgADeQADNAQ'
    image_2 = 'AgACAgIAAxkBAAIDcWYJvn6-FiwIhtAj9iSLZ7uBkiMDAALD1TEbwqNRSNqi48nalwXmAQADAgADeQADNAQ'
    media = []
    media.append(InputMediaPhoto(media=image_1))
    media.append(InputMediaPhoto(media=image_2))

    await asyncio.sleep(3)
    await callback.message.answer(text=f'За отзыв без фото вы можете получить 150₽.\n'  
                                       f' 1. Напишите отзыв не менее, чем из двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f' 2. Разместите отзыв через мобильное приложение WB.\n'
                                       f' 3. В отзыве не упоминайте нашу визитку и не размещайте ее на фотографиях.\n\n')
    await asyncio.sleep(3)
    await callback.message.answer_media_group(media=media)
    await callback.message.answer(text=f'За отзыв с фото вы можете получить 250₽.\n'
                                       f' 1. Напишите отзыв не менее, чем из двух предложений, с оценкой '
                                       f'5 ⭐️ звезд.\n'
                                       f'Прикрепите к отзыву 5 качественных фотографий, как в примере выше.\n'
                                       f'Одежду на фотографиях должно быть хорошо видно! Изображения чёткие, вещи'
                                       f' опрятные: надеты на ребенка, лежат и/или висят на вешалке. Фотографии с'
                                       f' разных планов и ракурсов (сзади/спереди). В кадре нет бардака и посторонних'
                                       f' предметов.\n'
                                       f' 2. Разместите отзыв через мобильное приложение WB.\n'
                                       f' 3. В отзыве не упоминайте нашу визитку и не размещайте ее на фотографиях.\n\n')
    await callback.message.answer(text=f'При не выполнении всех условий, мы оставляем за собой право'
                                       f' отказать в вознаграждении.')


@router.callback_query(F.data == 'feedback_edit')
async def process_no_feedback(callback: CallbackQuery) -> None:
    logging.info(f'process_no_feedback: {callback.message.chat.id}')
    # await callback.message.answer(text='Редактирование отзывов на WB сейчас не доступно.'
    #                                    ' Рекомендуем удалить отзыв, не соответствующий условиям, и написать новый.')
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAIDUmYJuB1GmJnBZC8sD3-GvQKg1aNZAAKR1TEbwqNRSP8PsRsnYhyKAQADAgADeQADNAQ',
                                        caption='Редактирование отзывов на WB сейчас недоступно.'
                                                ' Рекомендуем удалить отзыв, не соответствующий условиям, и написать новый.')
