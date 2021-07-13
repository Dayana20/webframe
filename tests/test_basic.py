import unittest, sys

sys.path.append('../webframe') # imports python file from parent directory
from demo import app #imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        print("Here")
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_about_page(self):
        print("Here2")
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_second_page(self):
        print("Here3")
        response = self.app.get('/second_page', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_register(self):
        print("Here4")
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()