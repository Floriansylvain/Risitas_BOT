from osuapi import OsuApi, ReqConnector
from private import TOKEN_OSU
import requests

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
