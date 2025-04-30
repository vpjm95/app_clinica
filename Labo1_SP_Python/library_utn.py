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

import os
import validaciones as val



def clear_console():
    """
    The function `clear_console` prompts the user to press Enter to continue and then clears the console
    screen based on the operating system.
    """
    _ = input('\nPresione Enter para continuar...')
    if os in ['nt', 'dos', 'ce']:
        os.system('clear')
    else: os.system('cls')    

def UTN_messenger(message: str, message_type: str = None, new_line: bool = False) -> None:
    """
    This is a Python function that prints a message with a specific color and message type.
    
    :param message: The message that needs to be displayed in the console
    :param message_type: The type of message being passed, which can be 'Error', 'Success', 'Info',
    or None. If None, the message will be printed without any formatting
    """
    _b_red: str = '\033[41m'
    _b_green: str = '\033[42m'
    _b_blue: str = '\033[44m'
    _f_white: str = '\033[37m'
    _no_color: str = '\033[0m'
    message_type = message_type.strip().capitalize()
    new_line_char = '\n'
    final_message = f'{new_line_char if new_line else ""}'
    match message_type:
        case 'Error':
            final_message += f'{_b_red}{_f_white}> Error: {message}{_no_color}'
        case 'Success':
            final_message += f'{_b_green}{_f_white}> Success: {message}{_no_color}'
        case 'Info':
            final_message += f'{_b_blue}{_f_white}> Information: {message}{_no_color}'
        case _:
            final_message += message
    print(final_message)



def quicksort_ascen(lista, key):
    if len(lista) <= 1:
        return lista
    else:
        pivote = lista[0]
        menores = []
        mayores = []
        
        for elemento in lista[1:]:
            valor_pivote = pivote[key]
            valor_elemento = elemento[key]
            
            # Convertir fechas si la clave es "fecha_de_registro"
            if key == "_Paciente__fecha_de_registro":
                valor_pivote = val.convertir_a_datetime(valor_pivote)
                valor_elemento = val.convertir_a_datetime(valor_elemento)
                
            if valor_elemento <= valor_pivote:
                menores.append(elemento) 
            else:
                mayores.append(elemento)

        return quicksort_ascen(menores, key) + [pivote] + quicksort_ascen(mayores, key)

def quicksort_desc(lista:list,key:str):
    if len(lista) <= 1:
        return lista
    else:
        pivote = lista[0]
        menores = []
        mayores = []
        
        for elemento in lista[1:]:
            valor_pivote = pivote[key]
            valor_elemento = elemento[key]
            
            # Convertir fechas si la clave es "fecha_de_registro"
            if key == "_Paciente__fecha_de_registro":
                valor_pivote = val.convertir_a_datetime(valor_pivote)
                valor_elemento = val.convertir_a_datetime(valor_elemento)
                
            if valor_elemento <= valor_pivote:
                menores.append(elemento) 
            else:
                mayores.append(elemento)
    return quicksort_desc(mayores, key) + [pivote] + quicksort_desc(menores, key)

def ingresar_datos():   
    nombre = input("Nombre del paciente: ").strip()
    while not val.validar_nombre_apellido(nombre):
        nombre = input("Error: Ingrese un nombre válido (solo letras y máximo 30 caracteres): ").strip()

    apellido = input("Apellido del paciente: ").strip()
    while not val.validar_nombre_apellido(apellido):
        apellido = input("Error: Ingrese un apellido válido (solo letras y máximo 30 caracteres): ").strip()

    dni = input("DNI del paciente: ").strip()
    while not val.validar_dni(dni):
        dni = input("Error: Ingrese un DNI válido (8 dígitos numéricos): ").strip()

    edad = input("Edad del paciente: ").strip()
    while not val.validar_edad(edad):
        edad = input("Error: Ingrese una edad válida (entre 18 y 90 años): ").strip()

    obra_social = input("Obra Social del paciente: ").strip()
    while not val.validar_obra_social(edad, obra_social):
        obra_social = input("Error: Seleccione una obra social válida según las indicaciones: ").strip()

    fecha_de_registro = input("Fecha de registro (dd/mm/yyyy): ").strip()
    while not val.validar_fecha(fecha_de_registro):
        fecha_de_registro = input("error formato de Fecha invalido (dd/mm/yyyy): ").strip()

    return nombre, apellido, dni, int(edad), fecha_de_registro, obra_social

def menu():
    print("BIENVENIDO A UTN-Medical Center \n1) Alta de Paciente\n2) Alta Turno\n3) Ordenar turnos (Obra social / monto a pagar)\n4) mostrar pacientes en espera\n5) atender pacientes\n6)cobrar atenciones\n7) cerrar caja\n8)informe especialidad menos solicitada\n9) salir. ")


