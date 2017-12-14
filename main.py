#!/usr/bin/env python3

import json
import sys

from messaging.email import EmailClient, EmailTemplate

with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

client = EmailClient(config['ses'])
template = EmailTemplate('example')
em = template.render(message='Hello, world.')
em.add_recipient('jane.doe@example.com')
em.set_subject('Amazon SES Test')
client.send(em)

