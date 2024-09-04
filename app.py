from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/products' # Configurer l'URI pour la bdd SQLite à utiliser
db = SQLAlchemy(app)#Créer un objet (db) SQLAlchemy  pour les opérations de bdd
app.secret_key = 'GAz0m_WbOYvUCWcSQ7pwDZ6efxdmo0Ty'
admin_username = "admin"
admin_password = "adminpass"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)

    description = db.relationship('Ingredient', backref='product', lazy=True)

    # Relation avec EffetSecondaire
    effet_secondaire_id = db.Column(db.Integer, db.ForeignKey('effet_secondaire.id'), nullable=True)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class EffetSecondaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Relation avec Product
    products = db.relationship('Product', backref='effet_secondaire', lazy=True)


@app.route('/')
def index():
    return render_template('index.html')   


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == admin_username and password == admin_password:
            # rediriger vers la page d'administration
            return redirect(url_for('admin'))
        else:
            # connexion échouée afficher un message d'erreur
            error_message = "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer."
            return render_template('connexion.html', error_message=error_message)

    return render_template('connexion.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/produit')
def produit():
    products = Product.query.all()
    return render_template('produit.html', products=products)


@app.route('/produit/<int:id>')
def detail_prod(id):
    # Récupérer les details du produit à partir de la bdd 
    products = Product.query.get(id)
    if products:
        return render_template('detail_prod.html', products=products)
    

@app.route('/ajout_produit', methods=['GET','POST'])
def ajout_produit():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        file = request.files['file']
        # Enregistrer l'image dans un dossier
        file.save('static/image/' + file.filename)

        # Ajouter le produit à la bdd
        new_product = Product(nom=nom,description=description, file=file.filename)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('liste_produit'))

    return render_template('ajout_produit.html')



@app.route('/liste_produit')
def liste_produit():
    products = Product.query.all()
    return render_template('liste_produit.html', products=products)



@app.route('/search_products', methods=['GET'])
def search_products():
    search_query = request.args.get('search_query', '')
    
    if search_query:
        # Effectuer la recherche dans la bdd en fonction de la requête
        search_results = Product.query.filter(Product.nom.ilike(f'%{search_query}%')).all()
        
        if search_results:
            return render_template('produit.html', products=search_results, search_query=search_query, no_results=False)
        else:
            return render_template('produit.html', no_results=True, search_query=search_query)
    
    else:
        p = Product.query.all()
        return render_template('index.html', products=p, no_results=False)


@app.route('/supprimer_produit/<int:id>', methods=['POST'])
def supprimer_produit(id):
    # Récupérer l'id de produit à supprimer
    product = Product.query.get(id)
    if request.method == 'POST' and product:
        # Supprimer le produit de la bdd
        db.session.delete(product)
        db.session.commit()
        # Rediriger vers la page de produits
        return redirect(url_for('liste_produit'))





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('connexion'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)











