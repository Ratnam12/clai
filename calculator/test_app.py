import unittest
import json
import os
import threading
import time
import urllib.request
import urllib.error
from app import HTTPServer, TodoHandler, DATA_FILE

PORT = 8002
BASE_URL = f'http://localhost:{PORT}'

class TodoApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', PORT), TodoHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def setUp(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def _request(self, path, method='GET', data=None):
        url = f'{BASE_URL}{path}'
        headers = {'Content-Type': 'application/json'}
        req_data = json.dumps(data).encode('utf-8') if data is not None else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as response:
                return response.getcode(), json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            try:
                return e.code, json.loads(e.read().decode('utf-8'))
            except:
                return e.code, None

    def test_create_task(self):
        status, data = self._request('/tasks', method='POST', data={'title': 'Test Task'})
        self.assertEqual(status, 201)
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['completed'], False)
        self.assertIn('id', data)

    def test_get_tasks(self):
        self._request('/tasks', method='POST', data={'title': 'Task 1'})
        self._request('/tasks', method='POST', data={'title': 'Task 2'})
        status, data = self._request('/tasks')
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)

    def test_get_task(self):
        status, data = self._request('/tasks', method='POST', data={'title': 'Task 1'})
        task_id = data['id']
        status, data = self._request(f'/tasks/{task_id}')
        self.assertEqual(status, 200)
        self.assertEqual(data['title'], 'Task 1')

    def test_get_task_not_found(self):
        status, data = self._request('/tasks/999')
        self.assertEqual(status, 404)

    def test_update_task(self):
        status, data = self._request('/tasks', method='POST', data={'title': 'Task 1'})
        task_id = data['id']
        status, data = self._request(f'/tasks/{task_id}', method='PUT', data={'title': 'Updated Task', 'completed': True})
        self.assertEqual(status, 200)
        self.assertEqual(data['title'], 'Updated Task')
        self.assertEqual(data['completed'], True)

    def test_delete_task(self):
        status, data = self._request('/tasks', method='POST', data={'title': 'Task 1'})
        task_id = data['id']
        status, data = self._request(f'/tasks/{task_id}', method='DELETE')
        self.assertEqual(status, 200)
        status, data = self._request(f'/tasks/{task_id}')
        self.assertEqual(status, 404)

    def test_create_task_invalid(self):
        status, data = self._request('/tasks', method='POST', data={})
        self.assertEqual(status, 400)
        self.assertEqual(data['error'], 'Title is required')

if __name__ == '__main__':
    unittest.main()
