import matplotlib.pyplot as plt
from osuapi import OsuApi, ReqConnector
from private import TOKEN_OSU

api = OsuApi(TOKEN_OSU, connector=ReqConnector())

async def ask_osu_profile(username):
    results = api.get_user(username)
    if not results:
        return 1
    res = results[0]
    return [res.user_id, res.ranked_score, res.accuracy, res.playcount,
            res.total_score, (res.count300 + res.count100 + res.count50),
            res.total_seconds_played, res.level, res.pp_rank]


async def ask_osu_last_game(username):
    last_game = api.get_user_recent(username)
    if not last_game:
        return 1
    lsg = last_game[0]
    lsm = api.get_beatmaps(beatmap_id=lsg.beatmap_id)[0]
    return [lsm.beatmapset_id, lsm.title, lsm.creator,
            lsm.bpm, lsm.difficultyrating, lsm.diff_size, lsm.diff_overall,
            lsm.diff_approach, lsm.diff_drain, lsg.score,
            lsg.maxcombo, lsg.rank, lsg.count300, lsg.count100,
            lsg.count50, lsg.countmiss, lsg.countkatu, lsg.countgeki]


async def ask_osu_acc(username):
    last_game = api.get_user_recent(username)
    if not last_game:
        return 0

    lst = []
    for game in last_game:
        total = game.count300 + game.count100 + game.count50 + game.countmiss
        lst.append((float("%.2f" % (((game.count300 * 300) + (game.count100 * 100) +
                                     (game.count50 * 50)) / (total * 300) * 100))))

    nb_games = len(lst)+1
    min_games = int(min(lst))

    plt.figure(figsize=(9, 6))

    plt.rc('axes', labelsize=18)

    plt.plot(list(range(1, nb_games)), lst, color='#ffbf00')
    plt.scatter(list(range(1, nb_games)), lst, color='#ffca2b')
    plt.axis([1, nb_games-1, min_games, 100])
    plt.xticks(range(1, nb_games))
    plt.yticks(range(min_games, 100, 3))

    plt.grid(linewidth=0.5)
    plt.title('Accuracy of ' + username + ' on his last ' +
              str(nb_games-1) + ' games.', fontsize=20)
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Games (from recent to oldest)')

    plt.gca().set_facecolor('#36393f')
    plt.savefig('acc.jpeg', facecolor='#ffd1f1')
    return 1
