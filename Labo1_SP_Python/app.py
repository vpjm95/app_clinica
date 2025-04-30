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

import library_utn as utn
from clinica import Clinica
from paciente import Paciente
from turno import Turno
import json
file_paciente = "./pacientes.json"



def main_app():
    """
    Aplicacion principal del Segundo Parcial de Laboratorio 1
    """
    # Cargar especialidades y obras sociales desde el archivo JSON
    with open('configs.json', 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    especialidades = config_data['especialidades']
    obras_sociales = config_data['obras_sociales']

    clinica = Clinica("UTN-Medical Center", especialidades, obras_sociales)
    clinica.cargar_pacientes_desde_json('pacientes.json')
    clinica.cargar_turnos_desde_json('turnos.json')
    
    while True:
        utn.menu()
        selected_option = int(input("selecione una opcion: "))
        while not selected_option:
            selected_option = int(input(" ¡Error!, selecione una opcion valida: "))

        match selected_option:
            case 1: # Alta paciente
                clinica.crear_paciente()
                
            case 2: # Alta turno
                clinica.crear_turno()
            case 3: # Ordenar turnos
                clinica.organizar_turnos()
            case 4: # Mostrar pacientes en espera
                clinica.mostrar_pacientes_en_espera()
            case 5: # Atender pacientes
                clinica.atender_pacientes()
                clinica.verificar_estados_turnos()
            case 6: # Cobrar atenciones
                clinica.cobrar_atenciones()
            case 7: # Cerrar caja
                clinica.cerrar_caja()
            case 8: # Mostrar informe
                clinica.especialidad_menos_solicitada()
            case 9: # Salir
                break
            case _:
                print('Opción inválida. Por favor, seleccione una opción válida.')
        utn.clear_console()
            