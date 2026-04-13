import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

DATA_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

class TodoHandler(BaseHTTPRequestHandler):
    def _send_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _get_path_parts(self):
        parsed_path = urlparse(self.path)
        return parsed_path.path.strip('/').split('/')

    def do_GET(self):
        parts = self._get_path_parts()
        tasks = load_tasks()

        if len(parts) == 1 and parts[0] == 'tasks':
            self._send_response(tasks)
        elif len(parts) == 2 and parts[0] == 'tasks':
            try:
                task_id = int(parts[1])
                task = next((t for t in tasks if t['id'] == task_id), None)
                if task:
                    self._send_response(task)
                else:
                    self._send_response({'error': 'Task not found'}, 404)
            except ValueError:
                self._send_response({'error': 'Invalid ID'}, 400)
        else:
            self._send_response({'error': 'Not Found'}, 404)

    def do_POST(self):
        parts = self._get_path_parts()
        if len(parts) == 1 and parts[0] == 'tasks':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_response({'error': 'Empty body'}, 400)
                return
            
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self._send_response({'error': 'Invalid JSON'}, 400)
                return

            if 'title' not in data:
                self._send_response({'error': 'Title is required'}, 400)
                return

            tasks = load_tasks()
            new_id = max([t['id'] for t in tasks], default=0) + 1
            new_task = {
                'id': new_id,
                'title': data['title'],
                'completed': data.get('completed', False)
            }
            tasks.append(new_task)
            save_tasks(tasks)
            self._send_response(new_task, 201)
        else:
            self._send_response({'error': 'Not Found'}, 404)

    def do_PUT(self):
        parts = self._get_path_parts()
        if len(parts) == 2 and parts[0] == 'tasks':
            try:
                task_id = int(parts[1])
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self._send_response({'error': 'Empty body'}, 400)
                    return

                put_data = self.rfile.read(content_length)
                try:
                    data = json.loads(put_data)
                except json.JSONDecodeError:
                    self._send_response({'error': 'Invalid JSON'}, 400)
                    return

                tasks = load_tasks()
                task = next((t for t in tasks if t['id'] == task_id), None)
                if not task:
                    self._send_response({'error': 'Task not found'}, 404)
                    return

                task['title'] = data.get('title', task['title'])
                task['completed'] = data.get('completed', task['completed'])
                save_tasks(tasks)
                self._send_response(task)
            except ValueError:
                self._send_response({'error': 'Invalid ID'}, 400)
        else:
            self._send_response({'error': 'Not Found'}, 404)

    def do_DELETE(self):
        parts = self._get_path_parts()
        if len(parts) == 2 and parts[0] == 'tasks':
            try:
                task_id = int(parts[1])
                tasks = load_tasks()
                task = next((t for t in tasks if t['id'] == task_id), None)
                if not task:
                    self._send_response({'error': 'Task not found'}, 404)
                    return

                tasks = [t for t in tasks if t['id'] != task_id]
                save_tasks(tasks)
                self._send_response({'message': 'Task deleted'})
            except ValueError:
                self._send_response({'error': 'Invalid ID'}, 400)
        else:
            self._send_response({'error': 'Not Found'}, 404)

def run(server_class=HTTPServer, handler_class=TodoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
