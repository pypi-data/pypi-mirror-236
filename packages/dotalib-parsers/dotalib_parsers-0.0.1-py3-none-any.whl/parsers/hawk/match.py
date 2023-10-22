from ..base import BaseMatchParser
from dotalib import Match, Team, find_hero
import html
import re


radiant_hero_pattern = re.compile(r'{"is_radiant":true,"hero":{"name":"[\w\-\'\"\_ ]+",')
dire_hero_pattern = re.compile(r'{"is_radiant":false,"hero":{"name":"[\w\-\'\"\_ ]+",')
team1_pattern = re.compile(r'"team1":\{"id":[\d]+,"name":".+?"')
team2_pattern = re.compile(r'"team2":\{"id":[\d]+,"name":".+?"')
team_side_pattern = re.compile(r'"series_best_of":.+?,"is_team1_radiant":.+?,')
winner_pattern = re.compile(r'"is_team1_radiant":[truefalse]*,"is_radiant_won":[truefalse]+,')
championship_patter = re.compile(r'championship_name":".+?"')


class HawkParser(BaseMatchParser):
    def parse_match(self, content: str) -> Match:
        self.content = html.unescape(content)
        radiant_heroes, dire_heroes = self._find_heroes()
        radiant_name, dire_name = self._find_teams_names()
        championship_name = self._find_championship()
        is_radiant_won = self._is_radiant_won()
        radiant_team = Team(radiant_heroes, name=radiant_name, is_winner=is_radiant_won)
        dire_team = Team(dire_heroes, name=dire_name, is_winner=not is_radiant_won)
        match = Match(radiant_team, dire_team, championship=championship_name)
        return match

    def _find_heroes(self):
        radiant_heroes_matches = radiant_hero_pattern.findall(self.content)
        dire_heroes_matches = dire_hero_pattern.findall(self.content)
        radiant_heroes = [match_.split('"')[-2] for match_ in radiant_heroes_matches]
        dire_heroes = [match_.split('"')[-2] for match_ in dire_heroes_matches]
        radiant_heroes = [find_hero(hero) for hero in radiant_heroes]
        dire_heroes = [find_hero(hero) for hero in dire_heroes]
        return radiant_heroes, dire_heroes
    
    def _find_teams_names(self):
        team1_match = team1_pattern.findall(self.content)[0]
        team2_match = team2_pattern.findall(self.content)[0]
        is_team1_radiant_match = team_side_pattern.findall(self.content)[0]
        name1 = team1_match.split('"')[-2]
        name2 = team2_match.split('"')[-2]
        is_team1_radiant = True if 'true' in is_team1_radiant_match else False
        radiant_name = name1 if is_team1_radiant else name2
        dire_name = name1 if not is_team1_radiant else name2
        return radiant_name, dire_name

    def _is_radiant_won(self):
        winner_matches = winner_pattern.findall(self.content)
        if not winner_matches:
            return None
        winner_match = winner_matches[0]
        is_radiant_won = winner_match.split(':')[-1][:-1]
        if is_radiant_won == 'true':
            return True
        elif is_radiant_won == 'false':
            return False
        else:
            return None

    def _find_championship(self):
        match = championship_patter.search(self.content)
        row = match.group()
        champ_name = row.split('"')[-2]
        return champ_name


_hawk = HawkParser()
parse_match = _hawk.parse_match