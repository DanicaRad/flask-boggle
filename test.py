from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up tests"""
        self.client = app.test_client()
        app.config['TESTING'] = True
    # TODO -- write tests for every view function / feature!

    def test_homepage(self):

        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('game_num'))
            self.assertIn('<h1>Play Boggle!</h1>', html)
            self.assertIn('Timer:', html)
            self.assertIn('<td>', html)

    def test_valid_word(self):
        """Test if word is valid and on board by creating board in session"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G']]

            res = self.client.get('/check-word?guess=dog')
            self.assertEqual(res.json['result'], 'ok')

            res2 = self.client.get('/check-word?guess=go')
            self.assertEqual(res2.json['result'], 'ok')

    def test_not_valid_word(self):
        """Test if word is not on board"""

        self.client.get('/')
        res = self.client.get('/check-word?guess=hello')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_word(self):
        """Test if word is not a valid english word"""

        self.client.get('/')
        res = self.client.get('/check-word?guess=kljnfdg')
        self.assertEqual(res.json['result'], 'not-word')