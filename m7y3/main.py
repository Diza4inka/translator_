import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
from googletrans import Translator

duration = 5  # секунды записи
sample_rate = 44100

words_by_level = {
    "easy": ["кот", "собака", "молоко", "солнце"],
    "medium": ["банан", "школа", "окно", "жёлтый"],
    "hard": ["технология", "информация", "произношение", "воображение"]
}

def translator():
    user_answer = 'да'
    while user_answer == 'да':
        print("🎙 Говори...")
        recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,      
        channels=1,                  
        dtype="int16")              
        sd.wait()  

        wav.write("output.wav", sample_rate, recording)
        print("✅ Запись завершена, теперь распознаём...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("📝 Ты сказал:", text)
        except sr.UnknownValueError:          
            print("Не удалось распознать речь.")
        except sr.RequestError as e:            
            print(f"Ошибка сервиса: {e}")

        lang = input("На какой язык перевести? (например, 'en' - английский, 'es' - испанский, 'pt' - Португальский, 'id' - Индонезийский, 'pl' - Польский, 'it' - Итальянский, 'tr' - Турецкий): ")

        translator = Translator()
        translated = translator.translate(text, dest=lang)  
        print("🌍 Перевод на выбранный язык:", translated.text)
        user_answer = input('Хотите ли вы продолжить?')

def game():
    print("🎮 Добро пожаловать в игру!")
    level = input("Выберите уровень сложности (easy, medium, hard):")

    mistakes = 0
    score = 0

    while mistakes < 3:
        word = random.choice(words_by_level[level])
        print(f"Слово для перевода: {word}")

        print("🎙 Говори перевод на английском...")

        recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,      
        channels=1,                  
        dtype="int16")              
        sd.wait()  
  
        wav.write("output.wav", sample_rate, recording)
        print("✅ Запись завершена, теперь распознаём...")

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            recognized_word = recognizer.recognize_google(audio, language="en-EN")
            print("📝 Ты сказал:", recognized_word)
            translator = Translator()
            translated = translator.translate(word, dest='en')  
            word_en = translated.text
            if recognized_word == word_en:
                print("🎉 Вы правильно перевели слово!")
                score += 1
            else:
                print(f"❌ Неправильно! Правильный перевод: {word_en}")
                mistakes += 1
                print(f"Ошибок: {mistakes}/3")
        
        except sr.UnknownValueError:          
            print("Не удалось распознать речь.")
        except sr.RequestError as e:            
            print(f"Ошибка сервиса: {e}")
            mistakes += 1
            print(f"Ошибок: {mistakes}/3")

    print(f"Игра окончена! Ваш счет: {score}. Вы сделали {mistakes} ошибок.")

choice = input("Выберите действие: 1 - Переводчик, 2 - Игра. Введите 1 или 2: ")
if choice == '1':
    translator()
elif choice == '2':
    game()
else:
    print("Неверный ввод. Пожалуйста, введите 1 или 2.")