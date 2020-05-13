from app import app, db
import unittest

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_contact(self):
        res = app.test_client(self).get('/contact')
        self.assertEqual(200,res.status_code)

    def test_company(self):
        res = app.test_client(self).get('/company')
        self.assertEqual(200,res.status_code)
    
    def test_mission_vision(self):
        res = app.test_client(self).get('/mission_vision')
        self.assertEqual(200,res.status_code)

    def test_values(self):
        res = app.test_client(self).get('/values')
        self.assertEqual(200,res.status_code)

    def test_dashboard(self):
        res = app.test_client(self).get('/dashboard')
        self.assertEqual(200,res.status_code)

    def test_solicitudes_dashboard(self):
        res = app.test_client(self).get('/solicitudes/dashboard')
        self.assertEqual(200,res.status_code)

    def test_solicitudes_bar_dashboard(self):
        res = app.test_client(self).get('/solicitudesBar/dashboard')
        self.assertEqual(200,res.status_code)

    def test_tiempo_dashboard(self):
        res = app.test_client(self).get('/tiempo/dashboard')
        self.assertEqual(200,res.status_code)

    def test_lineTiempo_dashboard(self):
        res = app.test_client(self).get('/lineTiempo/dashboard')
        self.assertEqual(200,res.status_code)

    def test_flyer_create_get(self):
        res = app.test_client(self).get('/flyer/create')
        self.assertEqual(200,res.status_code)

    def test_redirect_to_login(self):
        res = app.test_client(self).get('/flyer')
        self.assertEqual(302, res.status_code)
        self.assertIn('login', res.location)

    def test_login_get(self):
        res = app.test_client(self).get('/login')
        self.assertEqual(200,res.status_code)

    def test_login_post(self):
        res = app.test_client(self).post('/login')
        self.assertEqual(302, res.status_code)
        self.assertIn('login', res.location)

if __name__ == '__main__':
    unittest.main()