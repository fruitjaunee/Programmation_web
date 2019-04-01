#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for

from data import ARTICLES
# Set API dev in an another file


app = Flask(__name__)



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
def about_us():
    app.logger.debug('serving root URL /')
    return render_template('about_us.html', page_title="about_us")




@app.route('/creer_article')
def creer_article():
    return render_template('creer_article.html', page_title = "Help")


@app.route('/articles/')
@app.route('/articles/<nomarticle>/')

def articles(nomarticle=None):
    if not nomarticle:
        return render_template('articles.html' , articles= ARTICLES)
    else:
        for i in range(len(ARTICLES)):
            if ARTICLES[i]['nom'] == nomarticle:
                infos = ARTICLES[i]

        return render_template('articles.html' , articles = ARTICLES, nomarticle=nom, infos=infos)
    abort(404)


@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    req = request.args['pattern']
    for article in ARTICLES:
        if req == article['nom']:
            a = article
    return render_template('articles.html' , articles = ARTICLES, nomarticle=req, infos=a)


@app.route('/articles/<nomarticle>/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
       article ={}
       article['nom'] = request.form['nom']
       article['lien'] = request.form['lien']
       article['date'] = request.form['date']
       
       ARTICLES.append(article)

    return render_template('articles.html', error=error, articles = ARTICLES, infos = article )


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
