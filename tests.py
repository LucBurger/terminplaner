import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post, Team

#Übernommen aus den Beispielen
class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

#Übernommen aus den Beispielen
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

#Übernommen aus den Beispielen
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

#Übernommen aus den Beispielen
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

#Übernommen aus den Beispielen mit Anpassungen
    def test_mitglied(self):
        u1 = User(username='john', email='john@example.com')
        t2 = Team(teamname='Hoppluc', beschreibung='komm schon')
        db.session.add(u1)
        db.session.add(t2)
        db.session.commit()
        self.assertEqual(u1.mitglied.all(), [])
        self.assertEqual(u1.mitglieder.all(), [])

        u1.beitreten(t2)
        db.session.commit()
        self.assertTrue(u1.is_member(t2))
        self.assertEqual(u1.mitglied.count(), 1)
        self.assertEqual(u1.mitglied.first().teamname, 'Hoppluc')
        self.assertEqual(t2.mitglieder.count(), 1)
        self.assertEqual(t2.mitglieder.first().username, 'john')

        '''u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)'''

if __name__ == '__main__':
    unittest.main(verbosity=2)