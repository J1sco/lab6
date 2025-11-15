#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
from datetime import datetime

class ChatBot:
    """Простой чат-бот для лаборатории 6"""
    
    def __init__(self, name="LabBot"):
        self.name = name
        self.conversation_history = []
        
        # Паттерны и ответы
        self.patterns = {
            r'привет|здравствуй|hi|hello': [
                f"Привет! Я {self.name}, чем могу помочь?",
                f"Здравствуйте! Меня зовут {self.name}.",
                "Привет! Рад вас видеть!"
            ],
            r'как дела|как ты|how are you': [
                "Отлично, спасибо! Готов помочь с вашими задачами.",
                "Всё хорошо! Чем могу быть полезен?",
                "Прекрасно! У меня всегда хорошее настроение, когда я помогаю людям."
            ],
            r'что ты умеешь|помощь|help': [
                "Я могу:\n- Отвечать на вопросы\n- Помогать с обфускатором\n- Просто поболтать\n- Показать время\n- Рассказать анекдот",
                "Я умею отвечать на ваши вопросы, помогать с кодом и поддерживать беседу!",
            ],
            r'время|который час|what time': [
                f"Сейчас {datetime.now().strftime('%H:%M:%S')}",
                f"Текущее время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
            ],
            r'обфускатор|obfuscator': [
                "Обфускатор - это инструмент для усложнения чтения кода. В этом репозитории есть obSKUFATOR.py для обфускации C кода!",
                "У нас есть обфускатор кода! Используйте obSKUFATOR.py с файлом config.json для настройки.",
            ],
            r'анекдот|joke|пошути': [
                "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25! 🎃",
                "- Сколько программистов нужно, чтобы вкрутить лампочку?\n- Ни одного, это аппаратная проблема!",
                "Программист это человек, который решает проблемы, о существовании которых вы не знали, способами, которые вы не понимаете.",
            ],
            r'спасибо|thanks|thank you': [
                "Пожалуйста! Обращайтесь!",
                "Рад помочь!",
                "Не за что! 😊",
            ],
            r'пока|bye|goodbye|до свидания': [
                "До свидания! Удачи!",
                "Пока! Заходите ещё!",
                "До встречи! Хорошего дня!",
            ],
            r'кто ты|who are you': [
                f"Я {self.name} - чат-бот для помощи студентам!",
                f"Меня зовут {self.name}, я создан для помощи в лабораторных работах.",
            ],
            r'да|yes|конечно': [
                "Отлично!",
                "Хорошо!",
                "Понял вас!",
            ],
            r'нет|no': [
                "Понятно.",
                "Хорошо, как скажете.",
                "Ладно.",
            ],
        }
        
        self.default_responses = [
            "Интересно! Расскажите подробнее.",
            "Я вас понимаю.",
            "Хм, это любопытно.",
            "Не совсем понял, но продолжайте.",
            "Можете уточнить?",
            "Извините, я ещё учусь. Можете переформулировать?",
        ]
    
    def get_response(self, user_input):
        """Получить ответ на сообщение пользователя"""
        if not user_input or not user_input.strip():
            return "Вы ничего не сказали. Напишите что-нибудь!"
        
        user_input = user_input.lower().strip()
        self.conversation_history.append(("user", user_input))
        
        # Поиск подходящего паттерна
        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                response = random.choice(responses)
                self.conversation_history.append(("bot", response))
                return response
        
        # Если паттерн не найден, возвращаем случайный ответ по умолчанию
        response = random.choice(self.default_responses)
        self.conversation_history.append(("bot", response))
        return response
    
    def show_history(self):
        """Показать историю разговора"""
        if not self.conversation_history:
            return "История пуста."
        
        history = []
        for sender, message in self.conversation_history:
            if sender == "user":
                history.append(f"Пользователь: {message}")
            else:
                history.append(f"{self.name}: {message}")
        return "\n".join(history)
    
    def clear_history(self):
        """Очистить историю разговора"""
        self.conversation_history = []
        return "История очищена."


def main():
    """Основная функция для запуска чат-бота"""
    bot = ChatBot("LabBot")
    
    print("=" * 60)
    print(f"     Добро пожаловать в чат-бот {bot.name}!")
    print("=" * 60)
    print("Напишите 'выход' или 'exit' для завершения разговора")
    print("Напишите 'история' для просмотра истории разговора")
    print("Напишите 'очистить' для очистки истории")
    print("=" * 60)
    print()
    
    while True:
        try:
            user_input = input("Вы: ").strip()
            
            if not user_input:
                continue
            
            # Проверка на выход
            if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                print(f"\n{bot.name}: До свидания! Удачи в учёбе! 👋")
                break
            
            # Специальные команды
            if user_input.lower() in ['история', 'history']:
                print(f"\n{bot.name}: История разговора:")
                print("-" * 60)
                print(bot.show_history())
                print("-" * 60)
                print()
                continue
            
            if user_input.lower() in ['очистить', 'clear']:
                print(f"\n{bot.name}: {bot.clear_history()}")
                print()
                continue
            
            # Получение ответа от бота
            response = bot.get_response(user_input)
            print(f"\n{bot.name}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{bot.name}: До свидания! Удачи в учёбе! 👋")
            break
        except Exception as e:
            print(f"\n{bot.name}: Произошла ошибка: {e}\n")


if __name__ == "__main__":
    main()
