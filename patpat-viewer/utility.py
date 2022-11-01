""""""
import json


def group_list(input_list, n):
    g = []
    for i in range(0, len(input_list), n):
        g.append(input_list[i:i + n])
    return g


def get_result_from_file(task=None):
    """Get Patpat search result from patpat_env/result/<task>/result.json

    Args:
        task: uuid

    Returns:
        dict, project metadata
    """
    if task:
        with open(f'patpat_env/result/{task}/result.json') as f:
            data_json = ''.join(f.readlines())
            data_dict = json.loads(data_json)
        f.close()

        return data_dict

    else:
        print('Need to input task uuid.')


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

