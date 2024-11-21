def extract_text_from_pdf(pdf_path):
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
    
  
  