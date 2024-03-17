import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3
import datetime
import subprocess
import pyperclip
import json

fcfg = 'cfg.json'
with open(fcfg, 'r', encoding='utf-8') as json_file:
    cfg = json.load(json_file)

com_yt = ['открой ютуб', 'открой youtube', 'включи ютуб', 'включи youtube', 'смотреть ютуб', 'смотреть youtube']
com_mu = ['музыку', 'музыка', 'музык']
com_vr = ['время']
com_cp = ['копировать']
com_fd = ['поиск', 'найти', 'найди', 'искать', 'запрос', 'интернет']

music_servs = ['https://music.yandex.ru/home', 'https://vk.com/audio', 'https://open.spotify.com/',
               'https://music.youtube.com/', 'https://music.apple.com/']


# функция произношения текста
def talk(words):
    print(words)
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()


# функция музыки
def musicopen():
    r = sr.Recognizer()
    if cfg['musicID'] == -1:
        with sr.Microphone() as source:
            talk('Сначала назовите, где вы слушаете музыку: Яндекс, ВК, Спотифай, Ютуб, Эппл?')
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            mplatform = r.recognize_google(audio, language="ru-RU").lower()
            f1 = True
            if any(x in mplatform for x in ['яндекс', 'yandex']):
                cfg['musicID'] = 0
            elif any(x in mplatform for x in ['вк', 'вконтакте', 'vk', 'vkontakte']):
                cfg['musicID'] = 1
            elif any(x in mplatform for x in ['спотифай', 'spotify']):
                cfg['musicID'] = 2
            elif any(x in mplatform for x in ['ютуб', 'youtube', 'ютьюб']):
                cfg['musicID'] = 3
            elif any(x in mplatform for x in ['эплэппл', 'apple']):
                cfg['musicID'] = 4
            else:
                f1 = False
            with open(fcfg, 'w', encoding='utf-8') as json_file:
                json.dump(cfg, json_file)
            if f1:
                talk(f'платформа установлена на {mplatform}')
                print(f'платформа установлена на {mplatform}')
                return musicopen()
            else:
                talk('ошибка выбора сервиса')
                print('ошибка выбора сервиса')
                return musicopen()
        except sr.UnknownValueError:
            talk('ошибка выбора сервиса')
            return musicopen()
    else:
        talk('Запускаю музыку')
        mplatform = music_servs[cfg['musicID']]
        return mplatform


# функция поиска в браузере
def poiskbrows():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk('Жду текст для поисковика')
        print('жду текст для браузера')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        psk = r.recognize_google(audio, language="ru-RU").lower()
        talk('Запускаю поисковик')
        print('ищу в браузере:' + psk)
    except sr.UnknownValueError:
        talk('Я Вас не поняла')
        psk = poiskbrows()
    return psk


# функция копирования в буфер
def textvbufer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk('Жду текст для копирования')
        print('жду текст для буфера')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        ttb = r.recognize_google(audio, language="ru-RU").lower()
        talk('Добавила в буфер обмена')
        print('копирую в буфер:' + ttb)
    except sr.UnknownValueError:
        talk('Я Вас не поняла')
        ttb = textvbufer()
    return ttb


# функция рассказывания времени
def time_say():
    now = datetime.datetime.now()
    vremia = str(now.time())
    chasi = vremia[:2]
    minuti = vremia[3:5]
    chasii = int(chasi)
    minutii = int(minuti)
    if chasii == 1 or chasii == 21:
        chst = 'час'
    elif (chasii >= 2 and chasii <= 4) or chasii == 22 or chasii == 23:
        chst = 'часа'
    else:
        chst = 'часов'
    if minutii % 10 == 1:
        minst = 'минута'
    elif (minutii % 10 == 2 or minutii % 10 == 3 or minutii % 10 == 4) and minutii // 10 != 1:
        minst = 'минуты'
    else:
        minst = 'минут'
    talk('сейчас' + chasi + chst + minuti + minst)


# функция ожидания голосовой команды
def nachalo():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('жду начала')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        na = r.recognize_google(audio, language="ru-RU").lower()
        if 'варя' in na:
            make_command(command())
    except sr.UnknownValueError:
        nachalo()


# функция обработки команд
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk('Говорите')
        print('жду команду')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
        print('вы сказали:' + zadanie)
    except sr.UnknownValueError:
        talk('Я Вас не поняла')
        zadanie = command()
    return zadanie


# функция выполнения команд
def make_command(zadanie):
    # открыть ютуб
    if any(x in zadanie for x in com_yt):
        talk('Уже открываю')
        url = 'https://www.youtube.com/'
        webbrowser.open(url)

    # открыть музыку
    elif any(x in zadanie for x in com_mu):
        webbrowser.open(musicopen())

    # время
    elif any(x in zadanie for x in com_vr):
        time_say()

    # текст
    elif any(x in zadanie for x in com_cp):
        pyperclip.copy(textvbufer())

    # поиск в браузере
    elif any(x in zadanie for x in com_fd):
        pstr = poiskbrows()
        pstr = pstr.replace(' ', '+')
        pstr = 'https://yandex.ru/search/?text=' + pstr
        webbrowser.open(pstr)

    # отмена голосового ввода
    elif 'отмена' in zadanie:
        talk('Ожидаю')
        nachalo()

    # закрыть помощника
    elif 'закрыть' in zadanie:
        talk('Закрываюсь')
        sys.exit()


talk('Спроси что-то')

while True:
    nachalo()
