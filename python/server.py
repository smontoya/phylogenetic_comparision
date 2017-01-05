from flask import request, render_template, Flask, url_for
from werkzeug.utils import secure_filename
from os.path import join as joinPath
from Bio import Phylo
import os
import subprocess
import json
import uuid
from shutil import move
app = Flask(__name__)


@app.route('/')
def index():
    dirnames = get_dirs()
    return render_template('index.html', dirnames=dirnames)


@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_file(filename):
    if request.method == 'POST':
        f = request.files['uploadfile']
        filepath = 'uploads/' + secure_filename(filename)
        f.save(filepath)
        tree = Phylo.read(filepath, 'newick')

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/calcular_distancias/<arbol>', methods=['GET', 'POST'])
def calcular_distancias(arbol):
    command = 'Rscript'
    path2script = 'estima_longitud_arbol%s.R' % str(arbol)
    cmd = [command, path2script]
    try:
        x = subprocess.check_output(cmd, universal_newlines=True)
        x = eval(x)
    except Exception as e:
        return "{'error': 'Se ha producido un error al ejecutar R'}"
    if x == 0:
        return "{'ok': 'ok'}"
    else:
        return "{'error': 'La secuencia no corresponde al arbol'}"


@app.route('/distancias', methods=['GET', 'POST'])
def analizar():
    str_uuid = str(uuid.uuid1())
    command = 'Rscript'
    path2script_dist = 'distancias.R'
    path2script_arboles = 'subarboles.R'
    try:
        x = subprocess.check_output([command, path2script_dist],
                                    universal_newlines=True)
    except Exception as e:
        return "{'error': 'Se ha producido un error al ejecutar R'}"

    try:
        subarboles = subprocess.check_output([command, path2script_arboles],
                                             universal_newlines=True)
    except Exception as e:
        print(e)
        return "{'error': 'Se ha producido un error al calcular los subarboles'}"

    x = x.strip().split(';')
    for index in range(len(x)):
        x[index] = x[index].strip().split(' ')
        if len(x[index]) > 1:
            x[index] = {'name': x[index][0], 'value': x[index][1]}
    directory = joinPath('results', str_uuid)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(joinPath(directory, 'statistics.json'), 'w') as outfile:
        json.dump(x, outfile)

    with open(joinPath(directory, 'subarboles.json'), 'w') as outfile:
        outfile.write(subarboles)

    move("uploads/tree1.tree", joinPath(directory, 'tree1.tree'))
    move("uploads/tree2.tree", joinPath(directory, 'tree2.tree'))

    return json.dumps({'ok': url_for('.view', str_uuid=str_uuid)})


def get_dirs():
    return os.listdir('results')

@app.route('/validador', methods=['GET', 'POST'])
def validador():
    command = 'Rscript'
    path2script = 'check_breeds.R'
    cmd = [command, path2script]
    try:
        x = subprocess.check_output(cmd, universal_newlines=True)
    except Exception as e:
        return '{"error":"Error al ejecutar R"}'
    x = int(x)

    # 1 Tienen mismas especies
    # 2 distinta cantidad de especies
    # 3 misma cantidad pero no mismas especies

    if x == 1:
        return '{"ok": "ok"}'
    elif x == 2:
        return '{"error": "Las secuencias tienen distinta cantidad de especies", "id": 2}'
    elif x == 4:
        return '{"error": "El arbol 1 árbol esta sin distancias", "id": 4}'
    elif x == 5:
        return '{"error": "El árbol 2 no posee distancias", "id": 5}'
    elif x == 6:
        return '{"error": "Los árboles no poseen distancias", "id": 6}'
    else:
        return '{"error": "Las especias no coinciden", "id": 2}'


@app.route('/revisar/<str_uuid>', methods=['GET', 'POST'])
def view(str_uuid):
    directory = joinPath('results', str_uuid)
    data = None
    with open(joinPath(directory, 'statistics.json')) as data_file:
        data = json.load(data_file)
    data = data[0:4]
    newick1 = ''
    with open(joinPath(directory, 'tree1.tree')) as data_file:
        newick1 = data_file.read()
    newick2 = ''
    with open(joinPath(directory, 'tree2.tree')) as data_file:
        newick2 = data_file.read()

    subarboles = []
    try:
        with open(joinPath(directory, 'subarboles.json')) as data_file:
            subarboles = json.load(data_file)
    except Exception as e:
        print(e)

    return render_template("revisar.html", statistics=data, newick1=newick1,
                           newick2=newick2, subarboles=subarboles,
                           dirnames=get_dirs())



app.run(debug=True, host='0.0.0.0')