"""
Flask routes for liten API.
To start the Flask server do the following -
flask --app=litenapp.py run
See the docstring below for the api routes. These Restful calls can be made from the browser or from a client.
"""

import sys
import json
import litenai as tenai

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/create/<session_name>")
def create_session(session_name):
    """
    create or get a session with the given session_name.
    If creating these default config values are used -
    OpenAI API key to for API calls
    "OPENAI_API_KEY" : "<insert your litenkey here>"
    Spark local IP where  master is running. If local do local[1] or 
    "SPARK_MASTER_URL" : "local[2]"
    Liten Datalake URL - assumes litenlakehouse.py is here for file scheme
    "LITEN_LAKEHOUSE_URL": "file:///content/samplelogfiles/"
    Pass them as args to override these.
    Example:
    http://127.0.0.1:5000/create/test?LITEN_LAKEHOUSE_URL=file:/home/hkverma/work/samplelogfiles&OPENAI_API_KEY=sk-xxxxxxx&SPARK_MASTER_URL=local[2]
    """
    session = None
    try:
        if tenai.Session.exists(session_name):
            session = tenai.Session.get(session_name)
        if not session:
            session = tenai.Session(session_name, "")
            for key, value in request.args.items():
                if not session.config.set_config(key, value):
                    return f"Cannot set invalid config name {key} to {value}", 406
            session.init()
    except Exception as exc:
        error_message = f"Failed to create session {session_name} with Exception={exc}"
        return error_message, 406
    if not session:
        return f"Failed to create session {session_name}", 406
    return f"Session {session_name} created or retrieved successfully", 200

@app.route("/append/<session_name>/<prompt>")
def append_user_message(session_name, prompt):
    """
    get a session with the given session_name
    If creating use the config file_name
    """
    session = None
    try:
        session = tenai.Session.get(session_name)
    except Exception as exc:
        error_message = f"Failed to get session {session_name}. Exception={exc}"
        return error_message, 406
    if not session:
        return f"Failed to get session {session_name}", 406
    try:
        session.context.user(prompt)
    except Exception as exc:
        error_message = f"Failed to append user prompt {prompt}. Exception={exc}"
        return error_message, 500
    return "Added user prompt successfully", 200


@app.route("/ask/<session_name>/<prompt>")
def ask_liten(session_name, prompt):
    """
    Ask to complete prompt for session_name
    Example:
    http://127.0.0.1:5000/ask/test/%22What%20are%20status%20code%20errors%22
    """
    session = None
    try:
        session = tenai.Session.get(session_name)
    except Exception as exc:
        error_message = f"Failed to get session {session_name}. Exception={exc}"
        return error_message, 406
    if not session:
        return f"Failed to get session {session_name}", 406
    chat_response = ""
    try:
        chat_response= session._openai.complete_prompt_chat(prompt)
    except Exception as exc:
        error_message = f"Failed ask for user prompt {prompt}. Exception={exc}"
        return error_message, 500
    return chat_response, 200

@app.route("/send/<session_name>/<prompt>")
def send_liten(session_name, prompt):
    """
    Send to complete prompt for session_name. Master agent identifies the action from the prompt and completes it using the appropriate agent.
    Example:
    http://127.0.0.1:5000/send/xxx/%22Generate%20sql%20for%20the%20following.%20Select%20top%20100%20rows.%22
    """
    session = None
    try:
        session = tenai.Session.get(session_name)
    except Exception as exc:
        error_message = f"Failed to get session {session_name}. Exception={exc}"
        return error_message, 406
    if not session:
        return f"Failed to get session {session_name}", 406    
    resp = session.get_response_for_send(prompt)
    if resp.derr:
        return f"Failed to send user prompt with error {response.derr}", 406
    resp_str = ""
    if resp.dout:
        resp_str = resp.dout + "\n"
    resp_str = resp_str + resp.d
    return resp_str, 200