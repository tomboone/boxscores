import time
from datetime import date, timedelta
from xmlstats import xmlstats


def battingLine(i, team, stat, long_stat):  # assemble individual off stats
    statList = []
    side = team + '_batters'
    for b in i[side]:
        if b[long_stat] >= 1:
            statName = b['display_name']
            if b[long_stat] >= 2:
                statName += ' ' + str(b[long_stat])
            statList.append(statName)
    if statList:
        statStr = '; '.join(statList)
        statLine = '<span><strong>' + stat + ':</strong> '
        statLine += statStr + '<br /></span>\n'
        return statLine
    else:
        return ''


def offense(i, side):  # assemble other offensive stats per team
    bs = ''
    if (
        battingLine(i, side, '2B', 'doubles') or
        battingLine(i, side, '3B', 'triples') or
        battingLine(i, side, 'HR', 'home_runs') or
        battingLine(i, side, 'TB', 'total_bases') or
        battingLine(i, side, 'RBI', 'rbi') or
        battingLine(i, side, '2-out RBI', 'rbi_with_two_outs') or
        battingLine(i, side, 'SAC', 'sac_hits') or
        battingLine(i, side, 'SF', 'sac_flies')
    ):
        bs += '<h5>BATTING</h5>\n'
        bs += battingLine(i, side, '2B', 'doubles')
        bs += battingLine(i, side, '3B', 'triples')
        bs += battingLine(i, side, 'HR', 'home_runs')
        bs += battingLine(i, side, 'TB', 'total_bases')
        bs += battingLine(i, side, 'RBI', 'rbi')
        bs += battingLine(i, side, '2-out RBI', 'rbi_with_two_outs')
        bs += battingLine(i, side, 'SAC', 'sac_hits')
        bs += battingLine(i, side, 'SF', 'sac_flies')
    if (
        battingLine(i, side, 'SB', 'stolen_bases') or
        battingLine(i, side, 'CS', 'caught_stealing')
    ):
        bs += '<h5>BASERUNNING</h5>\n'
        bs += battingLine(i, side, 'SB', 'stolen_bases')
        bs += battingLine(i, side, 'CS', 'caught_stealing')
    return bs


def fieldingLine(i, team, stat, long_stat):  # assemble individual def lines
    statList = []
    side = team + '_fielding'
    for b in i[side]:
        if b[long_stat] >= 1:
            statName = b['display_name']
            if b[long_stat] >= 2:
                statName += ' ' + str(b[long_stat])
            statList.append(statName)
    if statList:
        statStr = '; '.join(statList)
        statLine = '<span><strong>' + stat + ':</strong> '
        statLine += statStr + '<br /></span>\n'
        return statLine
    else:
        return ''


def defense(i, side):  # assemble fielding stats per team
    bs = ''
    if (
        fieldingLine(i, side, 'E', 'errors')
    ):
        bs += '<h5>FIELDING</h5>\n'
        bs += fieldingLine(i, side, 'E', 'errors')
    return bs


def box(i, side):  # assemble batting stats per team into boxscore
    team = side + '_team'
    batters = side + '_batters'
    totals = side + '_batter_totals'
    bs = '<h4 style="margin-bottom:5px">'
    bs += i[team]['full_name'] + '</h4>\n'
    bs += """
        <table>
            <thead>
                <tr>
                    <th style="width:150px;">Batting</th>
                    <th>AB</th>
                    <th>R</th>
                    <th>H</th>
                    <th>RBI</th>
                    <th>BB</th>
                    <th>SO</th>
                    <th>LOB</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
"""
    bs += '<td>TOTALS</td>'
    bs += '<td>' + str(i[totals]['at_bats']) + '</td>'
    bs += '<td>' + str(i[totals]['runs']) + '</td>'
    bs += '<td>' + str(i[totals]['hits']) + '</td>'
    bs += '<td>' + str(i[totals]['rbi']) + '</td>'
    bs += '<td>' + str(i[totals]['walks']) + '</td>'
    bs += '<td>' + str(i[totals]['strike_outs']) + '</td>'
    bs += '<td>' + str(i[totals]['left_on_base']) + '</td>'
    bs += """
                </tr>
            </tfoot>
            <tbody>
    """
    for b in i[batters]:
        bs += '<tr>'
        if b['sub_bat_order'] >= 1:
            bs += '<td style="padding-left:20px;padding-right:30px">'
        else:
            bs += '<td style="padding-right:30px">'
        bs += b['display_name'] + ' ' + b['position'] + '</td>'
        bs += '<td>' + str(b['at_bats']) + '</td>'
        bs += '<td>' + str(b['runs']) + '</td>'
        bs += '<td>' + str(b['hits']) + '</td>'
        bs += '<td>' + str(b['rbi']) + '</td>'
        bs += '<td>' + str(b['walks']) + '</td>'
        bs += '<td>' + str(b['strike_outs']) + '</td>'
        bs += '<td>' + str(b['left_on_base']) + '</td>'
        bs += '</tr>'
    bs += """
            </tbody>
        </table>
    """
    return bs


def pitch(i, side):  # Assemble pitcher stats into boxscore
    team = side + '_team'
    pitchers = side + '_pitchers'
    bs = '<h4 style="margin-bottom:5px">'
    bs += i[team]['full_name'] + '</h4>\n'
    bs += """
        <table style='margin-bottom:20px'>
            <thead>
                <tr>
                    <th style="width:150px;">Pitching</th>
                    <th>IP</th>
                    <th>H</th>
                    <th>R</th>
                    <th>ER</th>
                    <th>BB</th>
                    <th>SO</th>
                    <th>HR</th>
                </tr>
            <thead>
            <tbody>
"""
    for p in i[pitchers]:
        bs += '<tr>'
        bs += '<td style="padding-right:30px">'
        bs += p['display_name']
        if p['win'] is True:
            bs += ' (W)'
        elif p['loss'] is True:
            bs += ' (L)'
        elif p['hold'] is True:
            bs += ' (H)'
        elif p['save'] is True:
            bs += ' (S)'
        bs += '</td>'
        bs += '<td>' + str(p['innings_pitched']) + '</td>'
        bs += '<td>' + str(p['hits_allowed']) + '</td>'
        bs += '<td>' + str(p['runs_allowed']) + '</td>'
        bs += '<td>' + str(p['earned_runs']) + '</td>'
        bs += '<td>' + str(p['walks']) + '</td>'
        bs += '<td>' + str(p['strike_outs']) + '</td>'
        bs += '<td>' + str(p['home_runs_allowed']) + '</td>'
        bs += '</tr>'
    bs += """
            </tbody>
        </table>
"""
    return bs


def pitchLine(i):  # Display other pitching stats
    plist = []
    for p in i['away_pitchers']:
        pitchStr = p['display_name'] + ' '
        pitchStr += str(p['pitch_count']) + '-' + str(p['pitches_strikes'])
        plist.append(pitchStr)
    listStr = '; '.join(plist)
    pline = '<span><strong>Pitches-Strikes:</strong> '
    pline += listStr + '<br /></span>\n'
    return pline


def line(i, side):  # assemble each team's row in linescore
    team = side + '_team'
    score = side + '_period_scores'
    totals = side + '_batter_totals'
    errors = side + '_errors'
    ls = '<tr>'
    ls += '<td>'
    ls += i[team]['full_name'] + '</td>\n'
    for inning in i[score]:
        ls += '<td>'
        if side == 'home' and inning == -1:
            ls += 'x'
        else:
            ls += str(inning)
        ls += '</td>\n'
    ls += '<td style="padding-left:15px">'
    ls += str(i[totals]['runs']) + '</td>\n'
    ls += '<td>' + str(i[totals]['hits']) + '</td>\n'
    ls += '<td>' + str(i[errors]) + '</td>\n'
    ls += '</tr>'
    return ls


def linescore(i):  # display linescore
    ls = """
        <table>
            <thead>
                <tr>
                    <th style="width:150px;"> </th>
"""
    innings = 1
    for inning in i['away_period_scores']:
        ls += '<th>' + str(innings) + '</th>\n'
        innings = innings + 1
    ls += """
                    <th style="padding-left:15px">R</th>
                    <th>H</th>
                    <th>E</th>
                </tr>
            </thead>
            <tbody>
"""
    ls += line(i, 'away')
    ls += line(i, 'home')
    ls += """
            </tbody>
        </table>
"""
    return ls


# BOXSCORES
def boxscores():
    # Get yesterday's games and create list of IDs
    yesterday = date.today() - timedelta(1)
    yesterday = date.strftime(yesterday, '%Y%m%d')
    events = xmlstats('events', sport='mlb', date=yesterday)
    games = []
    for e in events['event']:
        games.append(e['event_id'])
    if not games:
        output = '<h2>SCOREBOARD</h2>\n'
        output += '<p>No games scheduled yesterday.</p>\n'
        return output
        exit()

    # Retrieve each boxscore and add to list
    time.sleep(10)
    boxscores = []
    for e in games:
        boxscores.append(xmlstats('boxscore', sport='mlb', event=e))
        time.sleep(10)

    bs = '<h2>SCOREBOARD</h2>'
    for i in boxscores:
        bs += """
<div style="border-top: 1px solid">
    <h3>
"""
        # Final score
        bs += i['away_team']['full_name'] + ' '
        bs += str(i['away_batter_totals']['runs']) + ', '
        bs += i['home_team']['full_name'] + ' '
        bs += str(i['home_batter_totals']['runs'])
        bs += '</h3>'

        # Linescore
        bs += linescore(i)

        # Away offense box and other stats
        bs += box(i, 'away')
        bs += offense(i, 'away')
        bs += defense(i, 'away')

        # Home offense box and other stats
        bs += box(i, 'home')
        bs += offense(i, 'home')
        bs += defense(i, 'home')

        # Pitchers box
        bs += pitch(i, 'away')
        bs += pitch(i, 'home')

        # Other pitching stats
        bs += pitchLine(i)

        # Event information
        # Weather
        bs += '<span><strong>Temperature:</strong> '
        bs += str(i['event_information']['temperature'])
        bs += '<br /></span>\n'

        # Duration
        bs += '<span><strong>T:</strong> '
        bs += i['event_information']['duration']
        bs += '<br /></span>\n'

        # Attendance
        bs += '<span><strong>Att:</strong> '
        bs += str(i['event_information']['attendance'])
        bs += '<br /></span>\n'

        # Venue
        bs += '<span><strong>Venue:</strong> '
        bs += i['event_information']['site']['name']
        bs += '</span>\n'

        bs += """
</div>
"""

    return bs
