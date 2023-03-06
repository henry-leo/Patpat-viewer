"""

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
import re

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

import finisher
import utility


def create_app(name=__name__):
    flask = Flask(name)
    Bootstrap5(flask)

    return flask


patpat_viewer = create_app()


@patpat_viewer.route('/')
def home():
    return render_template('Home.html')


@patpat_viewer.route('/taskbar', methods=['GET', 'POST'])
def taskbar(pagination_num_per=10):
    configs = utility.config_process()

    pagination_num_per = pagination_num_per

    configs_group = utility.group_list(configs, pagination_num_per)

    this_page_data, pagination_num, page = choose_page(groups=configs_group)
    return render_template('Taskbar.html',
                           configs=this_page_data,
                           pagination_num=pagination_num,
                           page=page)


@patpat_viewer.route('/taskbar/<uid>', methods=['GET'])
def test2(
        uid,
        condition=None,
        pagination_num_per=10):
    # uid = '3d5b4e1d-937c-4661-83a2-b6ed7c19f060'
    uid = uid
    if condition is None:
        condition = {'start': '',
                     'end': '',
                     'databases': [],
                     'keywords': [],
                     }

    data_imported = finisher.ImportFinisher(uid).run()
    condition = condition

    acc_filtered = finisher.FiltrateFinisher(
        datasets=data_imported,
        condition=condition
    ).run()

    data_sorted = finisher.SortFinisher(
        datasets=data_imported,
        accession=acc_filtered,
        mode='submit',
        key='previously').run()

    pagination_num_per = pagination_num_per
    data_group = finisher.PaginateFinisher(
        data=data_sorted,
        run_per_page=pagination_num_per).run()

    if data_group:
        this_page_data, pagination_num, page = choose_page(groups=data_group)
        return render_template('Task.html',
                               uid=uid,
                               dataset=this_page_data,
                               pagination_num=pagination_num,
                               page=page)
    else:
        return render_template('Empty.html')


@patpat_viewer.route('/about')
def about():
    return render_template('About.html')


@patpat_viewer.route('/contact')
def contact():
    return render_template('Contact.html')


@patpat_viewer.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@patpat_viewer.route('/test')
def test():
    return render_template('test.html')


def choose_page(groups):
    pagination_num = range(1, len(groups) + 1)

    if re.search("(?<=\\?p).*", request.url):
        page = int(re.search("(?<=\\?p).*", request.url).group())
    else:
        page = 1

    this_page_data = groups[page - 1]
    return this_page_data, pagination_num, page


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

if __name__ == '__main__':
    patpat_viewer.run(debug=True)
