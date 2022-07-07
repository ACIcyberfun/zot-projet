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
def test_template():
    context = {
        'premiere_variable': 'CyB3rFun',
        'seconde_variable': 'PopopoooOOoo'
    }
    return render_template('accueil/accueil.html', context=context)


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
        return render_template('test/form.html')

    if request.method == 'POST':

        # on vérifie que le formulaire est bien rempli :
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        adressemail = request.form.get("adressemail")
        secteur = request.form.get("secteur")
        nomdelasociete = request.form.get("nomdelasociete")
        couleur = request.form.get("couleur")
        url_logo = request.form.get("url_logo")
        # formFileSm = request.form.get("formFileSm")
        # formFileLg = request.form.get("formFileLg")
        flex_radio_default = request.form.get("flexRadioDefault")
        slogan = request.form.get("slogan")
        example_form_control_textarea1 = request.form.get("exampleFormControlTextarea1")

        slug = slugify(nomdelasociete)

        # import ipdb; ipdb.set_trace()
        print(f'slug : {slug}')
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
                    "slug": slug,
                    "nom": nom,
                    "prenom": prenom,
                    "adressemail": adressemail,
                    "secteur": secteur,
                    "nomdelasociete": nomdelasociete,
                    "couleur": couleur,
                    "flexRadioDefault": flex_radio_default,
                    "slogan": slogan,
                    "exampleFormControlTextarea1": example_form_control_textarea1,
                    "url_logo": url_logo,
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
        dossier_du_template = "cheflo"
        return render_template(f"{dossier_du_template}/index.html", client=client[0])

    # Sinon, ça veut dire que le client n'existe pas en base de donnée,
    # on renvoie vers la page formulaire.
    else:
        return redirect(url_for('formulaire'))

# flask run --reload --host=0.0.0.0
