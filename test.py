import unittest
from flask_testing import TestCase
from app import app, db, Product

# Définit la classe de test qui hérite de TestCase
class TestSupprimerProduit(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utiliser une bdd temporaire en mémoire pour les tests
        return app




    def test_supprimer_produit(self):
        # Récupérer l'id du produit à supprimer 
        n_id = Product.query.filter_by(id='5').first().id

        with self.client:
            response = self.client.post(f'/supprimer_produit/{n_id}', follow_redirects=True)

            self.assertEqual(response.status_code, 200)  # Vérifier si la requête a réussi

            # Vérifier que le produit a été supprimé de la bdd
            n_in_db = Product.query.filter_by(id='5').first()
            self.assertIsNone(n_in_db)  # Assurer que le produit n'existe plus dans la base de données

if __name__ == '__main__':
    unittest.main()





