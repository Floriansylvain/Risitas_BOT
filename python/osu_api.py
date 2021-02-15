from osuapi import OsuApi, ReqConnector
from private import TOKEN_OSU
import matplotlib.pyplot as plt

api = OsuApi(TOKEN_OSU, connector=ReqConnector())

async def ask_osu_profile(username):
    results = api.get_user(username)
    if not results:
        return 1
    r = results[0]
    return [r.user_id, r.ranked_score, r.accuracy, r.playcount,
        r.total_score, (r.count300 + r.count100 + r.count50),
        r.total_seconds_played, r.level, r.pp_rank]


async def ask_osu_last_game(username):
    last_game = api.get_user_recent(username)
    if not last_game:
        return 1
    lg = last_game[0]
    lm = api.get_beatmaps(beatmap_id=lg.beatmap_id)[0]
    return [lm.beatmapset_id, lm.title, lm.creator,
        lm.bpm, lm.difficultyrating, lm.diff_size, lm.diff_overall,
        lm.diff_approach, lm.diff_drain, lg.score,
        lg.maxcombo, lg.rank, lg.count300, lg.count100,
        lg.count50, lg.countmiss, lg.countkatu, lg.countgeki]


async def ask_osu_acc(username):
    last_game = api.get_user_recent(username)
    if not last_game:
        return 0

    lst = []
    for game in last_game:
        total = game.count300 + game.count100 + game.count50 + game.countmiss
        lst.append((float("%.2f" %(((game.count300 * 300) + (game.count100 * 100) + (game.count50 * 50)) / (total * 300) * 100))))

    nb_games = len(lst)+1
    min_games = int(min(lst))

    plt.figure(figsize=(9, 5))
    plt.plot(list(range(1, nb_games)), lst)
    plt.scatter(list(range(1, nb_games)), lst, color='red')
    plt.axis([1, nb_games-1, min_games, 100])
    plt.title('Accuracy of ' + username + ' on his last ' + str(nb_games-1) + ' games.')
    plt.xticks(range(1, nb_games))
    plt.yticks(range(min_games, 100, 5))
    plt.grid(linewidth=0.5)
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Games (from recent to oldest)')
    plt.savefig('acc.jpeg')
    return 1
