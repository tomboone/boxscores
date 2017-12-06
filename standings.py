from xmlstats import xmlstats
from operator import itemgetter as i
from functools import cmp_to_key


def cmp(a, b):
    return (a > b) - (a < b)


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1)
            if col.startswith('-')
            else (i(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def division(data, league, division):
    op = """
<table>
    <thead>
        <tr>
            <th style="width:150px">
"""
    if division == 'C':
        op += 'Central'
    elif division == 'E':
        op += 'East'
    elif division == 'W':
        op += 'West'
    else:
        op = 'That\'s not a valid division.'
        exit()
    op += """
            </th>
            <th style="width:40px">W</th>
            <th style="width:40px">L</th>
            <th style="width:40px">PCT</th>
            <th style="width:40px">GB</th>
            <th style="width:40px">L10</th>
            <th style="width:40px">STRK</th>
        </tr>
    </thead>
    <tbody>
"""
    teams = []
    for s in data['standing']:
        if s['conference'] == league and s['division'] == division:
            teams.append(s)

    teams = multikeysort(teams, ['rank', '-won'])

    for i in teams:
        op += '<tr>\n'
        op += '<td>' + i['first_name'] + ' ' + i['last_name'] + '</td>\n'
        op += '<td>' + str(i['won']) + '</td>\n'
        op += '<td>' + str(i['lost']) + '</td>\n'
        op += '<td>' + i['win_percentage'] + '</td>\n'
        op += '<td>'
        if i['games_back'] == 0.0:
            op += '-'
        else:
            op += str(i['games_back'])
        op += '</td>\n'
        op += '<td>' + i['last_ten'] + '</td>\n'
        op += '<td>'
        if i['streak_type'] == 'loss':
            op += 'L'
        elif i['streak_type'] == 'win':
            op += 'W'
        op += str(i['streak_total']) + '</td>\n'
        op += '</tr>\n'

    op += """
    </tbody>
</table>
"""
    return op


def standings():
    standings = xmlstats('standings', sport='mlb')
    output = '<h2>STANDINGS</h2>'
    output += '<h3>AMERICAN LEAGUE</h3>\n'
    output += division(standings, 'AL', 'E')
    output += division(standings, 'AL', 'C')
    output += division(standings, 'AL', 'W')
    output += '<h3>NATIONAL LEAGUE</h3>'
    output += division(standings, 'NL', 'E')
    output += division(standings, 'NL', 'C')
    output += division(standings, 'NL', 'W')

    return output
