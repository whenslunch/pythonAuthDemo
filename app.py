import os
import requests
from flask import Flask, render_template
from identity.flask import Auth
import app_config

app = Flask(__name__)
app.config.from_object(app_config)

auth = Auth(
    app,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
    redirect_uri=app.config["REDIRECT_URI"]
)

@app.route("/")
@auth.login_required
def index(*, context):
    return render_template(
        'index.html',
        user=context['user'],
        title="Flask Web App Sample",
        api_endpoint=os.getenv("ENDPOINT") # added this line
    )

@app.route("/call_api")
@auth.login_required(scopes=os.getenv("SCOPE", "").split())
def call_downstream_api(*, context):
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="Graph API Response", result=api_result)