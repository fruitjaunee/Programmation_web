#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import abort, request, make_response
from flask import render_template, redirect, url_for
from flask import send_from_directory
import json
import datetime

from data import ARTICLES
# Set API dev in an another file


app = Flask(__name__)


@app.route('/')
def about_us():
    app.logger.debug('serving root URL /')
    return render_template('about_us.html', page_title="Qui sommes nous?")



@app.route('/creer_article/', methods=['POST','GET'])
def creer_article():
    if request.method == 'GET':
        return render_template('creer_article.html', page_title = "Créez votre article")
    
    elif request.method == 'POST':
        app.logger.debug(request.form)
        nom=request.form["nom"]
        date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        article=request.form["article"]
        lien="./articles/"+nom+".txt"
        nouvel_article=open(lien, "w")
        nouvel_article.write(article)
        nouvel_article.close()

        with open('data.json') as js:
            DATA = json.load(js)
        
        new_article = {}
        new_article["nom"] = nom
        new_article["lien"] = lien
        new_article["date"]= date
        ARTICLES.append(new_article)
        DATA.get("ARTICLES").append(new_article)


        with open('data.json', 'w') as outfile:
            json.dump(DATA, outfile)
        
        return render_template('envoi_article.html')




def find_article(nom_article):
    for i in ARTICLES :
        if i['nom']==nom_article:
            nom=i["nom"]
            lien=i["lien"]
            date=i["date"]
            mon_fichier = open(lien,"r")
            contenu=mon_fichier.read()
            mon_fichier.close()
    return (nom_article, nom, lien, date,contenu)

@app.route('/articles/')
@app.route('/articles/<nomarticle>/')

def articles(nomarticle=None):
    if not nomarticle:
        return render_template('articles.html' , articles= ARTICLES)
    else:
        (nom_article, nom, lien, date, contenu)=find_article(nomarticle)
        return render_template('articles.html' , article=[nomarticle, nom, lien, date, contenu])



@app.route('/search/', methods=['GET'])
def search():
    app.logger.debug(request.args)
    req = request.args["pattern"]
    A=[]
    for article in ARTICLES:
        A.append(article["nom"])
        if req in A:
            return (articles(req))


@app.route('/articles/<nomarticle>/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
       article ={}
       article['nom'] = request.form['nom']
       article['lien'] = request.form['lien']
       article['date'] = request.form['date']
       
       ARTICLES.append(article)

    return render_template('articles.html', error=error, articles = ARTICLES, infos = article , page_title = "Articles")


# Script starts here
if __name__ == '__main__':
    from os import environ
    DEBUG = environ.get('DEBUG')
    app.run(port=8000, debug=DEBUG)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
