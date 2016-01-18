import os
import server
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        server.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert '200' in rv.status
        assert bytes('No entries here so far', 'UTF-8') in rv.data


if __name__ == '__main__':
    unittest.main()
