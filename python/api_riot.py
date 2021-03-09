from riotwatcher import LolWatcher, ApiError
from private import TOKEN_RIOT
from datetime import datetime, timedelta

WATCHER = LolWatcher(TOKEN_RIOT)
REGION = 'EUW1'

def what_player(name):
    try:
        return WATCHER.summoner.by_name(REGION, name)
    except ApiError:
        return 0


def rank_track(player):
    ranked_stats = WATCHER.league.by_summoner(REGION, player['id'])
    if not ranked_stats:
        return 'Unranked cette saison.'
    liste = []
    for infos in ranked_stats:
        if infos['queueType'] == 'RANKED_SOLO_5x5':
            what_rank = 'Solo Queue'
        elif infos['queueType'] == 'RANKED_FLEX_SR':
            what_rank = 'Flexible'
        liste.append([what_rank, infos['tier'], infos['rank'], infos['leaguePoints'], infos['wins'], infos['losses']])
    return liste


def last_match(player):
    matches = WATCHER.match.matchlist_by_account('EUW1', player['accountId'])
    recent_match = matches['matches'][0]
    match_detail = WATCHER.match.by_id('EUW1', recent_match['gameId'])
    lst = [[],[[],[],[],[]]]
    for x, y in zip(match_detail['participants'], match_detail['participantIdentities']):
        lst[0].append([y['player']['summonerName'],
            x['stats']['totalDamageDealtToChampions'],
            x['stats']['kills'],
            x['stats']['deaths'],
            x['stats']['assists']])

    for team in match_detail['teams']:
        lst[1][0].append(team['win'])
        lst[1][1].append(team['firstBlood'])
        lst[1][2].append(team['firstTower'])
        lst[1][3].append(team['firstDragon'])

    ts = str(match_detail['gameCreation'])[:-3]
    dt = datetime.fromtimestamp(int(ts)).date()

    lst.append(str(dt))
    lst.append(str(timedelta(seconds=match_detail['gameDuration'])))

    return lst
