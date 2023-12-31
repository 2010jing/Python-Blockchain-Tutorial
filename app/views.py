import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.

CONNECT_NODE_ADDRESS = 'http://127.0.0.1:8000'

posts = []


@app.route('/fetch')
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = f'{CONNECT_NODE_ADDRESS}/chain'
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain['chain']:
            for tx in block['transactions']:
                tx['index'] = block['index']
                tx['hash'] = block['previous_hash']
                content.append(tx)
        print(content)
        global posts
        posts = sorted(content, key=lambda k: k['timestamp'], reverse=True)


@app.route('/')
def index():
    fetch_posts()
    print()
    return render_template('index.html',
                           title='Cat cat cat ...',
                                 posts=posts,
                                 node_address=CONNECT_NODE_ADDRESS,
                                 readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form['content']
    author = request.form['author']
    img = request.form['img']

    post_object = {
        'author': author,
        'content': post_content,
        'img': img
    }

    # Submit a transaction
    new_tx_address = f'{CONNECT_NODE_ADDRESS}/new_transaction'

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
