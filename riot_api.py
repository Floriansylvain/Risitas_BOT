from riotwatcher import LolWatcher
from private import token_riot
# import pandas as pd

watcher = LolWatcher(token_riot)
region = 'EUW1'

def rank_track(nickname, player):

    ranked_stats = watcher.league.by_summoner(region, player['id'])
    if not ranked_stats:
        return str(nickname) + ' n\'est pas ranked.'
    else:
        for infos in ranked_stats:
            if infos['queueType'] == 'RANKED_SOLO_5x5':
                what_rank = 'Solo Queue'
            elif infos['queueType'] == 'RANKED_FLEX_SR':
                what_rank = 'Flexible'
            return infos['summonerName'] + ' est ' + str(infos['tier']) + ' ' +  str(infos['rank']) + ' ' + str(infos['leaguePoints']) + ' LP en ' + str(what_rank) + '. ' + str(infos['wins']) + ' W / ' + str(infos['losses']) + 'L.'

# def match_track(nickname, player):
#     matche = watcher.match.matchlist_by_account(region, player['accountId'])
#     last_match = matche['matches'][0]
#     match_detail = watcher.match.by_id(region, last_match['gameId'])

#     print(match_detail)

# def main():
#     while 1:
#         nickname = str(input("Entrez votre pseudo league of legend : "))
#         try:
#             player = watcher.summoner.by_name(region, nickname)
#             rank_track(nickname, rank_track, player)
#             # match_track(nickname, player)
#             break
#         except ApiError:
#             print("Le pseudo est inconnu.")

# if __name__ == '__main__':
#     main()