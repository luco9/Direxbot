import os
import random
import threading
import time
from pytube import YouTube
from youtube_search import YoutubeSearch
from gtts import gTTS
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from telebot.types import Message
from urllib.parse import quote
import imageio
from telebot.types import ChatPermissions
import wikipediaapi
from google_images_search import GoogleImagesSearch
from translate import Translator
from PIL import Image, ImageDraw, ImageFont
import io
from telebot import types
import requests
from io import BytesIO
import re
from telebot import types
import telebot
from telebot.types import ChatMemberStatus
import json
#تعريفات ضرورية
API_KEY = '3724df92637d2b3aaab56a679961cf89'
Token = '7091131799:AAHhWet-rtp8zP48g9YUxfD1yKO662Gd228'
bot = telebot.TeleBot(Token)

words_list = [
    'python',
    'programming',
    'computer',
    'keyboard',
    'algorithm',
    'telegram',
    'internet',
    'technology',
    'developer',
    'android',
    'database',
    'java',
    'script',
    'language',
    'library',
    'variable',
    'function',
    'class',
    'object',
    'inheritance',
    'polymorphism',
    'encapsulation',
    'abstraction'
]

answers = ['الماء', '1', 'برلين', 'بنز Patent-Motorwagen', '1939', 'إسحاق نيوتن', 'توماس إديسون', 'الدراسة العلمية للكائنات الحية', 'باريس', 'بيل غيتس']
questions = [
    ('ما هو أساس الحياة على الأرض؟', 'الماء'),
    ('ما هو ناتج 1 + 1؟', '1'),
    ('ما هي عاصمة ألمانيا؟', 'برلين'),
    ('ما هي أول سيارة محركة؟', 'بنز Patent-Motorwagen'),
    ('في أي عام بدأت الحرب العالمية الثانية؟', '1939'),
    ('من هو اكتشف قانون الجاذبية؟', 'إسحاق نيوتن'),
    ('من اخترع اللمبة الكهربائية؟', 'توماس إديسون'),
    ('ما هي البيولوجيا؟', 'الدراسة العلمية للكائنات الحية'),
    ('ما هي عاصمة فرنسا؟', 'باريس'),
    ('من هو مؤسس شركة مايكروسوفت؟', 'بيل غيتس')
]
def save_scores(scores):
    with open('scores.txt', 'w') as file:
        for user_id, score in scores.items():
            file.write(f'{user_id}:{score}\n')

def load_scores():
    scores = {}
    if os.path.exists('scores.txt'):
        with open('scores.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                user_id, score = line.strip().split(':')
                scores[int(user_id)] = int(score)
    return scores
@bot.message_handler(commands=['leave'])
def leave_chat(message):
    if message.from_user.id == 1045489068:
        bot.send_message(message.chat.id, 'Good Bay')
        bot.leave_chat(message.chat.id)

@bot.message_handler(regexp='^ايدي')
def id(message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        user_id = user.id
        username = user.username
        full_name = user.full_name
        bio = user.bio if hasattr(user, 'bio') else "No bio available"
        user_photos = bot.get_user_profile_photos(user_id)
        num_photos = user_photos.total_count  # عدد الصور


        fancy_id = f"🆔 User ID: {user_id}"
        fancy_username = f"👤 @{username}"
        fancy_full_name = f"📛 Full Name: {full_name}"
        fancy_bio = f"📝 Bio: {bio}"
        fancy_num_photos = f"🖼️ Number of Photos: {num_photos}"

        if user_photos.photos:
            file_id = user_photos.photos[0][-1].file_id  # المعرف الفعلي للصورة
            bot.send_photo(message.chat.id, file_id, caption=f'{fancy_id}\n{fancy_username}\n{fancy_full_name}\n{fancy_bio}\n{fancy_num_photos}')
        else:
            bot.reply_to(message, f'''
            *{fancy_id}*
            *{fancy_username}*
            *{fancy_full_name}*
            *{fancy_bio}*
            *{fancy_num_photos}*
            ''', parse_mode='markdown')
    else:
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        bio = message.from_user.bio if hasattr(message.from_user, 'bio') else "No bio available"
        user_photos = bot.get_user_profile_photos(user_id)
        num_photos = user_photos.total_count  # عدد الصور


        fancy_id = f"🆔 User ID: {user_id}"
        fancy_username = f"👤 @{username}"
        fancy_full_name = f"📛 Full Name: {full_name}"
        fancy_bio = f"📝 Bio: {bio}"
        fancy_num_photos = f"🖼️ Number of Photos: {num_photos}"

        if user_photos.photos:
            file_id = user_photos.photos[0][-1].file_id  
            bot.send_photo(message.chat.id, file_id, caption=f'{fancy_id}\n{fancy_username}\n{fancy_full_name}\n{fancy_bio}\n{fancy_num_photos}')
        else:
            bot.reply_to(message, f'''
            *{fancy_id}*
            *{fancy_username}*
            *{fancy_full_name}*
            *{fancy_bio}*
            *{fancy_num_photos}*
            ''', parse_mode='markdown')


#ميزه عدم كتم المطور
@bot.message_handler(func=lambda message: message.text.startswith('كتم'))
def mute_user(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if bot_member.status in ['administrator', 'creator']:
            # التحقق مما إذا كان المستخدم هو المطور
            if user_id != 1045489068:  # استبدل DEVELOPER_ID بمعرف المطور الخاص بك
                bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
                bot.reply_to(message, f"تم كتم المستخدم بنجاح.")
            else:
                bot.reply_to(message, "لا يمكنك كتم المطور.")
        else:
            bot.reply_to(message, "لا يمكنك استخدام هذا الأمر.")
    else:
        bot.reply_to(message, "الرجاء الرد على رسالة المستخدم الذي تريد كتمه.")

# معرف الصورة المراد إرسالها عند كتم المستخدم
mute_image_id = "AgACAgIAAxkBAAMJZxAeniCYoGkZP4q_GSlnd4ea8-AAAnvjMRtp4oFIIwhnrDhZ4FIBAAMCAAN4AAM2BA"  # استبدل بـ file_id للصورة عند الكتم
unmute_image_id = "AgACAgIAAxkBAAMOZxAe9p4KpQSKL9fRmfs5SKWHC5wAAn3jMRtp4oFIN5Je7XIkOUcBAAMCAAN4AAM2BA"  # استبدل بـ file_id للصورة عند إلغاء الكتم
# قائمة المطورين الذين يستطيعون رفع الأعضاء (معرفاتهم)
developers = [1045489068]  # ضع هنا معرفات المطورين

# ملف JSON لحفظ الرتب
ROLES_FILE = 'roles.json'

# تحميل الرتب المخزنة من ملف JSON
def load_roles():
    try:
        with open(ROLES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # إذا لم يكن الملف موجوداً، نبدأ بقاموس فارغ

# حفظ الرتب إلى ملف JSON
def save_roles():
    with open(ROLES_FILE, 'w') as file:
        json.dump(user_roles, file)

# تحميل الرتب عند بدء تشغيل البوت
user_roles = load_roles()

# دالة للتحقق إذا كان المستخدم مالك أو مطور
def is_owner_or_developer(chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    if chat_member.status == ChatMemberStatus.OWNER or user_id in developers:
        return True
    return False

# دالة لترقية عضو إلى رتبة معينة
def promote_user(chat_id, user_id, role):
    if role == 'admin':
        user_roles[user_id] = 'admin'
        bot.send_message(chat_id, f"تم ترقية المستخدم إلى أدمن.")
    elif role == 'manager':
        user_roles[user_id] = 'manager'
        bot.send_message(chat_id, f"تم ترقية المستخدم إلى مدير.")
    elif role == 'vip':
        user_roles[user_id] = 'vip'
        bot.send_message(chat_id, f"تم ترقية المستخدم إلى مميز.")
    else:
        bot.send_message(chat_id, "رتبة غير معروفة!")
    save_roles()  # حفظ الرتب بعد أي ترقية

# دالة لتنزيل عضو من رتبة معينة
def demote_user(chat_id, user_id, role):
    if user_id in user_roles and user_roles[user_id] == role:
        del user_roles[user_id]
        bot.send_message(chat_id, f"تم تنزيل المستخدم من {role}.")
        save_roles()  # حفظ الرتب بعد أي تنزيل
    else:
        bot.send_message(chat_id, "المستخدم لا يملك هذه الرتبة.")

# دالة للتحقق من صلاحيات المستخدم في البوت
def can_mute_user(chat_id, from_user_id, target_user_id):
    if from_user_id == target_user_id:
        return False  # لا يمكن للمستخدم كتم نفسه
    if target_user_id not in user_roles:
        return True  # إذا كان العضو بدون رتبة، يمكن كتمه
    if user_roles[target_user_id] == 'manager':
        bot.send_message(chat_id, "لا يمكن كتم المدير.")
        return False
    if user_roles[target_user_id] == 'admin':
        bot.send_message(chat_id, "لا يمكن كتم الأدمن.")
        return False
    return True  # يسمح بكتم المميز أو العضو العادي

# دالة للتحقق إذا المستخدم مطور أو مالك
def cannot_mute_developer_or_owner(chat_id, user_id):
    if user_id in developers:
        return True

    # نشوف إذا المستخدم هو المالك (أدمن أساسي)
    chat_member = bot.get_chat_member(chat_id, user_id)
    return chat_member.status == "creator"

# أمر لكتم المستخدم
@bot.message_handler(func=lambda message: message.text and message.text.lower() == "كتم")
def mute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ لازم ترد على رسالة الشخص الي تريد تكتمه.")
        return

    user_id = message.reply_to_message.from_user.id

    # تحقق إذا المطور أو المالك حتى ما نكتمه
    if cannot_mute_developer_or_owner(message.chat.id, user_id):
        bot.reply_to(message, "❌ ما تگدر تكتم المطور أو المالك!")
        return

    # تحقق من الرتبة (لا يمكن كتم المدير أو الأدمن)
    if not can_mute_user(message.chat.id, message.from_user.id, user_id):
        return

    try:
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)

        # إرسال الصورة مع رسالة الكتم
        bot.send_photo(
            chat_id=message.chat.id,
            photo=MUTE_PHOTO_FILE_ID,
            caption=f"✅ تم كتم المستخدم {message.reply_to_message.from_user.first_name} بنجاح."
        )
    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ: {str(e)}")

# أمر لإلغاء الكتم عن المستخدم
@bot.message_handler(func=lambda message: message.text and message.text.lower() == "الغاء الكتم")
def unmute_user(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ لازم ترد على رسالة الشخص الي تريد ترفع الكتم عنه.")
        return

    user_id = message.reply_to_message.from_user.id

    try:
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True)

        # إرسال الصورة مع رسالة إلغاء الكتم
        bot.send_photo(
            chat_id=message.chat.id,
            photo=UNMUTE_PHOTO_FILE_ID,
            caption=f"✅ تم إلغاء كتم المستخدم {message.reply_to_message.from_user.first_name} بنجاح."
        )
    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ: {str(e)}")

# دالة للتحقق إذا كان المستخدم مشرف
def is_admin(chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    return chat_member.status in ["administrator", "creator"]

# الأوامر تكون فقط للمشرفين
@bot.message_handler(func=lambda message: message.text.lower() in ["كتم", "الغاء الكتم"])
def handle_admin_commands(message):
    if is_admin(message.chat.id, message.from_user.id):
        if message.text.lower() == "كتم":
            mute_user(message)
        elif message.text.lower() == "الغاء الكتم":
            unmute_user(message)
    else:
        bot.reply_to(message, "❌ هاي الأوامر فقط للمشرفين!")

@bot.message_handler(regexp='^طرد')
def kick_user(message):
    if message.from_user.id == 1045489068:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            bot.kick_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id, f'تم طرد هذا العضو : {user_id}')

@bot.message_handler(regexp='^رتبتي')
def check_rank(message):
    user_id = message.from_user.id
    if user_id == 1045489068:
        bot.send_message(message.chat.id, '<strong>رتبتك هي [مالك]</strong>', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, '<strong>رتبتك هي [عضو]</strong>', parse_mode='HTML')

@bot.message_handler(regexp='^اوامر البوت')
def bot_commands(message):
    kl = '''
    1- (ايدي) لاظهار معلوماتك
    2- (طرد) طرد الاشخاص لازم عندك صلاحية 
    3- (كتم) تقييد الاشخاص من الحجي لازم عندك صلاحية
    4- (لعبة ترتيب الاحرف) جربها بنفسك
    5- (ايموجي) جربها بنفسك
    6 (ترجم) يترجم نص الانكليزي
    7 (لعبة التفكيك ) جربها بنفسك
    8- ( الطقس + Bahghdad) طقس بغداد فقط حاليا
    9- (فيلم) ينطيك افلام متنوعه جربوا كلش حلو
    10- (انطق + الكلام) واضح 
    11- (ملصق +الرد على صورة) امر جدا غريب يحول الصورة الى ملصق والملصق مو عادي جربوا
    12- (صورة + الرد على ملصق) واضح
    13- (كوكل + السؤال) ايضا واضح
    14- (اكتبلي + نص الانكليزي) جربوا غريب جدا
    15- (بحث صور + الشي بالانكليزي) ملاحظه يعطيك صورة واحد وليس من كوكل
    16- (ماذا + اسم شخصية معينة) مثال: ماذا+فلاديمير بوتين
    17- (يوت + اسم الاغنية) لازم تكون دقيق ب اسم الاغنية او الشي الي تريدة يرسل الك ملف صوتي
    18- (يوت1 + اسم الفيديو) يرسلك الفيديو كامل ل الشي تريده من يوتيوب
    '''
    bot.send_message(message.chat.id, f'<strong>{kl}</strong>', parse_mode='html')

@bot.message_handler(func=lambda message: message.text == 'لعبة البوت')
def ask_question(message):
          question_number = len(questions)
          if question_number > 0:
              current_question = questions.pop(0)
              question_text, correct_answer = current_question
              bot.send_message(message.chat.id, f'سؤال: {question_text}')
              bot.register_next_step_handler(message, lambda msg: check_answer(msg, correct_answer))
          else:
              bot.send_message(message.chat.id, 'تم الانتهاء من الأسئلة!')

def check_answer(message, correct_answer):
          user_answer = message.text
          if user_answer.lower() == correct_answer.lower():
              bot.reply_to(message, 'إجابة صحيحة! +1 نقطة')
          # لا تقوم بإرسال رسالة عندما تكون الإجابة خاطئة


@bot.message_handler(func=lambda message: message.text == 'لعبة ترتيب الأحرف')
def start_game(message):
    word_list = ['كتاب', 'قلم', 'دفتر', 'مدرسة', 'معلم', 'طالب', 'دراسة']
    random_word = random.choice(word_list)
    shuffled_word = ''.join(random.sample(random_word, len(random_word)))
    bot.send_message(message.chat.id, f'كلمة مختلطة: {shuffled_word}')
    bot.register_next_step_handler(message, check_answer, random_word)

def check_answer(message, correct_word):
    user_answer = message.text
    if user_answer == correct_word:
        bot.reply_to(message, 'إجابة صحيحة! +1 نقطة')
    else:
        bot.reply_to(message, f'إجابة خاطئة! الإجابة الصحيحة هي: {correct_word}')                

emojis = ["😀", "😍", "😎", "🤩", "😂", "🥳", "🤠", "😇", "🤓", "😜", "🦩", "🌻", "🌼", "🌸", "🌺", "🌾", "🌿", "🍄", "🌰", "🐾", "🕊️", "🦢", "🐚", "🌍", "🌏", "🌋", "🌄", "🌠", "🌌", "🚀", "🌌", "🛰️", "🪐", "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "☀️", "🌞" ]

TIME_LIMIT = 30  # وقت اللعبة بالثواني

game_active = False  # متغير عالمي لتتبع حالة اللعبة
current_emoji = None  # متغير عالمي لتخزين الإيموجي الحالي
start_time = None  # متغير عالمي لتخزين وقت بدء اللعبة

@bot.message_handler(regexp='^ايموجي')
def start_emoji_game(message):
    global game_active
    global current_emoji
    global start_time

    if not game_active:
        current_emoji = random.choice(emojis)
        bot.send_message(message.chat.id, f"ها قد بدأنا! هل يمكنك إرسال هذا الإيموجي في النفس الصحيح؟ {current_emoji}")

        start_time = time.time()  # تسجيل وقت بدء اللعبة

        # بدء مؤقت زمني
        timer_thread = threading.Thread(target=game_timer, args=(message.chat.id,))
        timer_thread.start()

        game_active = True
    else:
        bot.send_message(message.chat.id, "اللعبة مستمرة حاليًا، يرجى انتظار الجولة الحالية.")

def game_timer(chat_id):
    global game_active

    time.sleep(TIME_LIMIT)

    if game_active:
        game_active = False
        bot.send_message(chat_id, "انتهى الوقت! للأسف، لم تتمكن من الرد في الوقت المحدد.")

@bot.message_handler(func=lambda message: message.text in emojis)
def check_winner(message):
    global game_active
    global start_time

    if game_active:
        if message.text == current_emoji:
            elapsed_time = time.time() - start_time  # حساب وقت استغراق اللاعب
            elapsed_time = round(elapsed_time, 2)  # تقريب الوقت لرقمين بعد الفاصلة
            bot.reply_to(message, f"أحسنت! لقد فزت في اللعبة! استغرق وقتك: {elapsed_time} ثانية.")
            game_active = False
        else:
            bot.reply_to(message, "للأسف، لم يكن الإيموجي الصحيح.")

@bot.message_handler(regexp='^بدء لعبة الايموجي')
def send_start_message(message):
    bot.send_message(message.chat.id, "قم بكتابة 'ايموجي' لبدء لعبة الإيموجي!")

@bot.message_handler(regexp='^بدء لعبة الايموجي')
def send_start_message(message):
    bot.send_message(message.chat.id, "قم بكتابة 'ايموجي' لبدء لعبة الإيموجي!")
@bot.message_handler(func=lambda message: 'Angel' in message.text)
def mention_angel(message):
    bot.reply_to(message, 'ماذا تريد من مطوري؟ @V_D_M')
	

@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.left_chat_member)
def goodbye_member(message):
    bot.send_message(message.chat.id, f"نأسف لرحيلك، {message.left_chat_member.first_name}. نأمل أن نراك مرة أخرى قريبًا!")

@bot.message_handler(func=lambda message: message.text.lower() == "هلو" and message.from_user.id == 1045489068)
def reply_to_hello_developer(message):
    bot.reply_to(message, "مرحبا يا مطوري!")

@bot.message_handler(func=lambda message: message.text.lower() == "شلونكم" and message.from_user.id == 1045489068)
def reply_to_how_are_you_developer(message):
    bot.reply_to(message, "أنا بخير، شكراً!")

@bot.message_handler(func=lambda message: "اكل خرا" in message.text.lower() and message.from_user.id == 1045489068)
def reply_to_bad_words_developer(message):
    bot.reply_to(message, "من فضلك تحدث بشكل محترم")

@bot.message_handler(func=lambda message: message.text.lower() == "كومبي" and message.from_user.id == 1045489068)
def reply_to_comby_developer(message):
    bot.reply_to(message,"كلهم يكومون بيك يا مطوري")



def translate_text(text, dest_language='ar'):
  translator = Translator(to_lang=dest_language)
  translation = translator.translate(text)
  return translation

@bot.message_handler(func=lambda message: message.text.lower() == "ترجم")
def translate_message(message):
  # التحقق مما إذا كانت الرسالة تحتوي على نص
  if message.reply_to_message and message.reply_to_message.text:
      # استخراج النص من الرسالة المردودة
      text_to_translate = message.reply_to_message.text
      # ترجمة النص إلى اللغة العربية
      translated_text = translate_text(text_to_translate)
      # إرسال النص المترجم
      bot.reply_to(message, translated_text)
  else:
      bot.reply_to(message, "يرجى الرد على الرسالة التي تريد ترجمتها.")



@bot.message_handler(func=lambda message: 'لعبة التفكيك' in message.text)
def start_game(message):
    current_word = random.choice(words_list)  # اختيار كلمة عشوائية من القائمة
    bot.send_message(message.chat.id, f'فكك الكلمة: {current_word}')
    bot.register_next_step_handler(message, check_answer, current_word)

def check_answer(message, current_word):
    if message.text.lower() == ' '.join(current_word):
        bot.reply_to(message, 'إجابة صحيحة! لقد فزت في اللعبة.')
    else:
        bot.reply_to(message, 'إجابة خاطئة! حاول مرة أخرى.')

@bot.message_handler(func=lambda message: message.text.lower() == "نكتة")

def send_iraqi_joke(message):
    joke = random.choice(iraqi_jokes_list)
    bot.reply_to(message, joke)


def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # للحصول على درجات الحرارة بوحدة مئوية
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f'Weather in {city}: {weather_desc}, Temperature: {temp}°C'
    else:
        return 'Sorry, could not retrieve weather information for this city.'

@bot.message_handler(func=lambda message: 'الطقس' in message.text.lower() and 'baghdad' in message.text.lower())
def weather_command(message):
    weather_info = get_weather('Baghdad, IQ')  # Baghdad, Iraq
    bot.reply_to(message, weather_info)





valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

@bot.message_handler(regexp='فيلم')
def search_movie(message):
    bot.reply_to(message, "يرجى الانتظار جاري البحث عن فيلم...")

    api_key = "e34783e28c20dee88c332949ff10067b"  # تعويض "YOUR_API_KEY" بمفتاح API الخاص بك
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}"
    response = requests.get(url)
    top_movies = response.json()["results"]
    random_movie = random.choice(top_movies)
    movie_id = random_movie["id"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ar"
    response = requests.get(url)
    movie = response.json()
    movied = movie["overview"]
    movien = random_movie["title"]
    rating = movie["vote_average"]
    year = movie["release_date"][:4]
    poster_path = movie["poster_path"]
    moviep = f"https://image.tmdb.org/t/p/w500{poster_path}"
    if movied is None:
        movied = "-"
    if any(moviep.endswith(ext) for ext in valid_extensions):
        moviep = bot.send_photo(message.chat.id, moviep).photo[0].file_id
    else:
        moviep = "https://telegra.ph/file/15480332b663adae49205.jpg"

    moviet = f"الاسم: {movien}\nالسنة: {year}\nالتقييم: {rating}\nالقصة:\n{movied}"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    response = requests.get(url)
    movie_data = response.json()
    buttons = []
    if 'results' in movie_data:
        for video in movie_data["results"]:
            url = "https://www.youtube.com/watch?v={}".format(video["key"])
            x = telebot.types.InlineKeyboardButton(text="مشاهدة الفيديو", url=url)

            buttons.append(x)

    bot.send_message(
        message.chat.id,
        moviet,
        reply_markup=telebot.types.InlineKeyboardMarkup([buttons]),
        parse_mode="HTML",
    )

@bot.message_handler(func=lambda message: "كوكل" in message.text)
def google_search(message):
    search_query = message.text.replace("كوكل", "").strip()
    # تحويل الجملة الكاملة إلى ترميز URL
    encoded_query = quote(search_query)
    google_search_link = f"https://www.google.com/search?q={encoded_query}"
    bot.reply_to(message, google_search_link)


# تعريف الأمر ومعالجته باستخدام regexp
@bot.message_handler(regexp=r'انطق\s+(.*)')
def text_to_speech(message):
    # استخراج النص بعد كلمة "انطق"
    match = re.search(r'انطق\s+(.*)', message.text)
    if match:
        text = match.group(1).strip()
    else:
        text = ''

    # إذا كان النص فارغًا، الرد برسالة تطلب إدخال نص
    if not text:
        bot.reply_to(message, 'يرجى إدخال نص للتحويل إلى صوت.')
        return

    # تحديد اللغة بناءً على النص
    lang = 'ar' if any(char for char in text if '\u0600' <= char <= '\u06FF') else 'en'

    # إنشاء ملف صوتي من النص
    tts = gTTS(text=text, lang=lang)
    tts.save('output.mp3')

    # إرسال الصوت إلى المستخدم
    audio = open('output.mp3', 'rb')
    bot.send_voice(message.chat.id, audio)
    audio.close()

    # حذف الملف بعد الانتهاء
    os.remove('output.mp3')

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.photo and 'ملصق' in message.text)
def convert_to_sticker(message):
    # الحصول على معرف الصورة المحددة في الرد
    photo_id = message.reply_to_message.photo[-1].file_id

    # تحويل الصورة إلى ملصق
    file_info = bot.get_file(photo_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    response = requests.get(file_url)

    # إرسال الملصق إلى المستخدم
    bot.send_sticker(message.chat.id, response.content)

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.sticker and 'صورة' in message.text)
def convert_to_image(message):
    # الحصول على معرف الملصق المحدد في الرد
    sticker_id = message.reply_to_message.sticker.file_id

    # تحويل الملصق إلى صورة
    file_info = bot.get_file(sticker_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    response = requests.get(file_url)

    # إرسال الصورة إلى المستخدم
    bot.send_photo(message.chat.id, response.content)

@bot.message_handler(func=lambda message: message.text.startswith("اكتبلي "))
def convert_text_to_image(message):
    # استخراج النص من الرسالة
    text = message.text[7:].strip()

    # إعداد صورة فارغة بالأبعاد المناسبة
    image = Image.new('RGB', (400, 100), color=(255, 255, 255))

    # إنشاء كائن ImageDraw لكتابة النص على الصورة
    draw = ImageDraw.Draw(image)

    # استخدام الخط المدمج في PIL
    font = ImageFont.load_default()

    # كتابة النص على الصورة في المكان المحدد
    draw.text((10, 10), text, fill=(0, 0, 0), font=font)

    # إرسال الصورة إلى المستخدم
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    bot.send_photo(message.chat.id, img_byte_arr)

# مفتاح لـ  API
UNSPLASH_ACCESS_KEY = "ilw2Fd-sbbu41IuSJ7h-CLFOlj_-XkL0be6WgaikjAU"

@bot.message_handler(func=lambda message: re.search(r'^بحث صور\s+', message.text))
def search_images(message):
    
    search_query = re.sub(r'^بحث صور\s+', '', message.text).strip()

    # استخدام API للبحث عن الصور
    unsplash_url = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(unsplash_url)

    if response.status_code == 200:
        # استخراج رابط الصورة من نتائج البحث
        data = response.json()
        if data["total"] > 0:
            image_url = data["results"][0]["urls"]["regular"]

            # إرسال الصورة إلى للشخص
            bot.send_photo(message.chat.id, image_url)
        else:
            bot.reply_to(message, "عذرًا، لم أجد أي صور تطابق البحث.")
    else:
        bot.reply_to(message, "عذرًا، حدثت مشكلة أثناء البحث عن الصور.")

wiki_wiki = wikipediaapi.Wikipedia(language='ar', user_agent='WikiSearchBot/1.0')

# معالج الرسائل للبحث في Wikipedia وإرسال صورة الشخصية
@bot.message_handler(func=lambda message: message.text.lower().startswith('ماذا'))
def handle_question(message):
    # استخراج السؤال من رسالة المستخدم
    user_question = message.text[5:]  # تجاهل كلمة "ماذا" واستخراج السؤال الفعلي

    # البحث في Wikipedia مع عنوان المستخدم المحدد
    wiki_page = wiki_wiki.page(user_question)

    if wiki_page.exists():
        
        image_url = wiki_page.text['imageinfo'][0]['url'] if 'imageinfo' in wiki_page.text else None

        if image_url:
            # تحميل الصورة من ويكيبيديا
            response = requests.get(image_url)

            # إرسال الصورة إلى المستخدم
            bot.send_photo(message.chat.id, response.content, caption=wiki_page.summary)
        else:
            bot.reply_to(message, wiki_page.summary)
    else:
        bot.reply_to(message, "عذراً، لم أتمكن من العثور على إجابة.")


# Handler for messages containing the word 'الرابط' using RegEx
@bot.message_handler(regexp=r'.*\bالرابط\b.*')
def handle_link_request(message):
    # Get the chat ID of the group where the message was sent
    chat_id = message.chat.id
    # Get the invite link for the group
    invite_link = bot.export_chat_invite_link(chat_id)
    if invite_link:
        # Send the invite link as a reply
        bot.reply_to(message, invite_link)
    else:
        bot.reply_to(message, 'Unable to retrieve group invite link.')

# الدالة التي تقوم بتنفيذ التحميل وإرسال الأغنية
@bot.message_handler(func=lambda message: message.text.startswith("يوت "))
def send_song(message):
    # بحث عن الأغنية على YouTube
    query = message.text[len("يوتيوب "):].strip()
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        
        yt = YouTube('https://www.youtube.com' + results[0]['url_suffix'])
        song_name = yt.title
        artist_name = yt.author
        caption = f"🎵 {song_name}\n🤖 Developed by @V_D_M"

        
        video = yt.streams.filter(only_audio=True).first()

        # التحقق من وجود وجهة لحفظ الملف
        destination = str(message.chat.id)

        # تنزيل الملف
        out_file = video.download(output_path=destination)

        # حفظ الملف
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        
        thumb_url = yt.thumbnail_url
        thumb_file = os.path.join(destination, "thumb.jpg")
        with open(thumb_file, "wb") as thumb:
            thumb.write(requests.get(thumb_url).content)

        audio = open(new_file, 'rb')
        thumb = open(thumb_file, 'rb')

        # إرسال الأغنية مع اسمها والصورة المصغرة
        bot.send_audio(message.chat.id, audio, title=song_name, thumb=thumb , performer=artist_name , caption=caption )
    else:
        bot.reply_to(message, "لم يتم العثور على الأغنية")
@bot.message_handler(func=lambda message: message.text.startswith("يوت1 "))
def send_full_video(message):
    query = message.text[len("يوت1 "):].strip()
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        yt_url = 'https://www.youtube.com' + results[0]['url_suffix']
        send_youtube_video(bot, message.chat.id, yt_url, full=True)
    else:
        bot.reply_to(message, "لم يتم العثور على الفيديو")

def send_youtube_video(bot, chat_id, youtube_url, full=False):
    yt = YouTube(youtube_url)
    if full:
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    else:
        video = yt.streams.filter(only_video=True).first()

    if video:
        destination = str(chat_id)
        out_file = video.download(output_path=destination)

        bot.send_video(chat_id, open(out_file, 'rb'))

        os.remove(out_file)  # لحذف الملف بعد الإرسال
    else:
        bot.send_message(chat_id, "لم يتم العثور على الفيديو")
@bot.message_handler(regexp=r'^بنترست\s+(https?://(?:www\.)?pinterest\.[^\s]+/pin/[^/?]+\b)')
def pinterest_post(message: Message):
    post_url = message.text.split(' ')[1]
    media_urls = get_media_from_pinterest_post(post_url)
    if media_urls:
        for url in media_urls:
            if url.endswith('.jpg') or url.endswith('.png'):
                bot.send_photo(message.chat.id, url)
            elif url.endswith('.mp4'):
                bot.send_video(message.chat.id, url)
            else:
                bot.reply_to(message, "نوع الوسائط غير مدعوم")
    else:
        bot.reply_to(message, "لم يتم العثور على الوسائط")

#بنتروست
def get_media_from_pinterest_post(post_url):
    response = requests.get(post_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        media_urls = []
        for meta_tag in soup.find_all('meta', {'property': 'og:image'}):
            media_urls.append(meta_tag['content'])
        for video_tag in soup.find_all('meta', {'property': 'og:video'}):
            media_urls.append(video_tag['content'])
        return media_urls
    return None
    
# قاموس لتخزين حالة المستخدمين الذين طلبوا الحصول على file_id
user_waiting_for_photo = {}

@bot.message_handler(commands=['file_id'])
def request_photo(message):
    chat_id = message.chat.id
    # وضع المستخدم في وضع الانتظار لإرسال الصورة
    user_waiting_for_photo[chat_id] = True
    bot.reply_to(message, "الرجاء إرسال الصورة للحصول على الـ file_id.")

@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    chat_id = message.chat.id
    # التأكد من أن المستخدم في وضع انتظار الصورة
    if user_waiting_for_photo.get(chat_id):
        file_id = message.photo[-1].file_id  # الحصول على أعلى جودة للصورة
        bot.reply_to(message, f"File ID: {file_id}")
        # إزالة حالة الانتظار بعد الحصول على الصورة
        user_waiting_for_photo.pop(chat_id)
    else:
        bot.reply_to(message, "استخدم /file_id أولاً لطلب الحصول على الـ file_id.")

# ملف JSON لتخزين الردود
RESPONSES_FILE = 'responses.json'

# تحميل الردود المخزنة من ملف JSON
def load_responses():
    try:
        with open(RESPONSES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # إذا لم يكن الملف موجوداً، نبدأ بقاموس فارغ

# حفظ الردود إلى ملف JSON
def save_responses():
    with open(RESPONSES_FILE, 'w') as file:
        json.dump(responses, file)

# تحميل الردود عند بدء تشغيل البوت
responses = load_responses()

# أمر لإضافة رد
@bot.message_handler(func=lambda message: message.text.lower() == "أضف رد")
def add_response(message):
    if is_admin(message.chat.id, message.from_user.id):
        bot.send_message(message.chat.id, "حسناً، ارسل لي الكلمة المستهدفة.")
        bot.register_next_step_handler(message, process_target_word)
    else:
        bot.send_message(message.chat.id, "عذراً، لديك صلاحيات غير كافية.")

def process_target_word(message):
    target_word = message.text
    bot.send_message(message.chat.id, "حسناً، أعطني الرد.")
    bot.register_next_step_handler(message, process_response_word, target_word)

def process_response_word(message, target_word):
    response_word = message.text
    responses[target_word] = response_word
    save_responses()  # حفظ الردود بعد إضافتها
    bot.send_message(message.chat.id, "تم حفظ الرد.")

# دالة لعرض الردود عند استلام رسالة
@bot.message_handler(func=lambda message: True)  # دالة لمعالجة أي رسالة
def handle_responses(message):
    for target_word, response in responses.items():
        if target_word in message.text.lower():
            bot.send_message(message.chat.id, response)
            break  # لإرسال رد واحد فقط
                
bot.infinity_polling()