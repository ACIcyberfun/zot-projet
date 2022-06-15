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
    'premiere_variable':'CyB3rFun',
    'seconde_variable': 'PopopoooOOoo'
    }
    return render_template('test/index.html', context=context)


# On teste avec une route qui contient une variable.
# Exemple : /game/123
@app.route('/game/<int:score>')
def game(score):
   return render_template('test/int.html', score = score)


'''
ZotProjet
'''

@app.route('/form', methods = ['POST', 'GET'])
def formulaire():
    if request.method == 'POST':
        
        # on vérifie que le formulaire est bien rempli :
        name = request.form.get('name')
        description = request.form.get('desc')
        slug = slugify(name)

        if name and description :

            # On lance la recherche dans la base de donnée
            Client = Query()
            client = db.search(Client.slug == slug)
            
            # Si le nombre de client trouvé = 0
            # Alors le client n'existe pas, on l'enregistre dans la base de donnée
            if len(client) == 0 :
                db.insert({
                    'slug': slug, 
                    'name': name,
                    'description': description,
                    })

                return redirect(f'/{slug}')

            else :
                return 'existe déja ! Merci de rentrer un autre nom'

    # Si la méthode n'est pas POST
    # Alors c'est que le formulaire est vide
    # On demande à le remplir
    return render_template('test/form.html')


@app.route('/<slug>')
def templater(slug):
    Client = Query()
    client = db.search(Client.slug == slug)
    if len(client) > 0 :
        return render_template('test/client.html', client=client[0])
        # return render_template('story/index.html', client=client[0])
    else :
        return redirect(url_for('formulaire'))




# flask run --reload --host=0.0.0.0