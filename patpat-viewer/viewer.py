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


def group_list(input_list, n):
    g = []
    for i in range(0, len(input_list), n):
        g.append(input_list[i:i + n])
    return g


"""
def get_fake_data():
    with open('logs/tasks.json', mode='r') as f:
        configs = json.loads(f.readline())
        f.close()
    task = '11111111-1111-1111-1111-111111111111'
    config = {
        'identifier': 'TEST_ID',
        'peptides': 10,
        'organism': {'accession': '9606', 'name': 'Homo sapiens'},
        'digestion': {'enzyme': 'trypsin', 'miss': 3, 'min': 7, 'max': 25},
        'proteome_source': '/',
        'description': '>sp|TEST_ID|TEST_PROTEIN test data OS=Homo sapiens OX=9606 GN=testGene PE=1 SV=1',
        'gene': 'testGene',
        'task': task,
        'mappers': ['PRIDE'],
        'state': 'Success',
        'startTime': 1.0
    }
    configs['tasks'][task] = config
    with open('logs/tasks.json', 'w') as fw:
        configs_json = json.dumps(configs)
        fw.write(configs_json)

    protein_ans = ['mzspec:PXD000001:test_file:scan:00001:VLHPLEGAVVIIFK/2']
    peptide_ans = [f'mzspec:PXD00000{i}:test_file:scan:00001:VLHPLEGAVVIIFK/2' for i in range(1, 10)]

    project_base = dict()
    for i in range(1, 10):
        a = retriever.PrideProjectRetriever()
        a.request_word = f"PXD00000{i}"
        a.retrieve()
        if a.response:
            project_base[f"PXD00000{i}"] = a.response

    for project in project_base:
        peptides = [i for i in peptide_ans if utility.usi_split(i).get('collection') == project]
        protein = [i for i in protein_ans if utility.usi_split(i).get('collection') == project]
        project_base[project]['peptides'] = peptides
        project_base[project]['protein'] = protein

    res = {'PRIDE': project_base}

    with open(f'res/{task}.json', 'w') as fw:
        res_json = json.dumps(res)
        fw.write(res_json)

    return res
"""


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

    configs_group = group_list(configs, pagination_num_per)
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
    group = group_list(data, pagination_num_per)
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


if __name__ == '__main__':
    patpat_viewer.run(debug=True)
