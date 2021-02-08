from riotwatcher import LolWatcher
from private import token_riot

watcher = LolWatcher(token_riot)
region = 'EUW1'

def rank_track(player):
    ranked_stats = watcher.league.by_summoner(region, player['id'])
    
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