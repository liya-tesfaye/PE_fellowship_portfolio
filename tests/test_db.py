import os
import unittest

os.environ["TESTING"] = "true"

from app import mydb, TimelinePost

MODELS = [TimelinePost]


class TestTimelinePostDatabase(unittest.TestCase):
    def setUp(self):
        mydb.bind(MODELS, bind_refs=False, bind_backrefs=False)
        if mydb.is_closed():
            mydb.connect()
        mydb.drop_tables(MODELS, safe=True)
        mydb.create_tables(MODELS, safe=True)

    def tearDown(self):
        mydb.drop_tables(MODELS, safe=True)
        if not mydb.is_closed():
            mydb.close()

    def test_timeline_posts_can_be_created_and_retrieved(self):
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello from John"
        )

        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello from Jane"
        )

        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))

        self.assertEqual(len(posts), 2)
        self.assertEqual(first_post.name, "John Doe")
        self.assertEqual(second_post.name, "Jane Doe")
        self.assertEqual(posts[0].name, "Jane Doe")
        self.assertEqual(posts[1].name, "John Doe")


if __name__ == "__main__":
    unittest.main()
