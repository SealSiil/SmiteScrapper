from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def process(match, match_num, playersdict):
    website = 'https://smite.guru/match/' + str(match)
    matchweb = requests.get(website)
    soup = BeautifulSoup(matchweb.text, 'html.parser')
    section_match = soup.find('section', id="match-stats")
    winners = section_match.find('div', class_="match-table win")
    w_matchtable = winners.find_all('div', class_="match-table__row")
    losers = section_match.find('div', class_="match-table loss")
    l_matchtable = losers.find_all('div', class_="match-table__row")

    game_mode = soup.find('h1').text
    for player_num, player in enumerate(w_matchtable):
        row_group = player.find_all('div', class_="row__item")
        playerdict = {'name': player.find('a', class_="row__player__name").text,
                      'god': player.find_all('img')[0]['alt'],
                      'Victory': 1,
                      'level': row_group[0].text,
                      'kda': row_group[1].text,
                      'gold': row_group[2].text,
                      'GMP': row_group[3].text,
                      'damage': row_group[4].text,
                      'taken': row_group[5].text,
                      'mitigated': row_group[6].text,
                      'build': [i['alt'] for i in player.find_all('img')[1:]],
                      'game_mode': game_mode,
                      'match_id': match}
        playersdict[player_num + match_num] = playerdict
    for player_num, player in enumerate(l_matchtable):
        row_group = player.find_all('div', class_="row__item")
        playerdict = {'name': player.find('a', class_="row__player__name").text,
                      'god': player.find_all('img')[0]['alt'],
                      'Victory': 0,
                      'level': row_group[0].text,
                      'kda': row_group[1].text,
                      'gold': row_group[2].text,
                      'GMP': row_group[3].text,
                      'damage': row_group[4].text,
                      'taken': row_group[5].text,
                      'mitigated': row_group[6].text,
                      'build': [i['alt'] for i in player.find_all('img')[1:]],
                      'game_mode': game_mode,
                      'match_id': match}
        playersdict[player_num + match_num + 5] = playerdict

    return playersdict


pattern = re.compile(r'href=\"\/match\/(\d*)')
matchList = []
failures = []
match_num = 0
playersdict = {}


try:
    for page in range(1, 100):
        website = f'https://smite.guru/profile/5339344-Stagefault/matches?page={page}'
        response = requests.get(website)
        print(response.status_code)
        matchList = matchList + pattern.findall(response.text)
except:
    print(f"Chris games stop at: {page}")

try:
    for page in range(1, 100):
        website = f'https://smite.guru/profile/5339344-Stagefault/matches?page={page}'
        response = requests.get(website)
        print(response.status_code)
        matchList = matchList + pattern.findall(response.text)
except:
    print(f"Zach games stop at: {page}")


try:
    for page in range(1, 100):
        website = f'https://smite.guru/profile/5339344-Stagefault/matches?page={page}'
        response = requests.get(website)
        print(response.status_code)
        matchList = matchList + pattern.findall(response.text)
except:
    print(f"Jason games stop at: {page}")


try:
    for page in range(1, 100):
        website = f'https://smite.guru/profile/5339344-Stagefault/matches?page={page}'
        response = requests.get(website)
        print(response.status_code)
        matchList = matchList + pattern.findall(response.text)
except:
    print(f"Ben games stop at: {page}")

match_set = set(matchList)


for match in match_set:
    print(f"Processing match: {match}")
    try:
        playersdict = process(match, match_num, playersdict)
        match_num += 10
    except:
        print(f"Failure at match: {match}")
        failures.append(match)


for match in failures:
    print(f"Processing match: {match}")
    try:
        playersdict = process(match, match_num, playersdict)
        match_num += 10
    except:
        print(f"Failure at match: {match}")


smite_df = pd.DataFrame.from_dict(playersdict, orient='index')
smite_df.to_excel(
    r"C:/Users/jason/Desktop/Coding/pythonProgramMemes/smitedata.xlsx", index=False)
