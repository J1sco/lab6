#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для демонстрации работы чат-бота
"""

from chatbot import ChatBot


def demo_chatbot():
    """Демонстрация возможностей чат-бота"""
    
    print("=" * 70)
    print("                  ДЕМОНСТРАЦИЯ ЧАТ-БОТА")
    print("=" * 70)
    print()
    
    bot = ChatBot("DemoBot")
    
    test_messages = [
        "Привет!",
        "Как дела?",
        "Что ты умеешь?",
        "Который час?",
        "Расскажи анекдот",
        "Что такое обфускатор?",
        "Спасибо!",
    ]
    
    for message in test_messages:
        print(f"👤 Пользователь: {message}")
        response = bot.get_response(message)
        print(f"🤖 {bot.name}: {response}")
        print()
    
    print("-" * 70)
    print("История разговора:")
    print("-" * 70)
    print(bot.show_history())
    print("-" * 70)
    print()
    
    print("=" * 70)
    print("                  ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)


if __name__ == "__main__":
    demo_chatbot()
