import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = [YOUR_APP_NAME]


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir,
        [YOUR_CREDENTIAL_JSON_FILE_NAME]
    )

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def stathead(stat):
    output = '<td><strong>' + stat + '</strong></td>\n'
    output += '<td><strong>' + stat + '</strong></td>\n'
    return output


def category(data, category=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = [YOUR_SPREADSHEET_ID]
    rangeName = data

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    output = """
<table>
    <tbody>
"""
    for i in values:
        output += '<tr>\n'
        output += '<td>' + i[0] + '.</td>\n'
        output += '<td style="width:220px">' + i[1] + ', ' + i[2] + '</td>\n'
        output += '<td>'
        if category == '3d':
            output += str('{0:.3f}'.format(float(i[3]))).lstrip('0')
        elif category == '2d':
            output += str('{0:.2f}'.format(float(i[3])))
        elif category == '1d':
            output += str('{0:.1f}'.format(float(i[3])))
        else:
            output += i[3]
        output += '</td>\n'
        output += '</tr>\n'

    output += """
    </tbody>
</table>
"""

    return output


def leaders():

    output = '<h2>LEAGUE LEADERS</h2>'
    output += '<h3>Batting</h3>'
    output += """
<table>
    <thead>
        <tr>
"""
    output += '<th>American League</th>\n'
    output += '<th>National League</th>\n'
    output += """
        </tr>
    </thead>
    <tbody>
        <tr>
"""
    output += stathead('Batting Average')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A2:D11', '3d') + '</td>'
    output += '<td>' + category('Sheet1!E2:H11', '3d') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Home Runs')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A13:D22') + '</td>'
    output += '<td>' + category('Sheet1!E13:H22') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Runs Batted In')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A24:D33') + '</td>'
    output += '<td>' + category('Sheet1!E24:H33') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Stolen Bases')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A35:D44') + '</td>'
    output += '<td>' + category('Sheet1!E35:H44') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('On-Base Percentage')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A46:D55', '3d') + '</td>'
    output += '<td>' + category('Sheet1!E46:H55', '3d') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('OPS')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A57:D66', '3d') + '</td>'
    output += '<td>' + category('Sheet1!E57:H66', '3d') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('wRC+')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A68:D77') + '</td>'
    output += '<td>' + category('Sheet1!E68:H77') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('fWAR')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!A79:D88', '1d') + '</td>'
    output += '<td>' + category('Sheet1!E79:H88', '1d') + '</td>'
    output += """
        </tr>
    </tbody>
</table>
"""
    output += '<h3>Pitching</h3>'
    output += """
<table>
    <thead>
        <tr>
"""
    output += '<th>American League</th>\n'
    output += '<th>National League</th>\n'
    output += """
        </tr>
    </thead>
    <tbody>
        <tr>
"""
    output += stathead('Wins')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I2:L11') + '</td>'
    output += '<td>' + category('Sheet1!M2:P11') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Strikeouts')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I13:L22') + '</td>'
    output += '<td>' + category('Sheet1!M13:P22') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Earned Run Average')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I24:L33', '2d') + '</td>'
    output += '<td>' + category('Sheet1!M24:P33', '2d') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('Saves')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I35:L44') + '</td>'
    output += '<td>' + category('Sheet1!M35:P44') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('xFIP')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I46:L55', '2d') + '</td>'
    output += '<td>' + category('Sheet1!M46:P55', '2d') + '</td>'
    output += """
        </tr>
        <tr>
"""
    output += stathead('fWAR')
    output += """
        </tr>
        <tr>
"""
    output += '<td>' + category('Sheet1!I57:L66', '1d') + '</td>'
    output += '<td>' + category('Sheet1!M57:P66', '1d') + '</td>'
    output += """
        </tr>
    </tbody>
</table>
"""

    return output
