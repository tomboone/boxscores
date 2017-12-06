#!/usr/bin/python3
from boxscores import boxscores
from standings import standings
from leaders import leaders

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

addr_to = [YOUR_EMAIL_ADDRESS]
addr_from = 'Python Baseball Times <[YOUR_FROM_EMAIL_ADDRESS]>'
smtp_server = [YOUR_SMTP_SERVER]
smtp_user = [YOUR_SMTP_USERNAME]
smtp_pass = [YOUR_SMTP_PASSWORD]

msg = MIMEMultipart('alternative')
msg['To'] = addr_to
msg['From'] = addr_from
msg['Subject'] = 'Daily MLB Report'

text = 'This email is not available in plain text.'

html = """
<html>
    <head>
        <style>
            td, th {padding: 3px}
            thead, tbody {
                border-bottom: 1px solid #747678;
            }
            thead {
                border-top: 1px solid #747678;
                background-color: #dddddd
                }
            div {margin-bottom: 30px}
            h5 {margin-bottom: 5px}
            tfoot tr td {
                background-color: #dddddd;
                font-weight: bold
            }
        </style>
    </head>
    <body style="font-size: 14px; font: Arial, Sans-serif;">
"""
html += boxscores()
html += '<hr />'
html += standings()
html += '<hr />'
html += leaders()
html += """
    </body>
</html>
"""
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html', _charset='iso-8859-1')

msg.attach(part1)
msg.attach(part2)

s = smtplib.SMTP_SSL(smtp_server, 465)
s.login(smtp_user, smtp_pass)
s.sendmail(addr_from, addr_to, msg.as_string())
s.quit()
