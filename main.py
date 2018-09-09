# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, send_from_directory, request, abort
from db import add_entity, client
from datetime import datetime
from jinja2 import Template
import inspect
import pathlib
from uuid import uuid4

def get_curent_file():
    filename = inspect.getfile(inspect.currentframe())
    return pathlib.Path(filename)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    # generate a random link and for the account.
    access_key = uuid4()
    add_entity(kind='Link', key=str(access_key), visited=False)
    
    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    template_file = this_path.parent / 'templates' / 'index.html'
    
    with template_file.open() as f:
        template = Template(f.read())
    
    return template.render(key=access_key)

@app.route('/regalos')
def regalos():
    access_key = request.args.get('key')
    query = client.query(kind='Link')
    query.add_filter('key', '=', access_key)
    key = list(query.fetch())

    if not key:
        abort(404)

    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    template_file = this_path.parent / 'templates' / 'regalos.html'

    with template_file.open() as f:
        template = Template(f.read())

@app.route('/js/<path:path>')
def serve_js(path):
    """Serve Javascript static files"""
    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    js_folder = this_path.parent / 'js'
    return send_from_directory(str(js_folder), path)


@app.route('/css/<path:path>')
def serve_css(path):
    """Serve Javascript static files"""
    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    css_folder = this_path.parent / 'css'
    return send_from_directory(str(css_folder), path)


@app.route('/images/<path:path>')
def serve_images(path):
    """Serve Javascript static files"""
    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    images_folder = this_path.parent / 'images'
    return send_from_directory(str(images_folder), path)


@app.route('/lib/<path:path>')
def serve_lib(path):
    """Serve Javascript static files"""
    this_file = inspect.getfile(inspect.currentframe())
    this_path = pathlib.Path(this_file)
    lib_folder = this_path.parent / 'lib'
    return send_from_directory(str(lib_folder), path)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_python37_app]
