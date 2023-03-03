"""test

    Typical usage example:
    典型用法示例：


Copyright 2022 Liao Weiheng

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import time
import re

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

import utility


def create_app(name=__name__):
    flask = Flask(name)
    Bootstrap5(flask)

    return flask


patpat_viewer = create_app()


@patpat_viewer.route('/')
def home():
    return render_template('Home.html')


"""
@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        q = hub.QueryHub()
        protein_id = identifier
        q.identifier = protein_id
        q.simple_query()

        return redirect(url_for('taskbar'), code=301)
        # redirect(url_for('search_loading', identifier=identifier), code=301)

    return render_template('Search.html')
"""


@patpat_viewer.route('/taskbar', methods=['GET', 'POST'])
def taskbar():
    try:
        with open('../patpat_env/logs/tasks.json', mode='r') as f:
            configs = json.loads(f.readline())
        f.close()
    except FileNotFoundError:
        with open('../patpat_env/logs/tasks.json', mode='w') as f:
            pass
        f.close()

    pagination_num_per = 20

    configs = [i for i in configs['tasks'].values() if i.get('startTime')]
    configs.sort(reverse=True, key=lambda x: x['startTime'])
    for n, task_config in enumerate(configs):
        task_config['startTime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(task_config['startTime']))
        if task_config['state'] == 'Running':
            task_config['state'] = 'Error'
        task_config['entry'] = f'Task-{n}'

    configs_group = utility.group_list(configs, pagination_num_per)
    pagination_num = range(1, len(configs_group) + 1)

    if re.search("(?<=\\?p).*", request.url):
        page = int(re.search("(?<=\\?p).*", request.url).group())
    else:
        page = 1

    this_page_configs = configs_group[page - 1]

    return render_template('Taskbar.html',
                           configs=this_page_configs,
                           pagination_num=pagination_num,
                           page=page)


@patpat_viewer.route('/taskbar/<uuid>', methods=['GET'])
def task(uuid=None):
    data = []
    with open(f'patpat_env/result/{uuid}/result.tab', mode='r', errors='ignore') as f:
        f.readline()
        while True:
            d = f.readline()
            if d:
                data.append(re.split('\t', d))
            else:
                break

    pagination_num_per = 20
    group = utility.group_list(data, pagination_num_per)
    pagination_num = range(1, len(group) + 1)

    if re.search("(?<=\\?p).*", request.url):
        page = int(re.search("(?<=\\?p).*", request.url).group())
    else:
        page = 1

    this_page_data = group[page - 1]

    return render_template('test.html',
                           uuid=uuid,
                           data=this_page_data,
                           pagination_num=pagination_num,
                           page=page)


@patpat_viewer.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@patpat_viewer.route('/about')
def about():
    return render_template('About.html')


@patpat_viewer.route('/contact')
def contact():
    return render_template('Contact.html')


@patpat_viewer.route('/test')
def test():
    return render_template('test.html')


@patpat_viewer.route('/test2')
def test2():
    return render_template('test2.html')


if __name__ == '__main__':
    patpat_viewer.run(debug=True)
