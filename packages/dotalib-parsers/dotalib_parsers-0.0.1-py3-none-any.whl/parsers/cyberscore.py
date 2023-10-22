from .base import BaseMatchParser
from dotalib import Match, Team, find_hero
import re

team_pattern = re.compile(r'itemProp="name">.+?</span')
hero_pattern = re.compile(r'\/b\&gt\; \(.+?\)')
winner_pattern = re.compile(r'Силы .+?<.+?loss')
championship_pattern = re.compile(r'"name_alternative":".+?"')


class CyberscoreParser(BaseMatchParser): 
    """
    Not thread-safe in each new thread create new class instead using prebound functions
    """
    def parse_match(self, content: str) -> Match:
        self.content = content
        radiant_heroes, dire_heroes = self._find_heroes()
        radiant_name, dire_name = self._find_teams_names()
        is_radiant_won = self._is_radiant_won()
        is_dire_won = None if is_radiant_won is None else (not is_radiant_won)
        champ_name = self._find_championship()
        radiant_team = Team(radiant_heroes, name=radiant_name, is_winner=is_radiant_won)
        dire_team = Team(dire_heroes, name=dire_name, is_winner=is_dire_won)
        match = Match(radiant_team, dire_team, championship=champ_name)
        return match

    def _find_heroes(self):
        hero_matches = hero_pattern.findall(self.content)[:10]
        heroes = [hero.split('(')[-1].split(')')[0] for hero in hero_matches]
        heroes = [find_hero(hero) for hero in heroes]
        radiant_heroes, dire_heroes = heroes[:5], heroes[5:]
        return radiant_heroes, dire_heroes
    
    def _find_teams_names(self):
        team_matches = team_pattern.findall(self.content)
        tm = team_matches[-1]
        title = tm[tm.find(">") + 1:tm.rfind("<")]
        teams_names = title.split(' vs ')
        radiant_name = teams_names[0]
        dire_name = teams_names[1][:-2]
        return radiant_name, dire_name
    
    def _is_radiant_won(self):
        winner_matches = winner_pattern.findall(self.content)
        if not winner_matches:
            return None
        winner_match = winner_matches[0].split("<")[0]
        return "Силы тьмы" in winner_match
    
    def _find_championship(self):
        champ_matches = championship_pattern.findall(self.content)
        champ_name = champ_matches[0].split('"')[-2] if champ_matches else None 
        return champ_name


_cyberscore_parser = CyberscoreParser()
parse_match = _cyberscore_parser.parse_match