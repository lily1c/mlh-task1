import os
import unittest

os.environ['TESTING'] = 'true'

from app import app, mydb, TimelinePost

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mydb.connect(reuse_if_open=True)
        mydb.create_tables([TimelinePost])

    @classmethod
    def tearDownClass(cls):
        mydb.drop_tables([TimelinePost])
        if not mydb.is_closed():
            mydb.close()

    def setUp(self):
        TimelinePost.delete().execute()
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Assol" in html
        assert "Abasova" in html
        assert "Peechz" in html
        # Tests navbar
        assert "/writing" in html