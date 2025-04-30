# MIT License
#
# Copyright (c) 2024 [UTN FRA](https://fra.utn.edu.ar/) All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from datetime import datetime
import re
def convertir_a_datetime(fecha_str):
    return datetime.strptime(fecha_str, '%d/%m/%Y')


def validar_nombre_apellido(nombre)->str:
    '''valida que no tenga espaci'''
    return re.match(r"^[a-zA-Z\s]+$", nombre) and len(nombre) <= 30

def validar_apellido(apellido):
    return re.match(r"^[a-zA-Z\s]+$", apellido) and len(apellido) <= 30

def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

def validar_edad(edad):
    return edad.isdigit() and 18 <= int(edad) <= 90

def validar_obra_social(edad, obra_social):
    opciones_validas = ["swiss medical", "apres", "pami", "particular"]
    obra_social = obra_social.lower()  # Convertir a minúsculas
    
    if int(edad) >= 60:
        return obra_social == "pami"
    else:
        return obra_social in map(str.lower, opciones_validas) and obra_social != "pami"
    
def validar_fecha(fecha):
    try:
        dia, mes, año = map(int, fecha.split('/'))
                        
        if año < 2024 and año >2100 :
            return False
        if mes < 1 or mes > 12:
            return False
        if dia < 1:
            return False
        
        # Verificar el número de días en febrero (considerando años bisiestos)
        if mes == 2:
            if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
                if dia > 29:
                    return False
            elif dia > 28:
                return False
        # Verificar el número de días en otros meses
        elif mes in [4, 6, 9, 11]:
            if dia > 30:
                return False
        else:
            if dia > 31:
                return False
        
        return True
    except ValueError:
        
        return False   