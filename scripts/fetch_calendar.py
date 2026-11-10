import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY = 'query { user(login:"chenyiwen-work") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date weekday contributionCount contributionLevel } } } } } }'
LEVELS = {'NONE': 0, 'FIRST_QUARTILE': 1, 'SECOND_QUARTILE': 2, 'THIRD_QUARTILE': 3, 'FOURTH_QUARTILE': 4}


def save(calendar):
    weeks = []
    for week in calendar['weeks']:
        slots = [None] * 7
        for day in week['contributionDays']:
            slots[day['weekday']] = {'date': day['date'], 'count': day['contributionCount'], 'level': LEVELS[day['contributionLevel']]}
        weeks.append(slots)
    assert sum(d['count'] for w in weeks for d in w if d) == calendar['totalContributions']
    (ROOT / 'cache').mkdir(exist_ok=True)
    (ROOT / 'cache/calendar.json').write_text(json.dumps({'total': calendar['totalContributions'], 'weeks': weeks}, indent=1), encoding='utf-8', newline='\n')
    print(f"Calendar: {calendar['totalContributions']} contributions, {len(weeks)} weeks")


if __name__ == '__main__':
    request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query': QUERY}).encode(), headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Content-Type': 'application/json', 'User-Agent': 'chenyiwen-work-profile'})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    if data.get('errors'):
        raise RuntimeError(data['errors'])
    save(data['data']['user']['contributionsCollection']['contributionCalendar'])
