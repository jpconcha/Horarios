#coding: utf-8 
########################################################
#             Generacion de Horario                    #
#     UACH, Ingeniería   Miraflores                    #
########################################################  


#pathHORARIOS=os.path.dirname(os.path.abspath('..\\'))
#pathBDMiraflores = os.path.join(os.path.dirname(os.path.abspath('..\\generahoraraio.py')), 'Horarios 1er Sem 2023\\Horarios Miraflores\\HorariosMiraflores.xlsx')
#BDMiraflores=pd.read_excel(pathBDMiraflores,sheet_name='Horario',dtype={'Grupo': str,'Sala': str}) 
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect
from ConsultaBDMiraflores import ConsultaDisponibilidadSalas
import numpy as np

app = Flask(__name__)

app.secret_key = 'clave_secreta'

users = {
    'Usuario': ['usuario1', 'usuario2', 'usuario3','jconcha'],
    'Contraseña': ['contraseña1', 'contraseña2', 'contraseña3','050783'],
    'Correo': ['correo1@example.com', 'correo2@example.com', 'correo3@example.com','juanpabloconcha@gmail.com']
}

dfUsers = pd.DataFrame(users)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ConsultaSalaClases')
def consultaSala():
    return render_template('ConsultaSalaClases.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # Obtener los valores de los campos del formulario
        usuario = request.form.get('txt')
        contraseña = request.form.get('pswd')
        email = request.form.get('email')

        if usuario == None:
            # Buscar el índice de la fila que contiene el correo dado
            indice_fila = dfUsers[dfUsers['Correo'] == email].index

            if len(indice_fila) > 0:
                # Obtener la contraseña correspondiente al correo encontrado
                contraseña_registrada = dfUsers.loc[indice_fila[0], 'Contraseña']
                if contraseña == contraseña_registrada:
                    print("El correo y la contraseña corresponden al mismo registro")
                    return redirect('/')
                else:
                    print("La contraseña no corresponde al correo")
            else:
                print("El correo no se encuentra registrado")    
        else:
            # Agregar un nuevo registro al DataFrame
            
            dfUsers.loc[len(dfUsers)] = [usuario, contraseña, email]
            print(dfUsers)
            #dfUsers = dfUsers.append(nuevo_registro, ignore_index=True)
            print('nuevo registro')
            return redirect('/')
        # Realizar la lógica de verificación de inicio de sesión
        # ...

        
    
    return render_template('login.html')


@app.route('/tabla', methods=['GET'])
def obtener_tabla():
    
    campo1 = request.args.get('campo1')
    campo2 = request.args.get('campo2')

    # Crear el DataFrame con los datos utilizando los valores de campo1 y campo2
    data = {
        'Campo 1': [campo1],
        'Campo 2': [campo2]
    }
    data = ConsultaDisponibilidadSalas(campo1,campo2)

    # Obtener la longitud máxima
    max_length = max(len(lst) for lst in data.values())

    # Ajustar las longitudes de los arrays
    data = {key: lst + [' '] * (max_length - len(lst)) for key, lst in data.items()}


    # Leer el DataFrame desde algún origen de datos
    #data = {
    #'Día': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
    #'Hora de inicio': ['9:00 AM', '10:30 AM', '9:00 AM', '11:00 AM', '10:30 AM'],
    #'Duración': ['1 hora', '1.5 horas', '2 horas', '1.5 horas', '1 hora']
    #}

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data)
    
    #df = df.drop('ONLINE',axis = 1)
    #df = df.drop('DAE', axis = 1)
    #df = df.drop('UAAEP', axis = 1)
    df = df.replace("", None)
    df = df.dropna(axis=1,how='all')
    print(df)
    #df = pd.DataFrame(...)  # Aquí defines tu DataFrame con los datos

    # Convertir el DataFrame en formato JSON
    json_data = df.to_json(orient='records')

    # Retornar los datos como respuesta JSON
    return jsonify(json_data)

if __name__ == '__main__':
    app.run()