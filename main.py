#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:51:20 2020

@author: camilo
"""

import pyodbc
from flask import Flask, request
import json
import bcrypt


#=================================================================
#       Conexión a la BD - query estudiantes/administrativos
#=================================================================

def get_connection():
    server = 'localhost' 
    database = 'CTIC_Service' 
    username = 'user' 
    password = 'FooF9853' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor, cnxn


def get_data_estudiante(usuario):
    cursor = get_connection()
    cursor = cursor[0]
    query = """SELECT * FROM CTIC_Service.dbo.estudiantes WHERE Usuario = ? """
    return cursor.execute(query, [str(usuario)])


def get_data_administrativo(identificacion):
    cursor = get_connection()
    cursor = cursor[0]
    query = """SELECT * FROM CTIC_Service.dbo.administrativos WHERE Identificacion = ? """
    return cursor.execute(query, [str(identificacion)])




app = Flask(__name__)



#=================================================================
#                       Get estudiante
#=================================================================

@app.route('/estudiante/<string:usuario>', methods=['GET'])
def get_estudiantes(usuario):
    
    # Creamos una lista vacía para almacenar los datos
    lis = []
    
    # llamamos a la función y le pasamos el usuario enviado desde la url
    dat = get_data_estudiante(usuario)
    
    # Recorremos el cursor que retorna la función y lo agregamos a la lista
    for row in dat:
        lis.append(row)
    
    # Comprobamos que la lista no esté vacía
    if (len(lis) == 1):

        # Creamos un diccionario que almacenará los datos con su llave, accediendo a la lisya
        datos = {
                     "codigo":lis[0][0],
                     "identificacion":lis[0][1],
                     "nombres": lis[0][2],
                     "apellidos":lis[0][3],
                     "correo":lis[0][4],
                     "telefono": lis[0][5],
                     "programa": lis[0][6],
                     "creditos_aprobados": lis[0][7],
                     "modGrado":lis[0][8],
                     "imagen":lis[0][9],
                     "usuario":lis[0][10],
                     "contraseña":lis[0][11],
                     "rol":lis[0][12] 
                     
                 }
        
        # Convertimos el diccionario en json
        datos = json.dumps(datos)
        print(type(datos))
    
        # Retornamos el json
        return datos
    
    # Si la lista está vacía, retornamos un 0
    else:
        return "0"

""" El proceso para el administrativo, es el mismo del anterior, sólo que en este 
    vamos a pasar la identificación enviada desde la url a al query  """

#=================================================================
#                       Get administrativo
#=================================================================

@app.route('/administrativo/<string:identificacion>', methods=['GET'])
def get_administrativo(identificacion):

    id = str(identificacion)
    
    lis = []
    
    dat = get_data_administrativo(id)
    
    for row in dat:
        lis.append(row)
    
    if (len(lis) == 1):
        datos = {
                     "identificacion":lis[0][0],
                     "nombres": lis[0][1],
                     "apellidos":lis[0][2],
                     "correo":lis[0][3],
                     "telefono": lis[0][4],
                     "programa": lis[0][5],
                     "imagen":lis[0][6],
                     "usuario":lis[0][7],
                     "contraseña":lis[0][8],
                     "rol":lis[0][9] 
                     
                 }
        
        datos = json.dumps(datos)
        print(type(datos))
    
        return datos
    
    else:
        return "0"



#~~~~~~~~~~~~~~~~ Esta parte se hizo para insertar los datos (No se utiliza para el servicio) ~~~~~~~~~~~~~~


#=================================================================
#                       Post estudiante
#=================================================================
@app.route('/estudiante', methods=['POST'])
def post_estudiantes():
    
    codigo = str(request.form['codigo'])
    identificacion = str(request.form['identificacion'])
    nombres = str(request.form['nombres'])
    apellidos = str(request.form['apellidos'])
    
    telefono = str(request.form['telefono'])
    programa = str(request.form['programa'])
    creditos_aprobados = int(request.form['creditos_aprobados'])
    
    modGrado = request.form['modGrado']
    if modGrado == "":
        modGrado = None
    else: 
        modGrado = float(modGrado)
        
    
    imagen = None
    
    usuario = str('u'+ codigo)
    correo = usuario + '@usco.edu.co'
    
    contrasena = str(request.form['contrasena'])
    salt = bcrypt.gensalt(10)
    contrasena = bcrypt.hashpw(contrasena.encode(), salt)
    
    rol = str(request.form['rol'])
    

    
    conn = get_connection()
    
    cursor = conn[0]
    data = (codigo,identificacion,nombres,apellidos,correo,telefono,programa,creditos_aprobados,
     modGrado,imagen,usuario,contrasena,rol)
    
    sql = """INSERT INTO CTIC_Service.dbo.estudiantes (Codigo,Identificacion,Nombres,Apellidos,Correo,
        Telefono,Programa,CreditosAprobados,ModGrado,Imagen,Usuario,Contraseña,Rol)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    
    cursor.execute(sql, data)
    
    cnxn = conn[1]
    cnxn.commit()
    
    
    return "Ok"


#=================================================================
#                     Post administrativo
#=================================================================

@app.route('/administrativo', methods=['POST'])
def post_admins():
    
    id = str(request.form['id'])
    
    nom = str(request.form['nom'])
    
    ape = str(request.form['ape'])
    
    corr = str(request.form['corr'])
    
    tel = str(request.form['tel'])
    
    pro = str(request.form['pro'])

    img = None
    
    usu = id
    
    contra = str(request.form['contra'])
    salt = bcrypt.gensalt(10)
    contra = bcrypt.hashpw(contra.encode(), salt)
    
    role = str(request.form['role'])
    

    
    conn = get_connection()
    
    cursor = conn[0]
    data = (id,nom,ape,corr,tel,pro,img,usu,contra,role)
    
    sql = """INSERT INTO CTIC_Service.dbo.administrativos (Identificacion,Nombres,Apellidos,Correo,
        Telefono,Programa,Imagen,Usuario,Contraseña,Rol)
    VALUES (?,?,?,?,?,?,?,?,?,?)"""
    
    cursor.execute(sql, data)
    
    cnxn = conn[1]
    cnxn.commit()
    
    
    return "Ok"



if __name__ == '__main__' :
    app.run(debug=True)
