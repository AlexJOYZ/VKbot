import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from giga_chat import GigaChat
import requests
import os

# Ваши токены и идентификаторы
VK_TOKEN = 'ваш_токен_группы'
GROUP_ID = ваш_id_группы
GIGA_CHAT_API_KEY = 'ваш_API_ключ_GigaChat'

# Инициализация VK API
session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(session)
api = session.get_api()

# Инициализация GigaChat
giga_chat = GigaChat(api_key=GIGA_CHAT_API_KEY)

def send_message(user_id, message):
    api.messages.send(
        user_id=user_id,
        random_id=0,
        message=message
    )

def extract_text_from_pdf(pdf_path):
    # Используйте библиотеку PyPDF2 или другую для извлечения текста из PDF
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def summarize_text(text, topic):
    prompt = f"Сделайте краткий обзор по теме '{topic}' на основе следующего текста:\n\n{text}\n\nТезисы должны быть структурированы и содержать только ключевые моменты."
    response = giga_chat(prompt)
    summary = response
    return summary

def process_file(file_info, user_id, topic):
    file_url = file_info['url']
    file_name = file_info['title']
    
    # Сохраняем файл на диск
    local_path = f'/tmp/{file_name}'
    with open(local_path, 'wb') as f:
        f.write(requests.get(file_url).content)
    
    # Извлекаем текст из файла
    extracted_text = extract_text_from_pdf(local_path)
    
    # Подготавливаем краткое содержание
    summary = summarize_text(extracted_text, topic)
    
    # Удаляем временный файл
    os.remove(local_path)
    
    return summary

def handle_file_upload(event, user_id, topic):
    attachment_type = event.attachments[0]['type']
    
    if attachment_type == 'doc':
        doc = event.attachments[0]['doc']
        summary = process_file(doc, user_id, topic)
        return summary
    
    else:
        return 'К сожалению, я могу работать только с документами. Можете прислать документ по данной теме?'

def main_loop():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text:
                request = event.text.lower().strip()
                user_id = event.user_id
                
                if request.startswith('помощь'):
                    send_message(user_id, 'Привет! Я готов помочь вам с изучением любой темы. Назовите тему, пожалуйста.')
                    
                elif request.startswith('тема:'):
                    topic = request.replace('тема:', '').strip()
                    send_message(user_id, f'Отлично! Я помогу вам с темой "{topic}". Пожалуйста, пришлите мне файл с материалами по этой теме.')
                    
                elif event.attachments:
                    summary = handle_file_upload(event, user_id, topic)
                    send_message(user_id, summary)

if __name__ == "__main__":
    main_loop()