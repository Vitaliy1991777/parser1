import requests
from datetime import datetime
from telegram import send_telegram

def get_message(yellow_card):
    league, team_1, team_2, timestamp, total, total_high, total_low = yellow_card.values()
    timestamp = yellow_card['S'] + 2*60*60
    game_date = datetime.fromtimestamp(timestamp).strftime('%d.%m %H:%M')

    message = f'{league} ({game_date})\n' \
              f'{team_1} - {team_2}\n' \
              f'\n' \
              f'ТМ {total}@{total_low}\n' \
              f'ТБ {total}@{total_high}\n'
    send_telegram(message)
    print(message)
    print('==========================')

def get_yellow_card(game_result, game_id):
    for game in game_result["Value"]:
        current_id = game['I']
        if current_id == game_id:
            yellow_card = {}
            yellow_card["L"] = game["L"]
            yellow_card["O1"] = game["O1"]
            yellow_card["O2"] = game["O2"]
            yellow_card["S"] = game["S"]

            bets = game["SG"]
            for item in bets:
                try:
                    bet = item["TG"]
                except:
                    bet = item["PN"]
                if 'Желтые карточки' in bet:
                    for node in item["E"]:
                        table_cell = node["T"]

                        if 9 == table_cell:
                            total = node["P"]
                            coef = node["C"]
                            yellow_card['total'] = total
                            yellow_card['total_high'] = coef
                        if 10 == table_cell:
                            coef = node["C"]
                            yellow_card['total_low'] = coef

                    get_message(yellow_card)
            print('===========================================')

def get_game(result):
    for game in result["Value"]:
        game_id = game['I']
        champs = game['LI']

        params = {
            'count': '10',
            'sports': '1',
            'champs': champs,
            'partner': '51',
            'antisports': '188',
            'mode': '4',
            'getEmpty': 'true',
            'country': '1',
            'tf': '2200000',
            'subGames': game_id,
        }

        response = requests.get('https://1xstavka.ru/LineFeed/BestGamesExtVZip', params=params)
        game_result = response.json()
     #   print(game_result)

        get_yellow_card(game_result, game_id)

        break


def main():
    url = 'https://1xstavka.ru/line/football/96463-germany-bundesliga/'

    champs = url.split('/')[-2].split('-')[0]


    params = {
        'count': '10',
        'sports': '1',
        'champs': champs,
        'partner': '51',
        'antisports': '188',
        'mode': '4',
        'getEmpty': 'true',
        'country': '1',
        'tf': '2200000',
        'subGames': '449970928',
    }

    response = requests.get('https://1xstavka.ru/LineFeed/BestGamesExtVZip', params=params)
    result = response.json()

    get_game(result)


if __name__ == '__main__':
    main()
