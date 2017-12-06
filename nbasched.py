import time
from datetime import date, datetime
from xmlstats import xmlstats


def schedule():
    today = date.today()
    today = date.strftime(today, '%Y%m%d')

    output = '<div class="schedule">\n'
    output += '<h2>TODAY\'S GAMES</h2>\n'

    events = xmlstats('events', sport='nba', date=today)
    games = []

    for e in events['event']:
        games.append(e)
    if not games:
        output += '<p>No games scheduled today.</p>\n</div>'
        return output
        exit()

    for g in games:
        away = '<strong>' + g['away_team']['abbreviation'] + '</strong>'
        home = '<strong>' + g['home_team']['abbreviation'] + '</strong>'
        gtime = g['start_date_time'].replace('-04:00', '')
        gtime = g['start_date_time'].replace('-05:00', '')
        gtime = datetime.strptime(gtime, '%Y-%m-%dT%H:%M:%S')
        gtime = datetime.strftime(gtime, '%-I:%M%p')
        output += '<table>\n<tbody>\n'
        output += '<tr>\n<td style="padding-right: 10px;">'
        output += away + '</td>\n'
        output += '<td rowspan=2 style="padding-left: '
        output += '10px; text-align: right;">'
        output += gtime + '</td>\n</tr>\n'
        output += '<tr>\n<td>' + home + '</td>\n</tr>\n</tbody>\n</table>\n'

    output += '</div>'
    return output
