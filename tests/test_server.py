import os

from patpat_viewer import viewer

# app.config['PATPAT_ENV'] = ''
os.chdir('..')

# Development Mode
viewer.app.run()
"""
# Production Mode
from wsgiref import simple_server
host = '127.0.0.1'
port = 5000
print(f'Running on http://{host}:{port}')
app = simple_server.make_server(host=host, port=port, app=viewer.app)
app.serve_forever()
"""
