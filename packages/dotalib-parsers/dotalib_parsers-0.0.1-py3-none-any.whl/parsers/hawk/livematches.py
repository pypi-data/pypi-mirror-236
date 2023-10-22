from dotalib import Match
import re


live_pattern = re.compile(r'"id":[\d]+,"number":[\d]+,"is_team1_radiant":[\w]+,"is_radiant_won":null,')

LIVE_URL = 'http://hawk.live'
MATCHES_URL = 'https://hawk.live/matches'


class HawkLiveMatchesParser(object):
    def parse_matches_ids(self, content: str) -> list[str]:
        topic_matches = live_pattern.findall(content)
        topics = [t.split(',')[0].split(':')[1] for t in topic_matches]
        return topics

_hawk_live_matches_parser = HawkLiveMatchesParser()
parse_matches_ids = _hawk_live_matches_parser.parse_matches_ids

    # def find_matches(self, content: str) -> dict:
    #     ids = self.parse_live_ids(content)
    #     urls = [f'{MATCHES_URL}/{id}' for id in ids]
    #     matches_copy = self.matches.copy()
    #     for url in matches_copy:
    #         if url not in urls:
    #             self.matches.pop(url)
    #     for url in urls:
    #         if url in self.matches:
    #            continue 
    #         parser = HawkParser(url)
    #         try:
    #             await parser.read_content()
    #             match = parser.parse_match()
    #             cls._matches[url] = match
    #         except:
    #             logger.warning('Live match is not ready.')
    #     return self.matches
    
    # def get_match(self, url: str) -> Match or None:
    #     return self.matches.get(url, None)
