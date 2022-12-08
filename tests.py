from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post, connect_db

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()


        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        second_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        test_post = Post(
            title="test_post",
            content="this is a test post",
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()


        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.first_name = test_user.first_name
        self.last_name = test_user.last_name

        self.post_id = test_post.id
        self.post_title = test_post.title
        self.post_content = test_post.content

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Cofirms that our users page returns a page with a list of users."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    # when user is clicked, do we get the right user? do we see their posts?
    def test_user_page(self):
        """ Confirms that our individual users page shows the correct user and information"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1>test1_first test1_last</h1>", html)
            # add if we see the user's posts

    # when "add user" is clicked, do you get the add user form?
    def test_add_user_form(self):
        """ Comfirms that our new user page shows the create user page"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1>Create a user</h1>", html)

    # when new user submitted, do they end up in database? do we land on "/users"?
    def test_adding_user(self):
        """" Tests adding a new user and confirms that the input data is on that we are
        redirected back to the users page and that our new user is present."""
        with self.client as c:
            data={
                    'first-name': 'Robot',
                    'last-name': 'McRobot',
                    'img-url': "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/HONDA_ASIMO.jpg/440px-HONDA_ASIMO.jpg"
            }
            resp = c.post("/users/new", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn("Robot McRobot</a>", html)

    # when "edit user" is clicked, do you get the edit user form? do the input fields get filled?
    def test_edit_user(self):
        """ Tests if the edit user route displays the correct page """

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("<h1>Edit a user</h1>", html)

    # when "add post" is clicked, do we get the add post form
    def test_add_post(self):
        """ Tests if the add post route displays the correct page"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(f"<h1>Add Post for {self.first_name} {self.last_name}</h1>", html)

    # when we "edit post" do we get the edit post form? do the input fields get filled?
    def test_edit_post(self):
        """ Tests if the edit post route displays the correct page and properly
        populates the form data """

        with self.client as c:
            resp = c.get(f"/posts/{self.post_id}/edit")
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(f'value="{self.post_title}"', html)
            self.assertIn(f'value="{self.post_content}"', html)

    # when we delete a post does it no longer show on the user page
    def test_delete_post(self):
        """ Tests if a post actually gets deleted when the delete post route
        is accessed """
        breakpoint()
        with self.client as c:
            resp = c.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(f"<h1>{self.first_name} {self.last_name}</h1>", html)
            self.assertNotIn(f"{self.post_title}", html)
