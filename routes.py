import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
lin = []
filenameRes = ''
cantFilas = 0

UPLOAD_FOLDER = '/home/alomatics/Escritorio/prueba2/flask/sml/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'sml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def evaluador(x):
    i=0 
    e=0
    resp='Ambiente Estatico\tAmbiente Dinamico\n'
    archivo = open("/home/alomatics/Escritorio/prueba2/flask/sml/static/uploads/result.txt","w+")
    while i<(len(x)):
	  if x[i][e].isalpha():
	     if x[i][e] == "let":
	        print "es let"	
	     if x == "if":
	        print "es if"
	     if x[i][e] == "val":
		variable = x[i][e+1]
		if x[i][e+3].isalpha()==False and x[i][e+3] != '(':
		   tipo = 'int'
		   valor = x[i][e+3]
		   resp += variable +':'+ tipo +'\t\t\t'+ variable + '=' + valor +'\n'
                   archivo.write(resp)
	     e=0
	  i+=1
    archivo.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    cantFilas = 0
    lineas = ''
    if request.method == 'POST':
        file = request.files['file']
	path = str(UPLOAD_FOLDER+'/'+file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    archivo = open (path, "r")
	    linea= archivo.readline()
	    while linea != "":
		lin.append(linea.split())
	        linea = archivo.readline()
	    archivo.close()
            cantFilas = len(lin)
	    (evaluador(lin))
	    filenameRes = 'result.txt'
            return redirect(url_for('uploaded_file',filename=filenameRes))
    return render_template('home.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
  app.run(debug=True)
