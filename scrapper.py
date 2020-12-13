from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def process(match, match_num, playersdict):
    ''' The function extracts information from the given match by connecting to Smite.guru.  Takes three inputs: match an interger that repersents the match ID from Smite, 
    match_num is a interger that prevents the player enties in the playersdict for overlapping, 
    playersdict is a dictionary that is used to hold the records obtained from the scrapping.
    '''
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


def find_matches(username):
    '''A function that finds all the match IDs that a given user has played.
    Taking as input a string username, and outputs a list of the matches.
    '''
    page = 1
    new_matches = []
    matches = []
    while new_matches or page == 1:
        website = f'https://smite.guru/profile/{username}/matches?page={page}'
        response = requests.get(website)
        new_matches = pattern.findall(response.text)
        matches = matches + new_matches
        page += 1
    print(f"{username} games stop at: {page}")
    return matches


pattern = re.compile(r'href=\"\/match\/(\d*)')
matchList = []
failures = []
match_num = 0
accounts = ["5339344-Stagefault", "6434393-PantsuRaider",
            "440605-JDiablo6G6", "11056361-zdude18"]
file_path = r"C:/Users/jason/Desktop/Coding/pythonProgramMemes/smitedata.xlsx"
playersdict = {}


for account in accounts:
    matchList += find_matches(account)


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
smite_df.to_excel(file_path, index=False)
