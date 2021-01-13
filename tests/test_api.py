import unittest
from base64 import b64encode
import json
import sys

sys.path = ['', '..'] + sys.path[1:]
from project import *


class TestBase(unittest.TestCase):
    app.config['TESTING'] = True

    tester = app.test_client()
    credentials = b64encode(b"ostap@test.com:password").decode('utf-8')


class TestUser(TestBase):
    data = {
        "user_name": "ALexGer",
        "first_name": "ALex",
        "last_name": "Gerbert",
        "email": "ddd@gmail.com",
        "password": "7896",
        "phone": "3809355566",
        "place_id": 1
    }

    # check response 200
    def test_index(self):
        response = self.tester.get('/user/', headers={"Authorization": f"Basic {self.credentials}"})
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_invalid_auth(self):
        credentials = b64encode(b"invalid@test.com:invalid").decode('utf-8')
        response = self.tester.get('/user/', headers={"Authorization": f"Basic {credentials}"})
        statuscode = response.status_code
        self.assertEqual(401, statuscode)

    # user crud
    def test_create_user(self):
        response = self.tester.post("/user", data=json.dumps(self.data), content_type='application/json')

        statuscode = response.status_code

        credentials = b64encode(b"ddd@gmail.com:7896").decode('utf-8')
        self.tester.delete('/user/', headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(200, statuscode)

    def test_create_user(self):
        response = self.tester.post("/user", data=json.dumps({"name": 47}), content_type='application/json')

        statuscode = response.status_code
        self.assertEqual(405, statuscode)

    def test_put_user(self):
        self.tester.post("/user", data=json.dumps(self.data), content_type='application/json')

        credentials = b64encode(b"ddd@gmail.com:7896").decode('utf-8')
        data = {"first_name": "ILoveJava"}
        response = self.tester.put('/user/', data=json.dumps(data),
                                   content_type='application/json',
                                   headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(200, response.status_code)

        self.tester.delete('/user/', headers={"Authorization": f"Basic {credentials}"})

    def test_delete_user(self):
        self.tester.post("/user", data=json.dumps(self.data), content_type='application/json')

        credentials = b64encode(b"ddd@gmail.com:7896").decode('utf-8')

        response = self.tester.delete('/user/', headers={"Authorization": f"Basic {credentials}"})
        self.assertEqual(200, response.status_code)


class TestPlace(TestBase):
    # check response 200
    def test_index(self):
        response = self.tester.get('/place/1')
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_get_places(self):
        response = self.tester.get('/place')
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_put_place(self):
        response = self.tester.put('/place/1', data=json.dumps({"name": "LVIV"}),
                                   content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_wrong_put_place(self):
        response = self.tester.put('/place/47', data=json.dumps({"name": "LVIV"}),
                                   content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(404, statuscode)

    def test_create_place(self):
        response = self.tester.post('/place', data=json.dumps({"name": "Rozvadiv"}),
                                    content_type='application/json')
        statuscode = response.status_code
        self.tester.delete('/place/2', )
        self.assertEqual(200, statuscode)

    def test_create_invalid_place(self):
        response = self.tester.post('/place', data=json.dumps({"name": 47}),
                                    content_type='application/json')
        statuscode = response.status_code
        self.assertEqual(405, statuscode)

    def test_delete_invalid_place(self):
        response = self.tester.delete('/place/47')
        statuscode = response.status_code
        self.assertEqual(404, statuscode)


class TestBoard(TestBase):
    def test_get_global_board(self):
        response = self.tester.get('/board')
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_get_local_board(self):
        response = self.tester.get('/board/place/', headers={"Authorization": f"Basic {self.credentials}"})
        statuscode = response.status_code
        self.assertEqual(200, statuscode)


class TestAdvertisement(TestBase):
    data = {
        "name": "More lollipops 3.0",
        "description": "Want a lollipop!!! 3.0",
        "quantity": 5,
        "status": 1,
        "tag": 2,
        "owner_id": 1
    }

    def test_get_global_advertisement(self):
        response = self.tester.get('/advertisement/1',
                                   headers={"Authorization": f"Basic {self.credentials}"})
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_get_defunct_advertisement(self):
        response = self.tester.get('/advertisement/100',
                                   headers={"Authorization": f"Basic {self.credentials}"})
        statuscode = response.status_code
        self.assertEqual(404, statuscode)

    def test_get_local_advertisement(self):
        response = self.tester.put('/advertisement/1',
                                   data=json.dumps({"name": "Java"}),
                                   content_type='application/json',
                                   headers={"Authorization": f"Basic {self.credentials}"})
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    #
    def test_create_advertisement(self):
        response = self.tester.post('/advertisement',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.credentials}"})

        statuscode = response.status_code

        self.tester.delete('/advertisement/3', headers={"Authorization": f"Basic {self.credentials}"})

        self.assertEqual(200, statuscode)

    def test_post_invalid_advertisement(self):
        data = self.data
        data['owner_id'] = 79
        response = self.tester.post('/advertisement',
                                    data=json.dumps(self.data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.credentials}"})

        statuscode = response.status_code
        self.assertEqual(400, statuscode)

    def test_delete_advertisement(self):
        self.tester.post('/advertisement',
                         data=json.dumps(self.data),
                         content_type='application/json',
                         headers={"Authorization": f"Basic {self.credentials}"})

        response = self.tester.delete(f'/advertisement/{3}', headers={"Authorization": f"Basic {self.credentials}"})

        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_delete_invalid_advertisement(self):
        response = self.tester.delete('/advertisement/100', headers={"Authorization": f"Basic {self.credentials}"})

        statuscode = response.status_code
        self.assertEqual(404, statuscode)


if __name__ == '__main__':
    unittest.main()
