#!/usr/bin/env python

# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Generic script to allow ITRS to send email.  The recipients are passed
# as sys.argv[1] and can can be comma or space separated.  If no recipients
# are specified then just exit immediately.  Uses the environment set
# by itrs to create the contents
#
# Author: Andrew Lister

import os
import sys
import json
from alx.app import ALXapp
from alx.mail import ALXmail
from alx.itrs.alert import HtmlAlert
from alx.itrs.environment import Environment


args = [
    ['recipients', {'nargs': '*', 'default': '',
                    'help': 'space separated list of recipients'}]
]

app = ALXapp("Send an email from ITRS Geneos", args=args)

recipients = app.arguments.recipients
if len(recipients) == 0:
    sys.exit(0)

e = Environment()

subject = ("%s: %s - %s %s %s is %s" %
           (e.severity.title(), e.managed_entity, e.sampler,
            e.rowname, e.column, e.value))

mail = ALXmail()
mail.set_from(app.sender)

for r in recipients:
    mail.add_recipient(r)

mail.set_subject(subject)

alert = HtmlAlert(e)
html = alert.create()

mail.add_html(html)

app.logger.info("Sending %s to %s", subject, format(recipients))

# In a real world scenario, the email would be sent using the code below
# Just display the whole message instead and exit. As the environment is
# not set up, there will be a lot of 'None' values
print(mail._get_mime_message())
exit(0)

try:
    mail.send()
except Exception as e:
    app.logger.error("Send failure: %s", format(e))
