import os
import requests
from flask import Flask, render_template, session
from identity.flask import Auth
import app_config
from utils import optional_auth

app = Flask(__name__)
app.config.from_object(app_config)

# Enable session handling
app.secret_key = app.config.get('SECRET_KEY')
app.config['SESSION_TYPE'] = app.config.get('SESSION_TYPE')

# Create auth instance
auth = Auth(
    app,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
    redirect_uri=app.config["REDIRECT_URI"]
)

# Add auth instance to app context
app.auth_instance = auth

@app.route("/")
@optional_auth
def index(*, context):
    return render_template(
        'index.html',
        user=context['user'],
        title="Flask Web App Sample",
        api_endpoint=os.getenv("ENDPOINT")
    )

@app.route("/call_api")
@optional_auth(scopes=os.getenv("SCOPE", "").split())
def call_downstream_api(*, context):
    api_result = requests.get(
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="Graph API Response", result=api_result)