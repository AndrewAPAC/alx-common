# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Never store plain text passwords again!

from alx.app import ALXapp
import sys

args = [
    ['string'],
    ['-d', '--decrypt', {'action': 'store_true', 'default': False}]
]

app = ALXapp("Password encryption tool", args=args)

string = app.arguments.string

if not app.arguments.decrypt:
    string = app.encrypt(string)
    print("Encrypted: " + string)

print("Decrypted: " + app.decrypt(string))

sys.exit(0)
