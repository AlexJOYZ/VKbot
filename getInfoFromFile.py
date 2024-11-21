from langchain_gigachat.chat_models import GigaChat
from extractTextFromFile import extract_text_from_pdf 
from config import AI_TOKEN
from langchain_core.messages import HumanMessage
import os
import requests

model = GigaChat(
    credentials=AI_TOKEN,
    verify_ssl_certs=False,
)

def summarize_text(text, topic):
    prompt = f"Сделайте краткий обзор по теме '{topic}' на основе следующего текста:\n\n{text}\n\nТезисы должны быть структурированы и содержать только ключевые моменты."
    response = model.invoke([HumanMessage(content=prompt)])
    return response

def process_file(file_info, topic):
    print('@jsdsjd',file_info)
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

def handle_file_upload(event,  topic):
    attachment_type = event.attachments['attach1_type']
    # attachment_type='doc'
    print(event.attachments)
    
    if attachment_type == 'doc':
        doc = attachment_type
        summary = process_file(doc, topic)
        return summary
    
    else:
        return 'К сожалению, я могу работать только с документами. Можете прислать документ по данной теме?'

    
  
  