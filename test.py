import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Building, Unit

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdTbFVMT0Q1NTNVY0U5ZFNKSWJ0ZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbHR3YWltLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRmOWM4YTU2ZDA2MjAwMTMzNTY0MDQiLCJhdWQiOiJlc3RhdGUiLCJpYXQiOjE1OTM5MjYzMDEsImV4cCI6MTU5MzkzMzUwMSwiYXpwIjoiVmNwVmJmNmR6ZzF2NlFHYm1keTRlRERqTTBDWkIybXIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpidWlsZGluZ3MiLCJnZXQ6YnVpbGRpbmctYnktaWQiLCJwYXRjaDpidWlsZGluZ3MiLCJwb3N0OmJ1aWxkaW5ncyJdfQ.ZCJMU8fBCVLuiMj1qrLdZ1jawNJHLskerOGpHa_MJgqeHuii1vq-XR0oqgjKed6-dZqU1PfQyyJpLa1m5WcxfB4djzVTEOEVc5z0D7acqOpzrKK0K3YAr7gNuSjePNPoypFV47T2DqhraUm80EiaVElQrBZ3NEhhfjVm7gCBUuKDe7xBeWI2ZgzMw0u1tnnNv3y7pxq-yFp9SxG3io8j90M5aLGC7InjsFmpvulf5d3VwIgHVeea8Wwaec_IV45xkUJ9jg6Cga_8famqj2uq8A9IQmwESnvPnWYDGKLZ5MU_LnwDHKroNjOgCJ4EILDalDVQ2hM213nekSFax_51Aw'

class EstateTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI']='postgres://aaltwaim@localhost:5432/estate'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_visitor_get_buildings(self):
        res = self.client.get('/buildings', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_admin_get_buildings(self):
        self.headers.update({'Authorization': 'Bearer '+ token})
        res = self.client.get('/buildings', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_visitor_get_building_by_id(self):
        res = self.client.get('/buildings/2', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_admin_get_building_by_id(self):
        self.headers.update({'Authorization': 'Bearer '+ token})
        res = self.client.get('/buildings/2', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_visitor_add_building(self):
        new_building = {
            "address": "Alyasmin",
            "description": "3 floors building",
            "name": "Tlal",
            "number_of_units": 9,
            "ownerID": 1234567890,
            "building_image": "https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png"
        }
        res = self.client.post('/buildings', json=new_building)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_admin_add_building(self):
        new_building = {
            "address": "Alyasmin",
            "description": "3 floors building",
            "name": "Tlal",
            "number_of_units": 9,
            "ownerID": 1234567890,
            "building_image": "https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png"
        }
        self.headers.update({'Authorization': 'Bearer '+ token})
        res = self.client.post('/buildings', json=new_building, headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_visitor_update_building(self):
        updated_building = {
            "address": "Almraba",
        }
        res = self.client.patch('/buildings/2', json=updated_building)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_admin_update_building(self):
        building = Building(address="Alyasmin", description= "3 floors building", name="Tlal", 
        number_of_units=9, ownerID=1234567890, building_image="https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png")
        building.insert()
        building_id = building.id

        updated_building = {
            "address": "Almraba",
        }
        self.headers.update({'Authorization': 'Bearer '+ token})
        res = self.client.patch(f'/buildings/{building_id}', json=updated_building, headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    
    def test_visitor_delete_building(self):
        res = self.client.delete('/buildings/3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_admin_delete_building(self):
        building = Building(address="Alyasmin", description= "3 floors building", name="Tlal", 
        number_of_units=9, ownerID=1234567890, building_image="https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png")
        building.insert()
        building_id = building.id

        self.headers.update({'Authorization': 'Bearer ' + token})
        res = self.client.delete(f'/buildings/{building_id}', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_visitor_get_units_based_on_building(self):
        res = self.client.get('/buildings/2/units', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_admin_get_units_based_on_building(self):
        self.headers.update({'Authorization': 'Bearer ' + token})
        res = self.client.get('/buildings/2/units', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


    






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()