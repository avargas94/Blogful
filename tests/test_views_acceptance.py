import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"


from blog import app
from blog.database import Base, engine, session, User, Entry


class TestViews(unittest.TestCase):
    def setUp(self):
        self.browser = Browser('phantomjs')

        # Setup Tables
        Base.metadata.create_all(engine)

        # Creates User
        self.user = User(name="Andrew Vargas", email='andrewvargas6933@gmail.com',
                         password=generate_password_hash('test'))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run, kwargs={"port": 8080})

        self.process.start()
        time.sleep(1)

    def tearDown(self):

        self.process.terminate()
        session.close()
        session.close()
        engine.dispose()

        # Removes Table
        Base.metadata.drop_all(engine)

        self.browser.quit()

    def test_login_correct(self):
        self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.fill('email', 'andrewvargas6933@gmail.com')
        self.browser.fill('password', 'test')
        button = self.browser.find_by_css('button[type=submit]')
        button.click()
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")

    def test_login_incorrect(self):
        self.browser.visit("http://0.0.0.0:8080/login")
        self.browser.fill('email', 'andrewvargas6933@gmail.com')
        self.browser.fill('password', 'tesdt')
        button = self.browser.find_by_css('button[type=submit]')
        button.click()
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/login")



if __name__ == "__main__":
    unittest.main()