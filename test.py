from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def test_home_route(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="h2">Welcome to the  Boggle game!</h2>', html)

    def  test_board_submission(self):
        with app.test_client() as client:
            res = client.post('/board', data={'board', '["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]''})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<table class="board">{% for row in board %}<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>{% endfor %</table>', html)

    def test_post_score(self):
        with app.test_client() as client:
            res = client.get('/post-score')

            self.assertIsNone(session.post('highscore'))
            self.asserIn(' <p class="p">High Score:</p> <span id="highScore">0</span>', res.data)
    
    def test_get_stats(self):
        with app.test_client() as client:
            res = client.get('/get-stats')

            self.asserIn(' <p class="p">High Score:</p> <span id="highScore">0</span>', res.data)