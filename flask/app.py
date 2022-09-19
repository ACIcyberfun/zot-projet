#! /usr/bin/python
# -*- coding:utf-8 -*


# On charge les dépendances logicielles 
from flask import Flask, request, render_template, redirect, url_for
from tinydb import TinyDB, Query
from slugify import slugify

app = Flask(__name__)

# On défini l'endroit ou est stocké la base de donnée :
db = TinyDB('./db.json')


'''
Projet Example
'''


# On teste l'appli avec la route par default.
@app.route("/")
def index():
    context = {
        'premiere_variable': 'CyB3rFun',
        'seconde_variable': 'PopopoooOOoo'
    }
    return render_template('daju/index.html', context=context)


# On teste avec une route qui contient une variable.
# Exemple : /game/123
@app.route('/game/<int:score>')
def game(score):
    return render_template('test/int.html', score=score)


'''
ZotProjet
'''

@app.route('/form', methods=['POST', 'GET'])
def formulaire():
    if request.method == 'GET':
        # Alors c'est que le formulaire est vide
        return render_template('daju/form.html')

    if request.method == 'POST':

        # on vérifie que le formulaire est bien rempli :
        url = request.form.get("url")
        nomdelasociete = request.form.get("nomdelasociete")
        soustitre = request.form.get("soustitre")
        texte = request.form.get("texte")
        email = request.form.get("email")
        phone = request.form.get("phone")
        tempc = request.form.get("tempc")

        slug = slugify(nomdelasociete)

        # import ipdb; ipdb.set_trace()
        print(f'slug : {slug}, tempc: {tempc}')
        if nomdelasociete:
            print(f'nomdelasociete : {nomdelasociete}')

            # On lance la recherche dans la base de donnée
            Client: Query = Query()
            # noinspection PyTypeChecker
            client = db.search(Client.slug == slug)

            # Si le nombre de clients trouvé = 0
            # Alors le client n'existe pas, on l'enregistre dans la base de donnée
            if len(client) == 0:
                print(f'client : {client}')
                db.insert({
                    "url": url,
                    "nomdelasociete": nomdelasociete,
                    "soustitre": soustitre,
                    "texte": texte,
                    "email": email,
                    "phone": phone,
                    "tempc":tempc,
                    "slug":slug,
                })
                print(f'redirect vers  : /{slug}')
                return redirect(f'/{slug}')

            else:
                return 'existe déja ! Merci de rentrer un autre nom'
        return 'Pas de nom de société'


# noinspection PyUnresolvedReferences,PyTypeChecker
@app.route('/<slug>')
def templater(slug):
    print(f'GET /{slug}')
    Client = Query()
    client = db.search(Client.slug == slug)
    print(f'GET /{slug}')

    # Si le client existe, la longueur des objets trouvés
    # en base de donnée est suppérieur a 0 ( = 1 )
    if len(client) > 0:

        # Si plusieurs templates possible, *
        # on va chercher le nom du dossier
        # dossier_du_template = "cheflo"
        if client[0].get('tempc') == "3" :
            return render_template(f"papertemp/index.html", context=client[0])
        return render_template(f"test/client.html", client=client[0])



    # Sinon, ça veut dire que le client n'existe pas en base de donnée,
    # on renvoie vers la page formulaire.
    else:
        return redirect(url_for('formulaire'))

# flask run --reload --host=0.0.0.0
