
from os import path

import boto3
from botocore.exceptions import ClientError

class Email:
    def __init__(self):
        self.recipients = []
        self.charset = 'UTF-8'

    def set_html(self, html):
        self.html = html

    def set_text(self, text):
        self.text = text

    def set_subject(self, subject):
        self.subject = subject

    def add_recipient(self, address):
        self.recipients.append(address)

    def get_args_for_boto(self):
        assert self.html
        assert self.text

        return {
            'Destination': {
                'ToAddresses': self.recipients,
            },
            'Message': {
                'Body': {
                    'Html': {
                        'Charset': self.charset,
                        'Data': self.html,
                    },
                    'Text': {
                        'Charset': self.charset,
                        'Data': self.text,
                    }
                },
                'Subject': {
                    'Charset': self.charset,
                    'Data': self.subject
                }
            },
        }


class EmailTemplate:
    def __init__(self, template_name, template_dir='./templates/emails/'):
        self.template_name = template_name
        self.template_dir = template_dir
        self.template_html = self.__read_file(
            path.join(template_dir, template_name + '.html'))
        self.template_text = self.__read_file(
            path.join(template_dir, template_name + '.txt'))
        self.subject = None

    def render(self, **kwargs):
        email = Email()
        email.set_html(EmailTemplate.__format(self.template_html, **kwargs))
        email.set_text(EmailTemplate.__format(self.template_text, **kwargs))
        email.set_subject(self.subject)
        return email

    def __read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    @staticmethod
    def __format(html, **kwargs):
        for k, v in kwargs.items():
            key = '{{' + k + '}}'
            if key in html:
                html = html.replace(key, v)
        return html


class EmailClient:
    def __init__(self, config):
        self.client = boto3.client('ses', region_name=config['aws-region'])
        self.config = config

    def send(self, email):
        kwargs = email.get_args_for_boto()
        kwargs['Source'] = kwargs.get('Source', self.config['sender'])

        try:
            self.client.send_email(**kwargs)
        except ClientError as e:
            print(e.response['Error']['Message'])

