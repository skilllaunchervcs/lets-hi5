import os
import unittest
from app import app
from flask import Flask,session
from flask_mongoalchemy import MongoAlchemy

class ApplicationTests(unittest.TestCase):
    # setUp and tearDown
    def setUp(self):
        app.config['TESTING']=True
        app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://mlab:mlab123@ds115931.mlab.com:15931/testing'
        self.app = app.test_client()
        db = MongoAlchemy(app)


    def test_signup(self):
        response = self.app.post('/signup',data=dict(email="abc@gmail.com",username="abc",password="12345",repeat_password="12345"),follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def tearDown(self):
        pass
    # Tests

if __name__ == "__main__":
    unittest.main()
