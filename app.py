import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api.longpoll
from config import VK_TOKEN
from config import AI_TOKEN
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage


session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(session)
api = session.get_api()

model = GigaChat(
    credentials=AI_TOKEN,
    verify_ssl_certs=False,
)
def send_message_to_VK(user_id, message):
    api.messages.send(
        user_id=user_id,
        random_id=0,
        message=message
    )
def send_message_to_AI(user_id, prompt):
    response = model.invoke([HumanMessage(content=prompt)])
    send_message_to_VK(user_id, response.content)
    return response.content

topic= ''

def main_loop():
    isFlag = False
    isAnswer= False
    isTest= False
    global text
    global answers
    global res
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower().strip()
            user_id = event.user_id
            if (isFlag and isAnswer and request.startswith('стоп')):
                prompt = f"Составьте вопросы, которые будут проверять усвоенную информацию из темы '{topic}', используя в качестве источника информации следующий текст:\n\n{text}\n\n"
                send_message_to_VK(user_id, 'Проверьте свои знания и ответьте на вопросы')
                answers = send_message_to_AI(user_id,prompt)
                res = request
                isAnswer=False
                isTest = True
            elif isTest:
                prompt = f" Оценить правильность ответов {res} на вопросы {answers} по темы '{topic}', используя в качестве источника следующий текст:\n\n{text}\n\n"
                send_message_to_VK(user_id,'Оцените себя сами. Только честно! Что было не понятно спросите')
                send_message_to_AI(user_id,prompt)
                isAnswer = True
            elif (isFlag and isAnswer):
                prompt = f"Ответь на вопрос {request} по теме '{topic}', используя в качестве источника информации следующий текст:\n\n{text}\n\n"
                send_message_to_AI(user_id,prompt)
                send_message_to_VK(user_id,'Если остались ещё вопросы, то продолжайте приссылать сообщения. Однако если вы хотите прейти уже непосредственно к проверке усвоенного материала, то пиши команду: стоп')
            elif isFlag:
                prompt = f"Сделайте краткий обзор по теме '{topic}' на основе следующего текста:\n\n{request}\n\nТезисы должны быть структурированы и содержать только ключевые моменты."
                text = request
                send_message_to_AI(user_id,prompt)
                send_message_to_VK(user_id, 'Если что-то не понятно можете уточнить?')
                isAnswer= True


            elif request.startswith('начать'):
                send_message_to_VK(user_id, 'Привет! Я готов помочь вам с изучением любой темы. Назовите тему, пожалуйста. Но сделайте это согласно шаблону: Помоги мне изучить тему: [Ваша тема]')
            elif request.startswith('помоги мне изучить тему:'):
                topic = request.replace('помоги мне изучить тему:', '').strip()
                send_message_to_VK(user_id, f'Отлично! Я помогу вам с темой "{topic}". Пожалуйста, пришлите мне текст по этой теме.')
                isFlag=True
                    
            else:
                send_message_to_VK(user_id, "Некорректное сообщение, пожалуйства следуйте шаблону")
            

if __name__ == "__main__":
    main_loop()