#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import USERS
# Set API dev in an another file
from api import SITE_API

app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)


@app.route('/hello_world')
def hello_world():
    app.logger.debug('Hello,World!')
    response = make_response('Hello, World!')
    response.headers['Content-Type'] = "text/plain; charset=utf-8"
    response.headers['Content-Language'] = "en"
    if 'Accept-Language' in request.headers:
        if 'fr' in request.headers['Accept-Language']:
            response.headers.add('Content-Language', 'fr')
            response.data = 'Bonjour le monde'
    return response


@app.route('/')
def index():
    app.logger.debug('serving root URL /')
    return render_template('index.html', page_title="index")


@app.route('/indexapi')
def indexapi():
    return render_template('indexapi.html')


@app.route('/about')
@app.route('/about/<title>')
def about(title="Lorem ipsum"):
    app.logger.debug('about')
    return render_template('about.html', title = 'Un truc chelou en latin', page_title="About")


@app.route('/help')
def help():
    return render_template('help.html', page_title = "Help")


@app.route('/users/')
@app.route('/users/<username>/')

def users(username=None):
    if not username:
        return render_template('users.html' , users= USERS )
    else:
        for i in range(len(USERS)):
            if USERS[i]['name'] == username:
                nom = USERS[i]['name']
                celebrity = USERS[i]

        return render_template('users.html' , users = USERS, username=nom, infos=celebrity)
    abort(404)


@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    req = request.args['pattern']
    for user in USERS:
        if req == user['name']:
            celebrity = user
    return render_template('users.html' , users = USERS, username=req, infos=celebrity)


@app.route('/users/<username>/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
       new_guy ={}
       new_guy['name'] = request.form['name']
       new_guy['gender'] = request.form['gender']
       new_guy['birth'] = request.form['birth']
       new_guy['wikipageid'] = request.form['wikipageid']
       USERS.append(new_guy)

    return render_template('users.html', error=error, users = USERS, infos = new_guy )


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
