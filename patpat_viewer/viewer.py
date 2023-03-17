"""Patpat-viewer APP Views
    This APP Power by Flask
"""
import re

from flask import render_template, request, redirect, url_for

from patpat_viewer import finisher
from patpat_viewer import utility

from patpat_viewer import app


@app.route('/', methods=['GET'])
def home(env_=None):
    return render_template('Home.html')


@app.route('/tasktable/', methods=['GET'])
def tasktable(pagination_num_per=10):
    configs = utility.config_process()

    pagination_num_per = pagination_num_per

    if configs is None:
        configs = "TaskTable is empty."
        return redirect(url_for('empty', configs=configs))

    configs_group = utility.group_list(configs, pagination_num_per)

    this_page_data, pagination_num, page = choose_page(groups=configs_group)
    return render_template('TaskTable.html',
                           configs=this_page_data,
                           pagination_num=pagination_num,
                           page=page)


@app.route('/tasktable/<uid>', methods=['GET', 'POST'])
def task(
        uid,
        condition=None,
        pagination_num_per=10):
    """

    Args:
        uid:
        condition:
        pagination_num_per:

    Returns:

    """
    uid = uid

    if request.method == 'POST':
        condition = request.form['condition']
        pagination_num_per = request.form['pagination_num_per']

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

    acc_sorted = finisher.SortFinisher(
        datasets=data_imported,
        accession=acc_filtered,
        mode='submit',
        key='previously').run()

    data_sorted = [data_imported[acc] for acc in acc_sorted]

    pagination_num_per = pagination_num_per
    data_group = finisher.PaginateFinisher(
        data=data_sorted,
        run_per_page=pagination_num_per).run()

    if data_group:
        this_page_data, pagination_num, page = choose_page(groups=data_group)
        return render_template('Task.html',
                               uid=uid,
                               datasets=this_page_data,
                               pagination_num=pagination_num,
                               page=page)
    else:
        configs = "This task is empty."
        return redirect(url_for('empty', configs=configs))


@app.route('/tasktable/<uid>/<accession>')
def dataset_page(uid, accession):
    uid = uid
    data_imported = finisher.ImportFinisher(uid).run()
    dataset = data_imported[accession]
    return render_template('Dataset.html', dataset=dataset)


@app.route('/contact')
def contact():
    return render_template('Contact.html')


@app.route('/empty/<configs>')
def empty(configs):
    return render_template('Empty.html', configs=configs)


@app.errorhandler(404)
def page_not_found(*args):
    return render_template('404.html'), 404


@app.route('/test')
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



