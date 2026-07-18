import os
import unittest

os.environ["TESTING"] = "true"

from app import app, mydb, TimelinePost

MODELS = [TimelinePost]


class TestFlaskTimelineApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        mydb.bind(MODELS, bind_refs=False, bind_backrefs=False)
        if mydb.is_closed():
            mydb.connect()
        mydb.drop_tables(MODELS, safe=True)
        mydb.create_tables(MODELS, safe=True)

    def tearDown(self):
        mydb.drop_tables(MODELS, safe=True)
        if not mydb.is_closed():
            mydb.close()

    def test_home_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("<title>", html)

    def test_timeline_page_loads(self):
        response = self.client.get("/timeline")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Timeline", html)

    def test_get_timeline_posts_empty(self):
        response = self.client.get("/api/timeline_post")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertIn("timeline_post", data)
        self.assertEqual(len(data["timeline_post"]), 0)

    def test_post_timeline_post_then_get_it(self):
        post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Liya Test",
                "email": "liya@example.com",
                "content": "Testing timeline post creation",
            },
        )

        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(post_response.is_json)

        created = post_response.get_json()
        self.assertEqual(created["name"], "Liya Test")
        self.assertEqual(created["email"], "liya@example.com")
        self.assertEqual(created["content"], "Testing timeline post creation")

        get_response = self.client.get("/api/timeline_post")
        self.assertEqual(get_response.status_code, 200)

        data = get_response.get_json()
        self.assertEqual(len(data["timeline_post"]), 1)
        self.assertEqual(data["timeline_post"][0]["name"], "Liya Test")
        self.assertEqual(data["timeline_post"][0]["email"], "liya@example.com")
        self.assertEqual(data["timeline_post"][0]["content"], "Testing timeline post creation")

    def test_malformed_timeline_post_requests(self):
        missing_name = self.client.post(
            "/api/timeline_post",
            data={
                "email": "liya@example.com",
                "content": "Missing name",
            },
        )
        self.assertEqual(missing_name.status_code, 400)
        self.assertIn("Invalid name", missing_name.get_data(as_text=True))

        invalid_email = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Liya",
                "email": "not-an-email",
                "content": "Invalid email",
            },
        )
        self.assertEqual(invalid_email.status_code, 400)
        self.assertIn("Invalid email", invalid_email.get_data(as_text=True))

        missing_content = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Liya",
                "email": "liya@example.com",
                "content": "",
            },
        )
        self.assertEqual(missing_content.status_code, 400)
        self.assertIn("Invalid content", missing_content.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
