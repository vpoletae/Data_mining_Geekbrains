from webexteamssdk import WebexTeamsAPI, Webhook
import os
import sys
import shutil
import requests
from flask import Flask, request
from urllib.parse import urljoin
from ngrok_launcher import ngrok_launcher
from flask import render_template
import tempfile
import pandas as pd
from datetime import datetime

from EOA_converter import eoa_convert
from EOA_text_parser import eoa_text_parse, clean_docs
from EOA_help_data import *
from EOA_due_diligence import *
from EOA_mailer import *

today = datetime.strftime(datetime.date(datetime.today()), '%d_%m_%Y')
PATH_TO = os.path.dirname(os.path.abspath(__file__))
docs_folder = 'docs'
file_name_webex = 'webex_config.txt'

NGROK_CLIENT_API_BASE_URL = "http://localhost:4040/api"
WEBHOOK_NAME = "attachement_ngrok_webhook"
WEBHOOK_RESOURCE = "messages"
WEBHOOK_EVENT = "created"

with open(os.path.join(PATH_TO, file_name_webex), 'r') as f:
    content = f.readlines()
    webex_token = content[0].split(':')[1].strip()
    webex_bot_name = content[2].split(':')[1].strip()

api = WebexTeamsAPI(webex_token)

def get_ngrok_public_url():
    """Get the ngrok public HTTP URL from the local client API."""
    try:
        response = requests.get(url=NGROK_CLIENT_API_BASE_URL + "/tunnels",
                                headers={'content-type': 'application/json'})
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("Could not connect to the ngrok client API; "
              "assuming not running.")
        return None
    finally:
        for tunnel in response.json()["tunnels"]:
            if tunnel.get("public_url", "").startswith("https://"):
                print("Found ngrok public HTTP URL:", tunnel["public_url"])
                return tunnel["public_url"]

def delete_webhooks_with_name(api, name):
    """Find a webhook by name."""
    for webhook in api.webhooks.list():
        if webhook.name == name:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)

def create_ngrok_webhook(api, ngrok_public_url):
    """Create a Webex Teams webhook pointing to the public ngrok URL."""
    print("Creating Webhook...")
    webhook = api.webhooks.create(
        name=WEBHOOK_NAME,
        targetUrl=ngrok_public_url,
        resource=WEBHOOK_RESOURCE,
        event=WEBHOOK_EVENT,
    )
    print(webhook)
    print("Webhook successfully created.")
    return webhook

def delete_create_webhook():
    """Delete previous webhooks. If local ngrok tunnel, create a webhook."""
    ngrok_launcher()
    delete_webhooks_with_name(api, name=WEBHOOK_NAME)
    public_url = get_ngrok_public_url()
    if public_url is not None:
        create_ngrok_webhook(api, public_url)

# upload initial xls database
df_upd = create_df()
did_party_pids_dict = create_did_party_pids_dict(df_upd)
accounts_dates = create_accounts_dates_df(df_upd)

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET', 'POST'])
def webex_response():
    if request.method == 'POST':
        json_data = request.json
        # Create a Webhook object from the JSON data
        webhook_obj = Webhook(json_data)
        room = api.rooms.get(webhook_obj.data.roomId)
        message = api.messages.get(webhook_obj.data.id)
        person = api.people.get(message.personId)
        print(person)
        me = api.people.me()
        if message.personId == me.id:
            # Message was sent by me (bot); do not respond.
            return 'OK'
        else:
            if message.text:
                api.messages.create(roomId=room.id, text='Please attach EOA!')
            else:
                api.messages.create(roomId=room.id, markdown='{0}'.format('Thank you! Your request is being processed'))
                eoa_file = f'EOA_{person.lastName}_{today}.pdf'
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    headers = {"Authorization": "Bearer {}".format(webex_token)}
                    req = requests.get(message.files[0], headers=headers)
                    tmp.write(req.content)
                    tmp.flush()
                    shutil.copy(tmp.name, os.path.join(PATH_TO, docs_folder, eoa_file))

        eoa_convert()
        eoa_doc_type, eoa_party, eoa_date, eoa_pids = eoa_text_parse()

        api.messages.create(roomId=room.id, text=f'Doc type: {eoa_doc_type}')
        api.messages.create(roomId=room.id, text=f'3d party: {eoa_party}')
        api.messages.create(roomId=room.id, text=f'Date: {eoa_date}')
        api.messages.create(roomId=room.id, text=f'Pids: {eoa_pids}')

        clean_docs(eoa_file)
        # if eoa_party: # adjust logic
        #     eoa_party_adj = translate(eoa_party)
        # the_closest_account, the_closest_date, the_closest_ratio = find_the_closest(accounts_dates, eoa_party_adj)
        
        # # due diligence stage
        # checked_doc_type = check_doc_type(eoa_doc_type)
        # checked_date = check_date(eoa_date, the_closest_date)
        # similarity_ratio = check_pids(eoa_pids, did_party_pids_dict)

        # # mailing block
        # send_from, send_to, subject = create_head()
        # text = create_body(person.displayName, person.emails[0], checked_doc_type,
        #                     checked_date[0], checked_date[1], eoa_party,
        #                     the_closest_account, the_closest_ratio, similarity_ratio)
        # send_mail(send_to, subject, send_from, text, eoa_file)
        return 'OK'

    elif request.method == 'GET':
        return 'OK'

if __name__ == '__main__':
    delete_create_webhook()
    flask_app.run(port=5000)
