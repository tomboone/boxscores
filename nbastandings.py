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
    if division == 'ATL':
        op += 'Atlantic'
    elif division == 'SE':
        op += 'Southeast'
    elif division == 'CEN':
        op += 'Central'
    elif division == 'NW':
        op += 'Northwest'
    elif division == 'SW':
        op += 'Southwest'
    elif division == 'PAC':
        op += 'Pacific'
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
    standings = xmlstats('standings', sport='nba')
    output = '<div class="standings">\n'
    output += '<h2>STANDINGS</h2>\n'
    output += '<h3>ATLANTIC CONFERENCE</h3>\n'
    output += division(standings, 'EAST', 'ATL')
    output += division(standings, 'EAST', 'SE')
    output += division(standings, 'EAST', 'CEN')
    output += '<h3>WESTERN CONFERENCE</h3>'
    output += division(standings, 'WEST', 'NW')
    output += division(standings, 'WEST', 'SW')
    output += division(standings, 'WEST', 'PAC')
    output += '</div>'

    return output
