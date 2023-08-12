import requests


def send_telegram(text: str):
    token = "6161435363:AAHk-GbTTGPYzpo3uVWX1FzchDdzIpUhkEo"
    url = "https://api.telegram.org/bot"
    chat_id = '563455286'
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    })

    if r.status_code != 200:
        raise Exception("post_text error")


def main():
    send_telegram('Привет, чувак!')


if __name__ == '__main__':
    main()