from gigachat import GigaChat

from config import config_obj

def get_answer_from_gigachat(promt: str):
    with GigaChat(credentials=config_obj.gigachat_api_key, verify_ssl_certs=False) as giga:
        response = giga.chat(promt)
        return response.choices[0].message.content

