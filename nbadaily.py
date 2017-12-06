import time
from datetime import date, timedelta
from xmlstats import xmlstats


def daily():
    yesterday = date.today() - timedelta(1)
    yesterday = date.strftime(yesterday, '%Y%m%d')
    leaders = xmlstats('daily-leaders', sport='nba', date=yesterday)

    output = '<div class="daily-leaders">\n'
    output += '<h2>YESTERDAY\'S HIGHLIGHTS</h2>\n'
    for i in leaders['player']:
        output += '<div style="margin-bottom: 20px;">'
        output += '<h3 style="margin-bottom: 0px;">' + i['display_name']
        output += ' (' + i['team_abbreviation'] + ')</h3>'
        output += str(i['points']) + ' Pts, '
        output += str(i['assists']) + ' Ast, '
        output += str(i['rebounds']) + ' Reb, '
        output += str(i['steals']) + ' Stl, '
        output += str(i['blocks']) + ' Blk, '
        output += str(i['three_point_field_goals_made'])
        output += '-' + str(i['three_point_field_goals_attempted'])
        output += ' 3pt</div>\n'
    output += '</div>'
    return output
