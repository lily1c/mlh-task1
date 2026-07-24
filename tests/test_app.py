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
        assert "/writing" in html
        assert "/hobbies" in html
        assert "Home" in html

    def test_timeline_api_empty(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert "timeline_posts" in json_data
        assert isinstance(json_data["timeline_posts"], list)
        assert len(json_data["timeline_posts"]) == 0

    def test_timeline_post_and_retrieve(self):
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 200
        post_data = response.get_json()
        assert post_data["name"] == "John Doe"
        assert post_data["email"] == "john@example.com"
        assert post_data["content"] == "Hello world, I'm John!"
        assert "created_at" in post_data

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert len(json_data["timeline_posts"]) == 1
        saved_post = json_data["timeline_posts"][0]
        assert saved_post["name"] == "John Doe"
        assert saved_post["email"] == "john@example.com"
        assert saved_post["content"] == "Hello world, I'm John!"

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Timeline" in html
        assert "name=\"name\"" in html
        assert "name=\"email\"" in html
        assert "name=\"content\"" in html

    def test_malformed_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

