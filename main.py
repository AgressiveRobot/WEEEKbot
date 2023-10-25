
python
import requests
from googleapiclient.discovery import build
from telegram import Bot

def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

def create_week_task(api_token, task_name):
    url = "https://api.week.app/task"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": task_name
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def handle_google_form_response(api_token, telegram_ids, telegram_api_token, week_api_token):
    service = build('forms', 'v1', credentials=api_token)
    response = service.forms().get().execute()
    form_id = response['formId']
    form_responses = service.forms().responses().list(formId=form_id).execute()
    for form_response in form_responses['responses']:
        answers = form_response['answers']
        # Получите необходимые данные из ответов на форму
        # Например, если в форме есть вопрос "Имя", то имя можно получить так:
        name = answers[0]['text']
        
        # Отправить уведомление в Telegram
        message = f"Получен новый ответ на Google Forms от {name}"
        for chat_id in telegram_ids:
            send_telegram_message(telegram_api_token, chat_id, message)
        
        # Создать новую задачу в WEEEK CRM
        task_name = f"Новый ответ на Google Forms от {name}"
        create_week_task(week_api_token, task_name)

# Замените значения переменных ниже на ваши токены и настройки
google_form_url = "https://docs.google.com/forms/..."
GF_API_TOKEN = "your_google_forms_api_token"
telegram_id_list = [123456789, 987654321]
telegram_api_token = "your_telegram_bot_api_token"
WEEEK_API_TOKEN = "your_week_api_token"

# Если используется google_form_url, получите api_token
if google_form_url:
    # Получите api_token с помощью Google OAuth2 аутентификации
    api_token = ...
else:
    api_token = GF_API_TOKEN

handle_google_form_response(api_token, telegram_id_list, telegram_api_token, WEEEK_API_TOKEN)
