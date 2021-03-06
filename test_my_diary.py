import unittest
import json
from my_class import ExternalFunctions

from my_diary_data_structures import register, login, home, entries, logout, delete_entry,\
 view_entry, create_entry, diary_entries, modify_entry, view_entry, user_details, app
#from flask import *
from my_class import ExternalFunctions
class Test_ExternalFunctions(unittest.TestCase):
    def test_home(self):
        test = app.test_client()
        response = test.get('/api/v1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test.post('/api/v1', json={}).status_code, 405)
    def test_password_verify(self):
        self.assertTrue(ExternalFunctions.password_verify("kevin", "kevin"), True)
        self.assertFalse(ExternalFunctions.password_verify("kevin", "kevins"), False)
    def test_register(self):
        t = app.test_client()
        response = t.get('/api/v1/register')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(t.post('/api/v1/register', json={\
            "fname":"kevin", "lname":"koech", "email":"kkkoech@gmail.com", \
        "username":"kibitok", "password":"1234", "cpassword":\
        "1234"}).status_code, 200)
        self.assertEqual(app.test_client().post('/api/v1/register', json={\
            "fname":"kkibitok", "lname":"kevin", "email":"kk@gmail.com", \
        "username":"kibitok", "password":"12345", "cpassword":\
        "12345"}).status_code, 409)        
        self.assertEqual(t.post('/api/v1/registers', json={}).status_code, 404)        
    def test_login(self):
        user_details.update({"kibitok":{"name":"kevin koech", "email":"kkkoech@gmail.com", "password":"1234"}})
        tester = app.test_client()
        response = tester.get('/api/v1/login')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(tester.post('/api/v1/login', json={\
        "username":"kibitok", "password":"1234"}).status_code, 200)
        self.assertEqual(tester.post('/api/v1/login', json={\
        "username":"kibitok", "password":"12345"}).status_code, 401)
        del user_details["kibitok"]
            
    def test_entries(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/entries')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(tester.post('/api/v1/entries', json={}).status_code, 405)
            self.assertEqual(tester.get('/api/v1/entry').status_code, 404)
            
    def test_logout(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/logout')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(tester.post('/api/v1/entries', json={}).status_code, 405)
    def test_delete_entry(self):
        response = app.test_client().get('/api/v1/delete_entry/3')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(app.test_client().post('/api/v1/delete_entry/3', json={}).status_code, 405)
    def test_create_entry(self):
        test = app.test_client()
        response = test.get('/api/v1/create_entry')
        self.assertEqual(response.status_code, 405)
        r = test.post('/api/v1/create_entry', json={"comment":"me"})
        self.assertEqual(test.get('/api/v1/create_entry').status_code, 405)
        self.assertEqual(r.status_code, 401)
    def test_modify_entry(self):
        with app.test_client() as tester:
            response = tester.get('/api/v1/modify_entry/1')
            self.assertEqual(response.status_code, 405)
            self.assertEqual(tester.get('/api/v1/modify_entr/').status_code, 404)
    def test_view_entry(self):
        tester = app.test_client()
        response = tester.get('/api/v1/view_entry/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(app.test_client().post('/api/v1/view_entry/1', json={}).status_code, 405)
if __name__ == '__main__':
    unittest.main()      
     