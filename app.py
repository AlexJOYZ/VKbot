import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api.longpoll
from config import VK_TOKEN
from config import AI_TOKEN
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage

model = GigaChat(
    credentials=AI_TOKEN,
    verify_ssl_certs=False,
)

session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(session)
api = session.get_api()


def send_message_to_VK(user_id, message):
    api.messages.send(
        user_id=user_id,
        random_id=0,
        message=message
    )
def send_message_to_AI(request):
    response = model.invoke([HumanMessage(content=f'Напиши мне краткую общую информацию о теме {request}')])
    return response

def main_loop():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text:
                request = event.text.lower().strip()
                user_id = event.user_id
                if request.startswith('начать'):
                    send_message_to_VK(user_id, 'Привет! Я готов помочь вам с изучением любой темы. Назовите тему, пожалуйста. Но сделайте это согласно шаблону: Помоги мне изучить тему: [Ваша тема]')
                elif request.startswith('помоги мне изучить тему:'):
                    topic = request.replace('помоги мне изучить тему:', '').strip()
                    # send_message_to_VK(user_id, f'Отлично! Я помогу вам с темой "{topic}". Пожалуйста, пришлите мне файл с материалами по этой теме.')
                    response = send_message_to_AI(topic)
                    send_message_to_VK(user_id, response.content)
                else:
                    send_message_to_VK(user_id, "Некорректное сообщение, пожалуйства следуйте шаблону")
            elif event.attachments:
              response = send_message_to_AI(topic)
              send_message_to_VK(user_id, response.content)

if __name__ == "__main__":
    main_loop()