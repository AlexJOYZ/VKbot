import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api.longpoll
from config import VK_TOKEN


from getInfoFromFile import handle_file_upload

session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(session)
api = session.get_api()

def send_message_to_VK(user_id, message):
    api.messages.send(
        user_id=user_id,
        random_id=0,
        message=message
    )

topic= ''

def main_loop():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text:
                request = event.text.lower().strip()
                print(request)
                user_id = event.user_id
                if request.startswith('начать'):
                    send_message_to_VK(user_id, 'Привет! Я готов помочь вам с изучением любой темы. Назовите тему, пожалуйста. Но сделайте это согласно шаблону: Помоги мне изучить тему: [Ваша тема]')
                elif request.startswith('помоги мне изучить тему:'):
                    topic = request.replace('помоги мне изучить тему:', '').strip()
                    topic = request.replace('помоги мне изучить тему:', '').strip()
                    send_message_to_VK(user_id, f'Отлично! Я помогу вам с темой "{topic}". Пожалуйста, пришлите мне файл с материалами по этой теме.')
                    
                else:
                    send_message_to_VK(user_id, "Некорректное сообщение, пожалуйства следуйте шаблону")
            elif event.attachments:
              print('@',vk_api.longpoll.VkLongpollMode(GET_EXTENDED = 8))
              text = handle_file_upload(VkEventType,topic)
              send_message_to_VK(user_id, text)
              send_message_to_VK(user_id, 'Если что-то не понятно можете уточнить')

if __name__ == "__main__":
    main_loop()