import json
import re


def minimize_str(s: str):
    return re.sub(r"\W", "", s.lower())


class HawkOddsParser(object):
    def __init__(self) -> None:
        self.odds_json = {}

    # @classmethod
    # async def update_odds(cls):
    #     if cls.is_cooldown():
    #         return
    #     await cls._parser.read_content()
    #     page = unescape(cls._parser.content)
    #     start_text = '"upcoming_series":'
    #     start = page.find(start_text) + len(start_text)
    #     end_text = ',"top_series"'
    #     end = page.find(end_text)
    #     content = page[start:end]
    #     cls._raw_odds_json = json.loads(content)
    #     cls._last_check_timestamp = time.time()
    #     odds = cls._parse_odds()
    #     cls._odds_json.update(odds)

    def update_odds(self, content: str):
        start_text = '"upcoming_series":'
        start = content.find(start_text) + len(start_text)
        end_text = ',"top_series"'
        end = content.find(end_text)
        content = content[start:end]
        raw_odds_json = json.loads(content)
        odds = self.parse_odds(raw_odds_json)
        self.odds_json.update(odds) 

    def parse_odds(self, raw_odds_json: dict):
        odds_json = {}
        for match in raw_odds_json:
            team1 = match['team1']['name']
            team2 = match['team2']['name']
            odds_info = match['series_odds_info_array']
            team1_odd = 0
            team2_odd = 0
            if not odds_info:
                continue
            for info in odds_info:
                odds = info['odds'][0]
                if info['is_team1_first']:
                    team1_odd += float(odds['first_team_winner'] or 1)
                    team2_odd += float(odds['second_team_winner'] or 1)
                else:
                    team2_odd += float(odds['first_team_winner'] or 1)
                    team1_odd += float(odds['second_team_winner'] or 1)
            team1_odd /= len(odds_info)
            team2_odd /= len(odds_info)
            odds_json[(minimize_str(team1), minimize_str(team2))] = (
                round(team1_odd, 2), 
                round(team2_odd, 2)
            )
        return odds_json

    def get_odds(self):
        return self.odds_json.copy()


_hawk_odds_parser = HawkOddsParser()
get_odds = _hawk_odds_parser.get_odds
update_odds = _hawk_odds_parser.update_odds