import time
from xmlstats import xmlstats


def leaders(category):
    time.sleep(10)
    leads = xmlstats('leaders', sport='nba', category=category)
    header = category.replace('_', ' ').title()
    op = '<table style="width: 300px;">\n<thead>\n<tr>'
    op += '<th colspan=3>' + header + '</th>\n</tr>\n</thead>\n'
    op += '<tbody>\n'
    for i in leads:
        op += '<tr>\n<td>' + str(i['rank']) + '</td>\n'
        op += '<td>' + i['display_name'] + ', '
        op += i['team']['abbreviation'] + '</td>\n'
        op += '<td>' + str(i['value']) + '</td>\n</tr>\n'
    op += '</tbody></table>\n'
    return op


def nbaleaders():
    output = '<div class="leaders">\n'
    output += '<h2>NBA Leaders</h2>\n'

    output += leaders('points_per_game')
    output += leaders('assists_per_game')
    output += leaders('rebounds_per_game')
    output += leaders('off_rebounds_per_game')
    output += leaders('def_rebounds_per_game')
    output += leaders('steals_per_game')
    output += leaders('blocks_per_game')
    output += leaders('field_goal_pct')
    output += leaders('free_throw_pct')
    output += leaders('three_point_pct')
    output += leaders('three_point_field_goals_made')

    output += '</div>'

    return output
