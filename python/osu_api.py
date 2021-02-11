from osuapi import OsuApi, ReqConnector
from private import TOKEN_OSU
import requests

api = OsuApi(TOKEN_OSU, connector=ReqConnector())

async def ask_osu(username):
    results = api.get_user(username)
    if not results:
        return 1
    r = results[0]
    liste = [r.user_id, r.ranked_score, r.accuracy, r.playcount,
        r.total_score, (r.count300 + r.count100 + r.count50),
        r.total_seconds_played, r.level, r.pp_rank]
    return liste
