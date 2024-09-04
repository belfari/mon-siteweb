import unittest
from flask_testing import TestCase
from app import app, db

class TestajoutProduit(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utiliser une base de données temporaire en mémoire pour les tests
        return app




    def test_ajout_produit(self):
     #ouvre le fichier image en mode binaire
     with open('static/image/nutella.jpg', 'rb') as img_file:
      response = self.client.post('/ajout_produit', data=dict(
        nom='nutella',  # Nom du produit
        quantite='20',   # Quantité
        description='Pâte à tartiner au chocolat et aux noisettes',  # Description
        effet1='xxxxxx',  # Effet
        file=(img_file, 'nutella.jpg')  # Fichier image
      ), follow_redirects=True)
      # Vérifier si la requete a reussi
      self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()

