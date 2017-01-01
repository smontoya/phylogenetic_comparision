from flask import request, render_template, Flask
from werkzeug.utils import secure_filename
import subprocess
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))



@app.route('/distancias', methods=['GET', 'POST'])
def analizar():
    command = 'Rscript'
    path2script = 'distancias.R'
    cmd = [command, path2script]
    try:
        x, error = subprocess.check_output(cmd, universal_newlines=True)
    except Exception as e:
        return 'Error al ejecutar R'

    valores = x.split(' ')
    for index in range(len(valores)):
        valores[index] = eval(valores[index])

    return json.dumps(valores)

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
        return "OK"
    elif x == 2:
        return "distinta cantidad de especies"
    else:
        return "misma cantidad pero no mismas especies"



    return json.dumps(valores)




# # run_max.py
# import subprocess

# # Define command and arguments
# command = 'Rscript'
# path2script = 'path/to your script/max.R'

# # Variable number of args in a list
# args = ['11', '3', '9', '42']

# # Build subprocess command
# cmd = [command, path2script] + args

# # check_output will run the command and store to result
# x = subprocess.check_output(cmd, universal_newlines=True)

# print('The maximum of the numbers is:', x)



app.run(debug=True)