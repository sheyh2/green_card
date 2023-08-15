import telebot
import time
from telebot import types
from datetime import datetime, timedelta


TOKEN = '5782318118:AAH5S6i15tkNVFPCUfIIDXuFuU7DF__bvvE'
CHANNEL_USERNAME = '-1001807711155'
SUBSCRIBER_INFO = '-1001811604521'

bot = telebot.TeleBot(TOKEN)
next_start_command_time = {}
user_pages = {}
# Создаем словарь для временного хранения времени нажатия кнопки
last_button_press_time = {}
# Your registration dictionary to store user data. For simplicity, we use a dictionary here.
registration_data = {}
registration_number = 1
user_marital_status = {}

# Создание словаря для хранения времени последнего запроса от каждого пользователя
last_start_command_time = {}

def countdown_timer(user_id):
    time_left = 10  # Время в секундах, которое пользователь должен подождать
    while time_left > 0:
        bot.send_message(user_id, f"Palata: {time_left} sekund o'tdi. /start komandasini bosing.")
        time_left -= 1
        time.sleep(1)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    current_time = time.time()

    # Проверяем, когда пользователь сможет снова использовать команду /start
    if user_id in next_start_command_time and current_time < next_start_command_time[user_id]:
        time_left = int(next_start_command_time[user_id] - current_time)
        bot.send_message(user_id,
                         f"Iltimos, kuting. Siz hali {time_left} sekund o'tmaguncha /start komandasini bosa olmaysiz.")
        return

    next_start_command_time[user_id] = current_time + 15  # Добавляем 15 секунд к текущему времени

    user_pages[user_id] = 1
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status == 'member' or member.status == 'creator' or member.status == 'administrator':
        # User is subscribed to the channel
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        registration_button = types.InlineKeyboardButton("📝Registratsiyadan o'tish", callback_data="registration")
        ds_button = types.InlineKeyboardButton("ℹ️DS-160 va DS-260", callback_data="ds")  # Add this line
        result_button = types.InlineKeyboardButton("🏆 DV2024 natija", callback_data="result")  # Add this line
        guest_button = types.InlineKeyboardButton("👤 Mijozlarimiz", callback_data="guest")  # Add this line
        contacts_button = types.InlineKeyboardButton("📞Kontaktlar", callback_data="contacts")
        faq_button = types.InlineKeyboardButton("❓ FAQ", callback_data="faq")  # Add this line
        keyboard.add(registration_button, ds_button, result_button, guest_button, contacts_button, faq_button)  # Add faq_button

        bot.send_message(user_id, "Bosh sahifa.", reply_markup=keyboard)
    else:
        # User is not subscribed to the channel
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        subscribe_button = types.InlineKeyboardButton("Kanalga a'zo bo'lish", url="https://t.me/green_card_uzbekistan")
        check_button = types.InlineKeyboardButton("A'zolikni tekshirish", callback_data="check_subscription")
        keyboard.add(subscribe_button, check_button)

        bot.send_message(user_id, "Botdan foydalanish uchun kanalimizga a'zo bo'ling. So'ngra botning qo'shimcha imkoniyatlariga ega bo'lasiz.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "ds")
def handle_ds_button(call):
    user_id = call.from_user.id

    # Here you can send the relevant information about DS-160 and DS-260
    ds_info = (
        "DS-160 va DS-260 anketa to'ldirish uchun: @dachatop_uzb ga yoki +998998029699 ga murojaat qilishingiz mumkin.\n\n"
        "Eslatma:\nDS-160 Noimmigratsion vizalar uchun to'ldiriladi.\nDS-260 Immigratsion vizalar uchun to'ldiriladi.",
        # Add more information as needed
    )

    bot.send_message(user_id, ds_info)

@bot.callback_query_handler(func=lambda call: call.data == "result")
def handle_result(call):
    # Текст с результатами DV2024
    result_text = """
    Quyida, dunyo bo’ylab eng ko’p yutuq egalari tanlab olingan mamlakatlar 10 taligini e’lon qilamiz. 

    🇺🇿 O’zbekiston - 5555
    🇷🇺 Rossiya - 5514
    🇪🇬 Misr - 5509
    🇸🇩 Sudan - 5435
    🇩🇿 Jazoir - 5142
    🇮🇷 Eron - 5077
    🇦🇫 Afg'oniston - 4536
    🇰🇬 Qirg’iziston - 4464
    🇺🇦 Ukraina - 4286
    🇲🇦 Marokash - 4250

    O’rta Osiyo boyicha. 
    🇺🇿 O’zbekiston - 5555
    🇦🇫 Afg’oniston - 4536
    🇰🇬 Qirg’iziston - 4464
    🇹🇯 Tojikiston - 3580
    🇰🇿 Qozog’iston - 2728
    🇹🇲 Turkmaniston -1313
    """

    bot.send_message(call.message.chat.id, result_text, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "guest")
def handle_guest_button(call):
    user_id = call.from_user.id

    guest_links = [
        {"title": "2018 yil lotereyada ishtirok etib, 2020 yil uchun yullanma olgan yutuk soxiblaridan biri.",
         "url": "https://t.me/green_card_uzbekistan/201"},
        {"title": "DV 2022 lotereyasida ishtirоk etib, yutuq qo’lga kiritib visa olib chiqqan ilk ishtirokchimiz.",
         "url": "https://t.me/green_card_uzbekistan/261"},
        {"title": "DV 2022 g’oliblaridan. Eson omon Amerikaga yetib borishdi.",
         "url": "https://t.me/green_card_uzbekistan/269"},
        {"title": "2022 lotereyasida ishtirоk etib, yutuq qo’lga kiritib visa olib chiqqan yana bir mijozimiz o'z hissiyotlarini baham kordilar.",
         "url": "https://t.me/green_card_uzbekistan/272"},
        {"title": "28 Fevral, 2022 yil DV2022 suhbatiga kirib “Finally refused” (qat’iy rad javobi) olib chiqqan mijozimiz bugun Viza olgandan keying quvonchini siz bilan ulashmoqda!",
         "url": "https://t.me/green_card_uzbekistan/273"},
        {"title": "Green Card 2023 ilk viza sohibi.",
         "url": "https://t.me/green_card_uzbekistan/306"},
        {"title": "Green Card 2023 g’oliblari visa olishda davom etmoqda 🎊🎉",
         "url": "https://t.me/green_card_uzbekistan/309"},
        {"title": "5ta farzandli mijozimiz viza olib chiqdilar.",
         "url": "https://t.me/green_card_uzbekistan/310"},
        {"title": "Green Card vizasi uchun suhbatga kirib viza olgan mijozimizning taassurotlari.",
         "url": "https://t.me/green_card_uzbekistan/311"},
        {"title": "Green Card 2023 yutiq sohibi, case raqam 19**",
         "url": "https://t.me/green_card_uzbekistan/312"},
        {"title": "Yaponiyaning, Tokyo shahridagi AQSh elchihonasidan suhbatdan o’tgan hamyurtimiz vizalarini qo’lga kiritdilar.",
         "url": "https://t.me/green_card_uzbekistan/317"},
        {"title": "Yana bir mamnun mijozimiz o’z vizalarini qo’lga kiritdi.",
         "url": "https://t.me/green_card_uzbekistan/327"},
        {"title": "Yana bir hursand mijozimiz o’z vizalarini qo’lga kiritdilar.",
         "url": "https://t.me/green_card_uzbekistan/331"},
        {"title": "Yana bir mijozimiz AQSH vizanisini qo'lga kiritdilar.",
         "url": "https://t.me/green_card_uzbekistan/332"},


        # ... добавьте остальные ссылки ...
    ]

    items_per_page = 5  # Количество элементов на странице
    start_index = (get_current_page(user_id) - 1) * items_per_page
    end_index = start_index + items_per_page

    guest_text = "👤 Bizning mijozlarimiz:\n\n"

    for idx, link in enumerate(guest_links[start_index:end_index], start=start_index + 1):
        guest_text += f"{idx}. <a href='{link['url']}'>{link['title']}</a>\n\n"

    if end_index < len(guest_links):
        # Добавляем кнопку "Загрузить ещё", если есть ещё элементы
        load_more_button = telebot.types.InlineKeyboardButton("Yana yuklash", callback_data="load_more_guests")
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(load_more_button)

        bot.send_message(user_id, guest_text, parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)
    else:
        bot.send_message(user_id, guest_text, parse_mode="HTML", disable_web_page_preview=True)

# Обработчик для кнопки "Загрузить ещё"
@bot.callback_query_handler(func=lambda call: call.data == "load_more_guests")
def handle_load_more_guests(call):
    user_id = call.from_user.id
    user_pages[user_id] += 1  # Увеличиваем номер текущей страницы

    handle_guest_button(call)  # Вызываем обработчик кнопки гостей для загрузки следующей страницы

@bot.callback_query_handler(func=lambda call: call.data == "contacts")
def handle_contacts(call):
    user_id = call.from_user.id

    # Отправьте информацию о контактах
    contacts_text = (
        "🌐 Telegram kanalimiz:\n @green_card_uzbekistan\n"
        "📸 Instagram kanalimiz:\n @green.card_uz\n"
        "📞 Telefon: +998998029699\n"
        "👤 Administrator: @CEK_PET\n"
        "📍 Bizning ofis: <a href='https://t.me/green_card_uzbekistan/281'>Lokatsiya</a>"
    )

    bot.send_message(user_id, contacts_text, parse_mode="HTML", disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "faq")
def handle_faq(call):
    user_id = call.from_user.id

    # Определение текущей страницы пользователя
    current_page = get_current_page(user_id)

    # Создаем словарь с вопросами и ссылками
    faq_dict = {
        "Q1": "«Green card» o’zi nima?",
        "Q2": "«Green card» ni nechta odam yutadi har yili?",
        "Q3": "«Green card» yutishning qanday sirlari, nozik taraflari bor?",
        "Q4": "«Green card» latareyasi qachon boshlanib, qachon tugidi?",
        "Q5": "«Green card» qanday o’ynaladi va necha pul to’lash kerak?",
        "Q6": "«Green card» latareyasi tekin bo’lsa, nima uchun turli joylarda turli hil narxlarda ro’yhatga olish uchun pul talab etiladi?",
        "Q7": "«Green card» lotoreyasida ishtirok etish uchun qanday hujjatlar kerak bo'ladi?",
        "Q8": "Nima uchun rasmga telefon orqali tushib yuborsa bo'lmaydi?",
        "Q9": "Oilali odam Grenn Card qanday o’ynaydi? Oila bilan o’ynashning nima afzalliklari bor?",
        "Q10": "Yutuq chiqqan yoki chiqmaganini qayerdan bilsa bo’ladi?",
        "Q11": "Green card uchun ofis ga borib regsitratsiya qilish bilan, telegram orqali registratsiya qilishning qanday farqi bor?",
        "Q12": "Agarda telegramdagi registratsiya bilan ofisdagi registratsiya bir hil bo’lsa nima uchun narxlar xar hil?",
        "Q13": "Nima uchun ayrim joylarda o’tgan yili latareyada qatnashgan odamning malumotlari saqlab qolinib, kelasi yili malumot egasi ogohlantirilmasdan uning nomidan oynash hollari kuzatiladi?",
        "Q14": "Siz Toshkent shahridan emasmisiz?",
        "Q15": "Grin karta o‘ynash uchun qandaydir savol javobdan o‘tish kerakmi?",
        "Q16": "Grin karta yutgandan keyin, yutuq sohiblariga Amerikada ish, uy joy beriladimi?",
        "Q17": "Grin Karta o‘ynash uchun necha yoshda bo‘lish kerak?",
        "Q18": "Grin Kartada ko‘proq Samarqandliklar yutadi, agar men ham Samarqandda o‘ynasam yoki Samarqandlik bo‘lsam yutishim osonmi?",
        "Q19": "Grin karta o‘ynash uchun Ingliz tilini bilish kerakmi?",
        "Q20": "Grin karta anketasini to‘ldirish tekin bo‘lsa nima uchun hujjat to‘ldirish uchun pul talab qilinadi?",
        "Q21": "Grin karta tizimi yasxshi ishlamasa bu qanchalik yomon?",
        "Q22": "Chet elda yurgan yurtdoshlarimiz qanday qilib Green Card o’ynaydi?",
        "Q23": "Green Card lotareysini rasmiylashtirish uchun asosiy litsenziyalangan ofis qayerda?",
        "Q24": "Sohta Green Card ofislari yoki ishonchli ofislar. Buni qanday bilsa bo’ladi?",
        "Q25": "Agar sizda chaqaloq bo’lsa uni qanday suratga olishni bilmayapsizmi?",
        "Q26": "Green Card lotareyasi Sentabr oyida takroriy oyinaladimi?",
        "Q27": "Hijobli ayol Green card uchun hijobini yechib tushishi shartmi?",
        "Q28": "Agar oila ajrashish arafasida turgan bo‘lsayu ammo hali rasman ajarshmagan bo‘lsa unday oila qanday lotareyada qatnashadi?",
        "Q29": "Green Card anketasidagi 6-bo'lim o'zi qanday bo'lim?",
        "Q30": "Green Card g'oliblari qanday harajatlarga tayyor bo'lishlari kerak?",
        "Q31": "Shar'iy nikohdagi oilalar...",
        "Q32": "Green Card yutuq chiqsa e-mailga xabar keladimi?",
        "Q33": "Ro'yhatdan o'tganimni qanday bilaman?!",
        "Q34": "Green Card lotareyasida yutish siri nimada?",
        "Q35": "Green Card javobini tekshirish qollanma video...",
        "Q36": "Ds-160 formasini to’ldirib B1/B2 visasiga suhbatga yozilishni istaganlar",
        "Q37": "Green Card anketasi to’ldirishdagi asosiy xatolar!",
        "Q38": "Green Card lotareyasida suratga tushish haqida qisqacha video.",
        "Q39": "Internetdagi turli anketa to’ldirishni o’rgatadigan videolar haqida.",
        "Q40": "Green card anketasida ro’yhatdan o’tgandan so’ng qanday hujjat olish kerak?",
        "Q41": "Green card anketasida yutuq chiqqandan so’ng qanday habar keladi?",
        "Q42": "Sudlanmaganlik haqida qanday hujjat kerak?",
        "Q43": "Talabalar uchun Work and Travel dasturi.",
        "Q44": "Green card yutgan odam qancha harajat qilishi haqida batafsil.",
        "Q45": "Nima uchun ayrim yutuq egalariga suhbat belgilanmayapti?",
        "Q46": "Confirmation qog’oz yo’qolgan bo’lsa qanday tekshiriladi?",
        "Q47": "Green Cardni qanday tekshirish, kod yoqolgan bo'lsa, qanday qilib tiklash va Green Card yutuq chiqsa, qanday ko'rinishda bo'lishi batafsil video.",
        "Q48": "Green Card yutganlar uchun 3 ta muhim tavsiya!",
        "Q49": "O’zgalar xatosidan ibrat olaylik!",
        "Q50": "Keys raqam (case number) katta bo’lgan fuqorolar diqqatiga!",
    }

    faq_links = {
        "Q1": "5",
        "Q2": "9",
        "Q3": "10",
        "Q4": "11",
        "Q5": "12",
        "Q6": "13",
        "Q7": "14",
        "Q8": "15",
        "Q9": "32",
        "Q10": "33",
        "Q11": "34",
        "Q12": "36",
        "Q13": "43",
        "Q14": "103",
        "Q15": "107",
        "Q16": "107",
        "Q17": "107",
        "Q18": "107",
        "Q19": "107",
        "Q20": "108",
        "Q21": "124",
        "Q22": "167",
        "Q23": "169",
        "Q24": "170",
        "Q25": "172",
        "Q26": "179",
        "Q27": "196",
        "Q28": "207",
        "Q29": "234",
        "Q30": "245",
        "Q31": "248",
        "Q32": "249",
        "Q33": "250",
        "Q34": "253",
        "Q35": "263",
        "Q36": "275",
        "Q37": "280",
        "Q38": "286",
        "Q39": "287",
        "Q40": "290",
        "Q41": "291",
        "Q42": "304",
        "Q43": "305",
        "Q44": "307",
        "Q45": "316",
        "Q46": "318",
        "Q47": "319",
        "Q48": "321",
        "Q49": "328",
        "Q50": "329",  # Здесь добавьте ссылку для Q50, если есть
    }

    items_per_page = 5  # Количество вопросов на одной странице
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page

    faq_message = f"📚 Eng ko'p beriladigan savollar (FAQ) \n  {current_page}-chi bet.\n\n"
    for key, value in list(faq_dict.items())[start_index:end_index]:
        faq_message += f"[{key}:] [\"{value}\"](https://t.me/green_card_uzbekistan/{faq_links[key]})\n"

    # Создаем клавиатуру с кнопками навигации
    navigation_buttons = telebot.types.InlineKeyboardMarkup()
    prev_button = telebot.types.InlineKeyboardButton("⬅️ Orqaga", callback_data="prev_page")
    next_button = telebot.types.InlineKeyboardButton("➡️ Oldinga", callback_data="next_page")
    navigation_buttons.row(prev_button, next_button)

    # Отправляем сообщение FAQ с клавиатурой навигации
    bot.send_message(user_id, faq_message, reply_markup=navigation_buttons, parse_mode='Markdown', disable_web_page_preview=True)

# ... Код для обработки кнопок навигации ...
# Обработчик для кнопок навигации
# Обработчик для кнопок навигации
# Функция для определения текущей страницы пользователя
def get_current_page(user_id):
    return user_pages.get(user_id, 1)

# Обработчик для кнопок навигации
@bot.callback_query_handler(func=lambda call: call.data in ["prev_page", "next_page"])
def handle_navigation_buttons(call):
    user_id = call.from_user.id

    # Получаем текущую страницу пользователя
    current_page = get_current_page(user_id)

    # Удаляем предыдущее сообщение с вопросами и ответами
    try:
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    except Exception as e:
        pass  # Обработка возможных ошибок удаления сообщения

    # Изменяем страницу в зависимости от нажатой кнопки
    if call.data == "prev_page":
        current_page = max(1, current_page - 1)
    elif call.data == "next_page":
        current_page += 1

    # Обновляем текущую страницу для пользователя
    user_pages[user_id] = current_page

    # Вызываем обработчик FAQ для отправки обновленного сообщения с новой страницей
    handle_faq(call)



@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def handle_check_subscription(call):
    user_id = call.from_user.id
    member = bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status == 'member' or member.status == 'creator':
        bot.answer_callback_query(call.id, "Siz kanalga a'zo bo'ldingiz!")

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        registration_button = types.InlineKeyboardButton("📝Registratsiyadan o'tish", callback_data="registration")
        ds_button = types.InlineKeyboardButton("ℹ️DS-160 va DS-260", callback_data="ds")  # Add this line
        result_button = types.InlineKeyboardButton("🏆 DV2024 natija", callback_data="result")  # Add this line
        guest_button = types.InlineKeyboardButton("👤 Mijozlarimiz", callback_data="guest")  # Add this line
        contacts_button = types.InlineKeyboardButton("📞Kontaktlar", callback_data="contacts")
        faq_button = types.InlineKeyboardButton("❓ FAQ", callback_data="faq")  # Add this line
        keyboard.add(registration_button, ds_button, result_button, guest_button, contacts_button, faq_button)  # Add faq_button

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    else:
        bot.answer_callback_query(call.id, "Siz kanalga a'zo bo'lmadingiz.")


@bot.callback_query_handler(func=lambda call: call.data == "registration")
def handle_registration(call):
    user_id = call.from_user.id

    if user_id in last_button_press_time:
        # Получаем время последнего нажатия кнопки
        last_press_time = last_button_press_time[user_id]

        # Определяем временной интервал, в течение которого повторное нажатие будет игнорироваться (например, 10 секунд)
        ignore_interval = timedelta(seconds=10)

        # Если прошло достаточно времени, разрешаем обработку кнопки
        if datetime.now() - last_press_time > ignore_interval:
            last_button_press_time[user_id] = datetime.now()
        else:
            # print("Ignoring button press due to recent press.")
            return
    else:
        # Если это первое нажатие, сохраняем текущее время
        last_button_press_time[user_id] = datetime.now()

    try:
        # Попытка удаления сообщения
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        # Обработка ошибки, если сообщение уже удалено
        if "Bad Request: message to delete not found" not in str(e):
            print("Error deleting message:", e)

    bot.send_message(user_id,
                     "Siz ro'yxatdan o'tish bo'limidasiz.\n\n1⃣Birinchi qadam, Passportingiz rasimini yuboring.")
    bot.register_next_step_handler_by_chat_id(user_id, process_passport_photo)

def process_passport_photo(message):
    user_id = message.from_user.id

    # Check if the message contains a photo
    if message.content_type == 'photo':
        # Assuming the user sent a photo, you can access the file_id of the photo from the message object
        file_id = message.photo[-1].file_id

        # Store the file_id in the registration data
        registration_data[user_id] = {'passport_photo': file_id}

        # URL фотографии на канале
        photo_url = 'https://t.me/green_card_uzbekistan/17'

        # Создаем HTML-разметку для текста с вставленной фотографией и превью-изображением
        message_text = f"5x5ga oq fonda rasimnigizni yuboring.\n\n🎞(Namunaviy sur'at) 👇\n<a href='{photo_url}'>&#8205;</a>"
        # В этой разметке &#8205; представляет нулевой неразрывный пробел, чтобы HTML-разметка сработала

        # Отправляем сообщение с HTML-разметкой
        bot.send_message(user_id, message_text, parse_mode='HTML')

        # Регистрируем следующий шаг для обработки фотографии на белом фоне
        bot.register_next_step_handler_by_chat_id(user_id, process_white_background_photo)
    else:
        # If the user did not send a photo, prompt them again
        bot.send_message(user_id, "Xato. Passport rasimingizni yuboring.")
        bot.register_next_step_handler_by_chat_id(user_id, process_passport_photo)

def process_white_background_photo(message):
    user_id = message.from_user.id

    # Check if the message contains a photo
    if message.content_type == 'photo':
        # Assuming the user sent a photo, you can access the file_id of the photo from the message object
        file_id = message.photo[-1].file_id

        # Store the file_id in the registration data
        registration_data[user_id]['passport_white_background_photo'] = file_id

        # Ask the user about their marital status with buttons
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("Bo'ydoq/Turmush qurmagan", callback_data="marital_status_single"),
            types.InlineKeyboardButton("Oilali", callback_data="marital_status_married"),
            types.InlineKeyboardButton("Ajrashgan", callback_data="marital_status_divorced"),
            types.InlineKeyboardButton("Beva", callback_data="marital_status_widow"),
            types.InlineKeyboardButton("Ajrashish arafasida", callback_data="marital_status_separated")
        )
        bot.send_message(user_id, "Oilaviy holatingizni tanlang:", reply_markup=keyboard)
    else:
        # If the user did not send a photo, prompt them again
        bot.send_message(user_id, "Xato. 5x5 oq fonda rasimingizni yuboring.")
        bot.register_next_step_handler_by_chat_id(user_id, process_white_background_photo)


@bot.callback_query_handler(func=lambda call: call.data.startswith("marital_status_"))
def handle_marital_status(call):
    user_id = call.from_user.id
    marital_status = call.data[len("marital_status_"):]

    # Save the marital status in the registration data
    registration_data[user_id]['marital_status'] = marital_status

    # Delete the original message with the inline buttons
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        print(f"An error occurred while deleting the message: {e}")

    if marital_status == 'single':
        bot.send_message(user_id, "Siz Bo'ydoq/Turmush qurmaganni tanladingiz.")
        # If the user is single, ask about the education level
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton("9-sinfni bitirganman", callback_data="education_9_class"),
            types.InlineKeyboardButton("11-sinfda o'qimoqdaman", callback_data="education_11_class"),
            types.InlineKeyboardButton("11-sinfni bitirganman", callback_data="education_completed_11_class"),
            types.InlineKeyboardButton("Litsey/kollejni bitirganman", callback_data="education_lic_col"),
            types.InlineKeyboardButton("Institutda o'qimoqdaman", callback_data="education_university"),
            types.InlineKeyboardButton("Institutni bitirganman", callback_data="education_univ_grad"),
            types.InlineKeyboardButton("Magistraturada o'qimoqdaman", callback_data="education_grad_school"),
            types.InlineKeyboardButton("Magistraturani bitirganman", callback_data="education_grad_school_grad"),
            types.InlineKeyboardButton("Doktoranturada o'qimoqdaman", callback_data="education_doctorate_school"),
            types.InlineKeyboardButton("Doktoranturani bitirganman", callback_data="education_doctorate_grad"),
            types.InlineKeyboardButton("Boshqa variant", callback_data="education_other")
        )
        bot.send_message(user_id, "Ma'lumotingizni tanlang", reply_markup=keyboard)
    elif marital_status == 'married':
        # If the user is married, ask for the spouse's passport photo
        bot.send_message(user_id, "Siz Oilalini tanladingiz. Turmush o'rtog'ingiz passport rasimini yuboring.")
        # Register the next step to process the spouse's passport photo
        bot.register_next_step_handler_by_chat_id(user_id, process_spouse_passport_photo)
    elif marital_status == 'divorced':
        # If the user is divorced, ask about the number of children
        bot.send_message(user_id, "Siz Ajrashganni tanladingiz.\n\n21 yoshgacha bo'lgan amerika fuqarosi bo'lmagan nechta farzandingiz bor?\n\nFarzand siz bilan birga yashamasa ham, uni ko'rsatish shart")
        # Register the next step to process the number of children
        bot.register_next_step_handler_by_chat_id(user_id, process_number_of_children)
    elif marital_status == 'widow':
        # If the user is a widow/widower, ask about the number of children
        bot.send_message(user_id, "Siz bevani tanladingiz. \n\n21 yoshgacha bo'lgan amerika fuqarosi bo'lmagan nechta farzandingiz bor?\n\nFarzand siz bilan birga yashamasa ham, uni ko'rsatish shart")
        # Register the next step to process the number of children
        bot.register_next_step_handler_by_chat_id(user_id, process_number_of_children)
    elif marital_status == 'separated':
        # If the user is separated, ask about the number of children
        bot.send_message(user_id, "Siz Ajrashish arafasidani tanladingiz'. \n\n21 yoshgacha bo'lgan amerika fuqarosi bo'lmagan nechta farzandingiz bor?\n\nFarzand siz bilan birga yashamasa ham, uni ko'rsatish shart")
        # Register the next step to process the number of children
        bot.register_next_step_handler_by_chat_id(user_id, process_number_of_children)
    else:
        # If the user is not married, divorced, a widow/widower, or separated, complete the registration
        complete_registration(user_id)

# ... (rest of the code remains unchanged)
def process_spouse_passport_photo(message):
    user_id = message.from_user.id

    # Check if the message contains a photo
    if message.content_type == 'photo':
        # Assuming the user sent a photo, you can access the file_id of the photo from the message object
        file_id = message.photo[-1].file_id

        # Store the file_id in the registration data
        registration_data[user_id]['spouse_passport_photo'] = file_id

        # Create a clickable link with the thumbnail preview
        link_text = "<a href='https://t.me/green_card_uzbekistan/17'>Turmush o'rtog'ingizni oq fonda 5x5 rasimini yuboring\nNamuna👇</a>"

        # Send the message with the link and the thumbnail preview
        bot.send_message(user_id, link_text, parse_mode="HTML")

        # Register the next step to process the spouse's photo on a white background
        bot.register_next_step_handler_by_chat_id(user_id, process_spouse_white_background_photo)
    else:
        # If the user did not send a photo, prompt them again
        bot.send_message(user_id, "Turmush o'rtog'ingizni passportini yuboring.")
        bot.register_next_step_handler_by_chat_id(user_id, process_spouse_passport_photo)


def process_spouse_white_background_photo(message):
    user_id = message.from_user.id

    # Check if the message contains a photo
    if message.content_type == 'photo':
        # Assuming the user sent a photo, you can access the file_id of the photo from the message object
        file_id = message.photo[-1].file_id

        # Store the file_id in the registration data
        registration_data[user_id]['spouse_white_background_photo'] = file_id

        # Ask the user about the number of children
        bot.send_message(user_id, "21 yoshgacha bo'lgan amerika fuqarosi bo'lmagan nechta farzandingiz bor?")
        # Register the next step to process the number of children
        bot.register_next_step_handler_by_chat_id(user_id, process_number_of_children)
    else:
        # If the user did not send a photo, prompt them again
        bot.send_message(user_id, "Turmush o'rtog'ingizni oq fonda 5x5 rasimini yuboring.")
        bot.register_next_step_handler_by_chat_id(user_id, process_spouse_white_background_photo)

def process_number_of_children(message):
    user_id = message.from_user.id
    # Assuming the user sent a text message, you can access the number of children from the message text
    number_of_children = message.text
    # Сохраняем количество детей в registration_data
    registration_data[user_id]['children_count'] = message.text


    # Check if the user provided a valid number
    if number_of_children is not None and number_of_children.isdigit():
        # Store the number of children in the registration data
        registration_data[user_id]['number_of_children'] = number_of_children

        num_children = int(number_of_children)
        if num_children > 0:
            bot.send_message(user_id, "Farzandaringiz metrika/passportlarini birma-bir yuboring.")
            # Register the next step to process the photos of children's height markers
            # Initialize the list to store photos
            registration_data[user_id]['children_height_markers'] = []
            bot.register_next_step_handler_by_chat_id(user_id, process_children_height_markers, num_children)
        else:
            # If the user has no children, ask for their education level directly
            bot.send_message(user_id, "Siz farzandim yo'q deb belgiladingiz. Ma'lumotingizni tanlang:")
            # Ask the user about their education level with buttons
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton("9-sinfni bitirganman", callback_data="education_9_class"),
                types.InlineKeyboardButton("11-sinfda o'qimoqdaman", callback_data="education_11_class"),
                types.InlineKeyboardButton("11-sinfni bitirganman", callback_data="education_completed_11_class"),
                types.InlineKeyboardButton("Litsey/kollejni bitirganman", callback_data="education_lic_col"),
                types.InlineKeyboardButton("Institutda o'qimoqdaman", callback_data="education_university"),
                types.InlineKeyboardButton("Institutni bitirganman", callback_data="education_univ_grad"),
                types.InlineKeyboardButton("Magistraturada o'qimoqdaman", callback_data="education_grad_school"),
                types.InlineKeyboardButton("Magistraturani bitirganman", callback_data="education_grad_school_grad"),
                types.InlineKeyboardButton("Doktoranturada o'qimoqdaman", callback_data="education_doctorate_school"),
                types.InlineKeyboardButton("Doktoranturani bitirganman", callback_data="education_doctorate_grad"),
                types.InlineKeyboardButton("Boshqa variant", callback_data="education_other")
            )
            bot.send_message(user_id, "Ma'lumotingizni tanlang", reply_markup=keyboard)
    else:
        # If the user did not provide a valid number, ask them to send a correct number
        bot.send_message(user_id, "Noto'g'ri qiymat kiritildi. Iltimos, to'g'ri biror son kiriting.")
        # Ask the user again about the number of children
        bot.register_next_step_handler_by_chat_id(user_id, process_number_of_children)

def process_children_height_markers(message, num_children):
    user_id = message.from_user.id
    photo = None

    # Check if the message contains a photo
    if message.content_type == 'photo':
        photo = message.photo[-1].file_id

    if photo:
        # Store the photo in the registration data
        registration_data[user_id]['children_height_markers'].append(photo)

    # Check if we have received all the required photos
    if len(registration_data[user_id]['children_height_markers']) == num_children:
        # Ask the user to send photos of their children on a white background
        bot.send_message(user_id, "Endi farzandlaringiz 5x5 oq fonda rasmlarini birma-bir yuboring.")
        # Register the next step to process the photos of children on a white background
        bot.register_next_step_handler_by_chat_id(user_id, process_children_white_background_photos, num_children)
    else:
        remaining_children = num_children - len(registration_data[user_id]['children_height_markers'])
        bot.send_message(user_id, f"Yana {remaining_children}ta {'s' if remaining_children > 1 else ''} metrika/passport yuboring.")
        # Register the next step to continue receiving photos of children's height markers
        bot.register_next_step_handler_by_chat_id(user_id, process_children_height_markers, num_children)

def process_children_white_background_photos(message, num_children):
    user_id = message.from_user.id
    photo = None

    # Check if the message contains a photo
    if message.content_type == 'photo' and message.photo:
        photo = message.photo[-1].file_id

    if photo:
        # Store the photo in the registration data
        registration_data[user_id].setdefault('children_white_background_photos', []).append(photo)

    # Check if we have received all the required photos
    if len(registration_data[user_id].get('children_white_background_photos', [])) == num_children:
        # Ask for the user's education level
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton("9-sinfni bitirganman", callback_data="education_9_class"),
            types.InlineKeyboardButton("11-sinfda o'qimoqdaman", callback_data="education_11_class"),
            types.InlineKeyboardButton("11-sinfni bitirganman", callback_data="education_completed_11_class"),
            types.InlineKeyboardButton("Litsey/kollejni bitirganman", callback_data="education_lic_col"),
            types.InlineKeyboardButton("Institutda o'qimoqdaman", callback_data="education_university"),
            types.InlineKeyboardButton("Institutni bitirganman", callback_data="education_univ_grad"),
            types.InlineKeyboardButton("Magistraturada o'qimoqdaman", callback_data="education_grad_school"),
            types.InlineKeyboardButton("Magistraturani bitirganman", callback_data="education_grad_school_grad"),
            types.InlineKeyboardButton("Doktoranturada o'qimoqdaman", callback_data="education_doctorate_school"),
            types.InlineKeyboardButton("Doktoranturani bitirganman", callback_data="education_doctorate_grad"),
            types.InlineKeyboardButton("Boshqa variant", callback_data="education_other")
        )
        bot.send_message(user_id, "Ma'lumotingzini tanlang:", reply_markup=keyboard)
    else:
        remaining_children = num_children - len(registration_data[user_id].get('children_white_background_photos', []))
        bot.send_message(user_id, f"Yana {remaining_children}ta {'s' if remaining_children > 1 else ''} 5x5 oq fonda rasim yuboring.")
        # Register the next step to continue receiving photos of children on a white background
        bot.register_next_step_handler_by_chat_id(user_id, process_children_white_background_photos, num_children)


@bot.callback_query_handler(func=lambda call: call.data.startswith("education_"))
def handle_education_level(call):
    user_id = call.from_user.id

    if hasattr(call.message, "text"):
        education_level = call.data.split("_", 1)[-1]
        # Store the education level in the registration data
        registration_data[user_id]['education_level'] = education_level

        # Construct a message based on the selected education level
        education_messages = {
            "9_class": "9-sinfni bitirganman",
            "11_class": "11-sinfda o'qimoqdaman",
            "completed_11_class": "11-sinfni bitirganman",
            "lic_col": "Litsey/kollejni bitirganman",
            "university": "Institutda o'qimoqdaman",
            "univ_grad": "Institutni bitirganman",
            "grad_school": "Magistraturada o'qimoqdaman",
            "grad_school_grad": "Magistraturani bitirganman",
            "doctorate_school": "Doktoranturada o'qimoqdaman",
            "doctorate_grad": "Doktoranturani bitirganman",
            "other": "Boshqa variant"
        }

        education_message = education_messages.get(education_level, "Invalid education level")

        try:
            # Edit the original message to remove the buttons and display the selected education level
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Siz '{education_message}'ni tanladingiz",
            )
        except telebot.apihelper.ApiTelegramException as e:
            print(f"An error occurred while editing the message: {e}")

        if education_level == 'completed_11_class':
            # If the user completed 11th grade, ask for their address
            bot.send_message(user_id, "🏠Hozirda yashayotgan manzilingiz:\n\n❗️(Shahar, tuman, ko'cha nomi, uy nomeri")
            # Register the next step to process the address
            bot.register_next_step_handler_by_chat_id(user_id, process_address)
        else:
            # For all other education levels, ask for the address directly
            bot.send_message(user_id, "🏠Hozirda yashayotgan manzilingiz:\n\n❗️(Shahar, tuman, ko'cha nomi, uy nomeri")
            # Register the next step to process the address
            bot.register_next_step_handler_by_chat_id(user_id, process_address)
    else:
        # Handle the case when call.message.text is not available
        bot.send_message(user_id, "Xatolik yuz berdi.")
        # You can take appropriate action here or log the error for further investigation.


def process_address(message):
    user_id = message.from_user.id
    address = message.text

    # Store the address in the registration data
    registration_data[user_id]['address'] = address

    # Ask for the user's phone number
    bot.send_message(user_id, "📞Telefon raqamingizni kiriting:")
    # Register the next step to process the phone number
    bot.register_next_step_handler_by_chat_id(user_id, process_phone_number)

def process_phone_number(message):
    user_id = message.from_user.id
    phone_number = message.text

    # Store the phone number in the registration data
    registration_data[user_id]['phone_number'] = phone_number

    # Ask for the user's Gmail address
    bot.send_message(user_id, "📂Emailingizni kiriting:\n\nAgar emailingiz yo'q bo'lsa, yo'q deb yozing.")
    # Register the next step to process the Gmail address
    bot.register_next_step_handler_by_chat_id(user_id, process_gmail_address)

def process_gmail_address(message):
    user_id = message.from_user.id
    gmail_address = message.text

    # Store the Gmail address in the registration data
    registration_data[user_id]['gmail_address'] = gmail_address

    # Call the complete_registration function
    complete_registration(user_id)

# Функция для завершения регистрации и отправки данных в канал
def complete_registration(user_id):
    user_data = registration_data.get(user_id, {})

    if user_data.get('passport_photo'):
        bot.send_photo(SUBSCRIBER_INFO, user_data['passport_photo'])

    if user_data.get('passport_white_background_photo'):
        bot.send_photo(SUBSCRIBER_INFO, user_data['passport_white_background_photo'])

    if user_data.get('spouse_passport_photo'):
        bot.send_photo(SUBSCRIBER_INFO, user_data['spouse_passport_photo'])

    if user_data.get('spouse_white_background_photo'):
        bot.send_photo(SUBSCRIBER_INFO, user_data['spouse_white_background_photo'])

    children_height_markers = user_data.get('children_height_markers', [])
    for photo in children_height_markers:
        bot.send_photo(SUBSCRIBER_INFO, photo)

    children_white_background_photos = user_data.get('children_white_background_photos', [])
    for photo in children_white_background_photos:
        bot.send_photo(SUBSCRIBER_INFO, photo)

    try:
        user_info = bot.get_chat(user_id)

        message_text = f"Yangi registratsiya:\n\n" \
                       f"User: {user_id}\n" \
                       f"Username: @{user_info.username}\n" \
                       f"Oilaviy ahvoli: {user_data.get('marital_status', 'N/A')}\n" \
                       f"Bolalar soni: {user_data.get('children_count', 'N/A')}\n" \
                       f"Ma'lumoti: {user_data.get('education_level', 'N/A')}\n" \
                       f"Telefon: {user_data.get('phone_number', 'N/A')}\n" \
                       f"Email: {user_data.get('gmail_address', 'N/A')}\n"

        bot.send_message(SUBSCRIBER_INFO, message_text)

        bot.send_message(user_id, "✅Arizangiz qabul qilindi.\n\nRo'yxatga olish faqat Oktyabr va Noyabr oylari oralig'ida amalga oshiriladi. Biz siz bilan ro'yhatga olish boshlanganda yana aloqaga chiqamiz. Royhatga olinganingizdan so'ng sizga tasdiqlovchi kod (Confirmation number) yuboramiz.")
    except Exception as e:
        bot.send_message(user_id, "Ma'lumot qabul qilishda xato bor")
        # print("Error sending data to channel:", e)

# Start the bot
bot.polling()