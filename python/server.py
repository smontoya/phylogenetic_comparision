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
    return render_template('index.html')


@app.route('/upload/<filename>', methods=['GET', 'POST'])
def upload_file(filename):
    if request.method == 'POST':
        f = request.files['uploadfile']
        filepath = 'uploads/' + secure_filename(filename)
        f.save(filepath)
        tree = Phylo.read(filepath, 'newick')

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/distancias', methods=['GET', 'POST'])
def analizar():
    str_uuid = str(uuid.uuid1())
    command = 'Rscript'
    path2script = 'distancias.R'
    cmd = [command, path2script]
    try:
        x = subprocess.check_output(cmd, universal_newlines=True)
    except Exception as e:
        return "{'error': 'Se ha producido un error al ejecutar R'}"

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

    move("uploads/tree1.tree", joinPath(directory, 'tree1.tree'))
    move("uploads/tree2.tree", joinPath(directory, 'tree2.tree'))

    return json.dumps({'ok': url_for('.view', str_uuid=str_uuid)})


@app.route('/validador', methods=['GET', 'POST'])
def validador():
    command = 'Rscript'
    path2script = 'check_breeds.R'
    cmd = [command, path2script]
    try:
        x = subprocess.check_output(cmd, universal_newlines=True)
    except Exception as e:
        return 'Error al ejecutar R'
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
    else:
        return '{"error": "Las especias no coinciden", "id": 2}'


@app.route('/revisar/<str_uuid>', methods=['GET', 'POST'])
def view(str_uuid):
    directory = joinPath('results', str_uuid)
    data = None
    with open(joinPath(directory, 'statistics.json')) as data_file:
        data = json.load(data_file)
    return render_template("revisar.html", statistics=data)



app.run(debug=True, host='0.0.0.0')