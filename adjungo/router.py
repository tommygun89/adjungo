from flask import Flask, request, jsonify, abort
from flask_reqarg import request_args
from slackclient import SlackClient
from event_handler import EventHandler
from enum import Enum
import os


class EventRequestTypes(Enum):
    CREATE = 'create'
    CANCEL = 'cancel'
    UPDATE = 'update'


app = Flask(__name__)
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
INTERNAL_ERROR = 500
slack_client = SlackClient("")
event_handler = EventHandler()


@app.route("/begin_auth", methods=["GET"])
def oauth_begin():
    return '''
        <a href="https://slack.com/oauth/authorize?scope=team%3Aread+users%3Aread+channels%3Aread&client_id={1}">
            Add to Slack
        </a>
    '''.format(client_id) # TODO Ugly, redo


@app.route("/finish_auth", methods=["GET", "POST"])
def oauth_finish():
    auth_response = slack_client.api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=request.args['code']
    )
    os.environ["SLACK_USER_TOKEN"] = auth_response['access_token']
    return "oAuth successfully complete!"


@app.route("/adjungo", methods=["GET", "POST"])
def slash_command_issued():
    args = request.form.get('text').split(' ')
    if args[0] == EventRequestTypes.CREATE:
        return event_handler.create_event(args[1])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = 'localhost'
    app.run(host=host, port=port, debug=True)
