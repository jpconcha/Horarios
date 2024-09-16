#coding: utf-8 
########################################################
#             Generacion de Horario                    #
#     UACH, Ingeniería   Miraflores                    #
########################################################  

from gurobipy import *
#from gurobipy.gurobipy import quicksum
import os
from django.template.defaultfilters import length
from xlrd import open_workbook
import pandas as pd
import unicodedata
import numpy as np
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import RGBColor,Cm, Inches, Pt
from docx.shared import Mm
from sympy.codegen.cnodes import restrict

# Consideraciones:
#       i) Grupos de cursos armados.
#      ii) Asignacion de cursos a profesores realizados.
#     iii) Asignacion grupos realizada. 

#Tabla Horario
#_____________________________________________________
#     | Lunes | Martes | Miercoles | Jueves | Viernes |
#-----------------------------------------------------
#  1  |   0   |   6    |     12    |   18   |   24    | 
#-----------------------------------------------------
#  2  |   1   |   7    |     13    |   19   |   25    | 
#-----------------------------------------------------
#  3  |   2   |   8    |     14    |   20   |   26    | 
#-----------------------------------------------------
#  4  |   3   |   9    |     15    |   21   |   27    | 
#-----------------------------------------------------
#  5  |   4   |   10   |     16    |   22   |   28    | 
#-----------------------------------------------------
#  6  |   5   |   11   |     17    |   23   |   29    |
#-----------------------------------------------------
def IDdiasperiodos(n,m):
    d={'Lunes':{    'I':0,  'II':1,  'III':2, 'IV':3, 'V':4, 'VI':5,   'Todos':[0,1,2,3,4,5],      'Mañana':[0,1,2],    'Tarde':[3,4,5],    'Almuerzo':3},
       'Martes':{   'I':6,  'II':7,  'III':8, 'IV':9, 'V':10,'VI':11,  'Todos':[6,7,8,9,10,11],    'Mañana':[6,7,8],    'Tarde':[9,10,11],  'Almuerzo':9},
       'Miercoles':{'I':12, 'II':13, 'III':14,'IV':15,'V':16,'VI':17,  'Todos':[12,13,14,15,16,17],'Mañana':[12,13,14], 'Tarde':[15,16,17], 'Almuerzo':15, '-':'NN'},
       'Jueves':{   'I':18, 'II':19, 'III':20,'IV':21,'V':22,'VI':23,  'Todos':[18,19,20,21,22,23],'Mañana':[18,19,20], 'Tarde':[21,22,23], 'Almuerzo':21},
       'Viernes':{  'I':24, 'II':25, 'III':26,'IV':27,'V':28,'VI':29,  'Todos':[24,25,26,27,28,29],'Mañana':[24,25,26], 'Tarde':[27,28,29], 'Almuerzo':27, '-': 'NN' },
       'Semana':{   'I':[0,6,12,18,24],'II':[1,7,13,19,25],'III':[2,8,14,20,26],'IV':[3,9,15,21,27],'V':[4,10,16,22,28],'VI':[5,11,17,23,29],'Mañana':[0,6,12,18,24,1,7,13,19,25,2,8,14,20,26],'Tarde':[3,9,15,21,27,4,10,16,22,28,5,11,17,23,29]},
       '-':{'III': 'NN' , '-': 'NN'  }  
       }
    return d[n][m]
def idSemestre(n):
    d={'I':'S1','II':'S2','III':'S3','IV':'S4'}
    return d[n]

def get_key(my_dict,val): 
    for key, value in my_dict.items(): 
        if val == value: 
            return key 
  
    return "no existe"    
def ConsultaBDHorario():    
    ################# Parametros generales del software ###################
    #######################################################################
    pathHORARIOS=os.path.dirname(os.path.abspath('..\\'))
    pathBDMiraflores = os.path.join(os.path.dirname(os.path.abspath('..\\generahoraraio.py')), 'Horarios 2do Sem 2024\\Horarios Miraflores\\HorariosMiraflores2doSem2024.xlsx')
    #Conjunto de dias de la semana 
    Dias= ['Lunes','Martes','Miercoles','Jueves','Viernes']
    #Periodos de trabajo por dia
    Periods=6
    #Inicio periodo semana
    iniPer=0
    #######################################           Unidades               ##########################################
    ####################################### Parametros ingresados por usuario ######################################### 
    
    print('------------------------------------------------')
    print('--            Sistema Consulta horaria         -')
    print('------------------------------------------------')
    print( )
    print('------------------------------------------------')
    print('    Inicio carga de datos.')
    print('------------------------------------------------')
    
    
    BDMiraflores=pd.read_excel(pathBDMiraflores,sheet_name='Horario',dtype={'Grupo': str,'Sala': str})    
    SalasMiraflores=BDMiraflores['Sala'].drop_duplicates().dropna(axis=0,how='any') 

    os.system('cls')
    print(' ')
    print(' ')
    print('        #################################')
    print('        ### Consulta salas disponibles ##')
    print('        #################################')
    op1='S'
    ingresoCorrectoDia='Correcto'
    ingresoCorrectoPeriodo='Correcto'
    while op1=='S':
        ingresoCorrectoDia='Correcto'
        ingresoCorrectoPeriodo='Correcto'     
        while ingresoCorrectoDia=='Correcto': 
            ConsultaDía=input('Ingrese día: ')
            if not(ConsultaDía== 'Lunes' or ConsultaDía == 'Martes' or ConsultaDía == 'Miércoles' or ConsultaDía == 'Jueves' or ConsultaDía == 'Viernes'):
                os.system('cls')
                print(' ')
                print(' ')
                print('        #################################')
                print('        ### Consulta salas disponibles ##')
                print('        #################################')
                
                print('Debe ingresar: Lunes, Martes, Miércoles, Jueves, Viernes')
                        
            else:            
                ingresoCorrectoDia='Incorrecto'
            os.system('cls')
        print(' ')
        print(' ')
        print('        #################################')
        print('        ### Consulta salas disponibles ##')
        print('        #################################')
                
        print('Ingrese día: '+ConsultaDía)                
        while ingresoCorrectoPeriodo=='Correcto': 
            
            ConsultaPeriodo=input('Ingrese periodo: ')
            if not(ConsultaPeriodo== 'I' or ConsultaPeriodo == 'II' or ConsultaPeriodo == 'III' or ConsultaPeriodo == 'IV' or ConsultaPeriodo == 'V' or ConsultaPeriodo=='VI'):
                os.system('cls')
                print(' ')
                print(' ')
                print('        #################################')
                print('        ### Consulta salas disponibles ##')
                print('        #################################')
                
                print('Ingrese día: '+ConsultaDía)
                print('Debe ingresar: I, II, III, IV, V, VI')
                        
            else:            
                ingresoCorrectoPeriodo='Incorrecto'    
             
        Consulta=BDMiraflores[(BDMiraflores['Dias']==ConsultaDía) & (BDMiraflores['Periodo']==ConsultaPeriodo)]['Sala']
        salasDisponibles={}
        print(' ')
        print('  Lista de salas disponibles (',ConsultaDía,ConsultaPeriodo,')')
        for s in SalasMiraflores:
            if s.upper() not in np.array([palabra.upper() for palabra in Consulta.values]):
                if s=='9202':
                    
                    print('    '+s+' (sala piano)')
                else:
                    capacidad_sala1 = BDMiraflores.loc[BDMiraflores['Sala'] == s, 'Capacidad sala'].iloc[0]    
                    print('    '+s+'    ' + str(capacidad_sala1).rjust(30-len(s)))    
        print(' ')
        print('--------------------------------------------------------')
        op1=input('Desea consultar nuevamente(S/N) o desea agregar una solicitud(I): ')
        if op1=='S' or op1=='s' or op1=='Si' or op1=='si':
            op1='S'
            os.system('cls')
            print(' ')
            print(' ')
            print('        ####################################')
            print('        ###   Consulta salas disponibles  ##')
            print('        ####################################')

            print(' ')

    os.system('cls')

    #######################################################################

if __name__ == '__main__':
    ConsultaBDHorario()

################################### Proceso de asignación horario Miraflores ####################################################

##### 1) Solicitud de requerimiento para institutos horario-profesor-grupo. 
##### 2) Enviar propuesta de horario optimizado, completo a instituto por carrera semestre. 
##### 3) Instituto da visto bueno a propuesta de horario y ahace ingreso de este al sistema. 
##### 4) El cambio de sala-horario la realiza el encargado, por solicitud de instituto. 

#######################################################################################   


