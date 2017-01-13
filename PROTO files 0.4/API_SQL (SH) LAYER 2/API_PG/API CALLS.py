import dota2api
import pymysql
import pymysql.cursors

api = dota2api.Initialise("BFF23F667B3B31FD01663D230DF11C25")
# hist = api.get_match_history(account_id=41231571)
# hist not working correctly, account MUST have 3rd party data turned on
summary = api.get_player_summaries (41231571)
match = api.get_match_details(match_id=1000193456)
match['radiant_win']

print (match)
print (summary)


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='api_data')

cur = conn.cursor()
cur.execute("SELECT * FROM league")
'''
#INSERT ATTEMPT
placeholders = ', '.join(['%s'] * len(summary))
columns = ', '.join(summary.keys())
sql = "INSERT INTO player_summary VALUES ( %s )"
cursors.execute(sql, summary())
#
'''


'''
Supported API calls

get_match_history (#STEAMID)
get_match_history_by_seq_num
get_match_details (MATCH ID)
get_player_summaries (#STEAMID)
get_league_listing
get_live_league_games
get_team_info_by_team_id
get_heroes ()
get_tournament_prize_pool
get_game_items
get_top_live_games
'''