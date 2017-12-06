import time
from datetime import date, timedelta
from xmlstats import xmlstats


def final(i, side):  # Get and format each team's final score
    # Set team variables
    team = side + '_team'
    score = side + '_period_scores'

    # Display team score
    if team in i:
        fin = '<td><strong>' + i[team]['full_name'] + '</strong></td>\n'
        fin += '<td style="text-align: right;"><strong>'
        fin += str(sum(i[score])) + '</strong></td>\n'

        return fin

    else:
        fin = ''
        return fin


def finals(i):  # Combine and display both final scores
    # Final scores
    fins = '<table style="font-size: 1.3em;">\n'
    fins += '<tr>\n' + final(i, 'away') + '</tr>'
    fins += '<tr>' + final(i, 'home') + '</tr>\n</table>'

    return fins


def line(i, side):  # Get and format each team's line score
    # Set team variables
    team = side + '_team'
    score = side + '_period_scores'

    # Team name
    if team in i:
        lin = '<tr><td><strong>' + i[team]['abbreviation']
        lin += '</strong></td>'

        # Team scores
        for p in i[score]:
            lin += '<td>' + str(p) + '</td>\n'
        lin += '</tr>'

        return lin

    else:
        lin = ''
        return lin


def lines(i):  # Combine and display both line scores
    # Open line score table
    lins = '<table>\n<thead>\n<tr>\n<th> </th>\n'

    # Set line score headers
    per = 1
    if 'away_period_scores' in i:
        for p in i['away_period_scores']:
            if per < 5:  # Set period number
                lins += '<th>' + str(per) + '</th>\n'
            else:  # Set OT number
                ot = per - 4
                lins += str(ot) + '<th> OT</th>\n'
            per = per + 1
        lins += '</tr>\n</thead>\n<tbody>\n'

        # Team line scores
        lins += line(i, 'away')  # Away team line score
        lins += line(i, 'home')  # Home team line score

        # Close line score table
        lins += '</tbody>\n</table>'

        return lins
    else:
        lins = ''
        return lins


def teambox(i, side):  # Get and format each team's boxscore
    team = side + '_team'
    stats = side + '_stats'

    # Team header
    if team in i:
        bs = '<h4>' + i[team]['full_name'] + '</h4>'

        # Stat headers
        bs += """
        <table>
            <thead>
                <tr>
                    <th style="width: 190px;">Player</th>
                    <th>Min</th>
                    <th>FG</th>
                    <th>3pt</th>
                    <th>FT</th>
                    <th>Off</th>
                    <th>Def</th>
                    <th>Reb</th>
                    <th>Ast</th>
                    <th>TO</th>
                    <th>Stl</th>
                    <th>Blk</th>
                    <th>PF</th>
                    <th>Pts</th>
                </tr>
            </thead>
            <tfoot>
"""

        # Team stat totals
        bs += '<tr>\n<td><strong>Totals</strong></td>\n'
        bs += '<td> </td>\n'
        bs += '<td>'
        bs += str(sum(p['field_goals_made'] for p in i[stats]))
        bs += '-'
        bs += str(sum(p['field_goals_attempted'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['three_point_field_goals_made'] for p in i[stats]))
        bs += '-'
        bs += str(sum(p['three_point_field_goals_attempted'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['free_throws_made'] for p in i[stats])) + '-'
        bs += str(sum(p['free_throws_attempted'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['offensive_rebounds'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['defensive_rebounds'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['rebounds'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['assists'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['turnovers'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['steals'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['blocks'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['personal_fouls'] for p in i[stats]))
        bs += '</td>\n<td>'
        bs += str(sum(p['points'] for p in i[stats]))
        bs += '</td>\n</tr>\n'

        # Team percentages
        bs += '<tr>'
        bs += '<td>Percentages</td>\n'
        bs += '<td> </td>'

        # Field goal percentage
        fgm = sum(p['field_goals_made'] for p in i[stats])
        fga = sum(p['field_goals_attempted'] for p in i[stats])
        fgp = round(float(fgm)/float(fga)*100, 1)
        bs += '<td>' + str(fgp) + '%</td>\n'

        # 3pt percentage
        tpm = sum(p['three_point_field_goals_made'] for p in i[stats])
        tpa = sum(p['three_point_field_goals_attempted'] for p in i[stats])
        tpp = round(float(tpm)/float(tpa)*100, 1)
        bs += '<td>' + str(tpp) + '%</td>\n'

        # Free throw percentage
        ftm = sum(p['free_throws_made'] for p in i[stats])
        fta = sum(p['free_throws_attempted'] for p in i[stats])
        ftp = round(float(ftm)/float(fta)*100, 1)
        bs += '<td>' + str(ftp) + '%</td>\n'
        bs += '<td> </td>\n<td> </td>\n<td> </td>\n<td> </td>\n<td> </td>\n'
        bs += '<td> </td>\n<td> </td>\n<td> </td>\n<td> </td>\n'

        bs += '</tr>\n</tfoot>\n<tbody>'

        # Player stat lines
        for p in i[stats]:
            bs += '<tr>\n'
            bs += '<td>' + p['display_name']
            bs += ' <strong>' + p['position'] + '</strong></td>\n'
            bs += '<td>' + str(p['minutes']) + '</td>\n'
            bs += '<td>' + str(p['field_goals_made']) + '-'
            bs += str(p['field_goals_attempted']) + '</td>\n'
            bs += '<td>' + str(p['three_point_field_goals_made']) + '-'
            bs += str(p['three_point_field_goals_attempted']) + '</td>\n'
            bs += '<td>' + str(p['free_throws_made']) + '-'
            bs += str(p['free_throws_attempted']) + '</td>\n'
            bs += '<td>' + str(p['offensive_rebounds']) + '</td>\n'
            bs += '<td>' + str(p['defensive_rebounds']) + '</td>\n'
            bs += '<td>' + str(p['rebounds']) + '</td>\n'
            bs += '<td>' + str(p['assists']) + '</td>\n'
            bs += '<td>' + str(p['turnovers']) + '</td>\n'
            bs += '<td>' + str(p['steals']) + '</td>\n'
            bs += '<td>' + str(p['blocks']) + '</td>\n'
            bs += '<td>' + str(p['personal_fouls']) + '</td>\n'
            bs += '<td>' + str(p['points']) + '</td>\n'
            bs += '</tr>\n'

        bs += '</tbody></table>\n'

        return bs
    else:
        bs = ''
        return bs


def nbaboxscore():
    # Get yesterday's games and create list of IDs
    yesterday = date.today() - timedelta(1)
    yesterday = date.strftime(yesterday, '%Y%m%d')

    box = '<div class="scores">\n'
    box += '<h2>SCOREBOARD</h2>\n'

    events = xmlstats('events', sport='nba', date=yesterday)
    games = []
    for e in events['event']:
        games.append(e['event_id'])
    if not games:
        box += '<p>No games scheduled yesterday.</p>\n</div>'
        return box
        exit()

    # Retrieve each boxscore and add to list
    time.sleep(10)
    boxscores = []
    for e in games:
        boxscores.append(xmlstats('boxscore', sport='nba', event=e))
        time.sleep(10)

    # Format each box score
    for i in boxscores:
        # Open box score div
        box += '<div style="border-top: 1px solid">\n'

        # Final score
        box += finals(i)

        # Line score
        box += lines(i)

        # Box score
        box += teambox(i, 'away')
        box += teambox(i, 'home')

        # Close out boxscore div
        box += '</div>\n'

    # Close out section div
    box += '</div>'

    return box
