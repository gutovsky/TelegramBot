import time
import json
import requests
import urllib3

class TBotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.api_url + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def echo_all(self, updates):
        for update in updates["result"]:
            try:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                self.send_message(text, chat)
            except Exception as e:
                print(e)

    @staticmethod
    def get_last_chat_id_and_text(updates):
        num_updates = len(updates["result"])
        if num_updates == 0:
            return None, None
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return text, chat_id

    def send_message(self, text, chat_id):
        params = {'text': text, 'chat_id': chat_id}
        encodedParams = urllib3.parse.urlencode(params)

        url = self.api_url + "sendMessage?" + encodedParams
        self.get_url(url)

    @staticmethod
    def get_url(url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    @staticmethod
    def get_last_update_id(updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)


def main():
    last_update_id = None

    bot = TBotHandler('774095680:AAHBGJuJa5R2nS3c92zS4C1J5TylQTHVMOg')
    while True:
        updates = bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            bot.echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()