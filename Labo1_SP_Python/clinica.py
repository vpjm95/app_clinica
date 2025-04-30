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
import json
from typing import List, Dict, Optional
from paciente import Paciente
from turno import Turno
import library_utn as utn

class Clinica():
    def __init__(self, razon_social: str, especialidades: Dict[str, float], obras_sociales: Dict[str, float]):
        self.__razon_social = razon_social
        self.__lista_pacientes = []
        self.__lista_turnos = []
        self.__especialidades = especialidades
        self.__obras_sociales = obras_sociales
        self.__recaudacion = 0.0
        self._hay_pacientes_sin_atencion = False
        self.__ultimo_id_paciente = 0

    def _generar_nuevo_id_paciente(self):
        self.__ultimo_id_paciente += 1
        return self.__ultimo_id_paciente    
    
    def alta_paciente(self, nombre: str, apellido: str, dni: str, edad: int, fecha_de_registro, obra_social: str):
        if any(paciente.dni == dni for paciente in self.__lista_pacientes):
            print("Error: Ya existe un paciente con ese DNI.")
            return
        nuevo_id = self._generar_nuevo_id_paciente()
        paciente = Paciente(nuevo_id, nombre, apellido, dni, edad, fecha_de_registro, obra_social)
        self.__lista_pacientes.append(paciente)
        self.guardar_pacientes_a_json('pacientes.json')
        print("Paciente registrado exitosamente.")

    def cargar_pacientes_desde_json(self, filename: str):
        try:
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    for paciente_data in data['pacientes']:
                        paciente = Paciente.from_dict(paciente_data)
                        self.__lista_pacientes.append(paciente)
                        self.__ultimo_id_paciente = max(self.__ultimo_id_paciente, paciente.id)
                except json.JSONDecodeError as e:
                    print(f"Error: El archivo {filename} tiene un formato JSON inválido.")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filename}")

    def guardar_pacientes_a_json(self, filename: str):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'pacientes': []}

        # Crear un conjunto de DNIs para verificar duplicados
        dni_set = {paciente['_Paciente__dni'] for paciente in data['pacientes']}

        # Agregar nuevos pacientes si no están en el archivo existente
        for paciente in self.__lista_pacientes:
            paciente_dict = paciente.to_dict()
            if paciente_dict['_Paciente__dni'] not in dni_set:
                data['pacientes'].append(paciente_dict)
                dni_set.add(paciente_dict['_Paciente__dni'])

        with open(filename, 'w') as file:
            json.dump(data, file, default=str, indent=4)

    def alta_turno(self, id_paciente: int, especialidad: str):
        
        paciente = next((p for p in self.__lista_pacientes if p.id == id_paciente), None)
        if not paciente:
            print("Error: No existe un paciente con ese ID.")
            return
        
        especialidad = especialidad.capitalize()
        especialidades_normalizadas = {key.capitalize(): value for key, value in self.__especialidades.items()}
        precio_base = especialidades_normalizadas.get(especialidad)
        if precio_base is None:
            print("Error: No existe esa especialidad.")
            return
        
        obra_social = paciente.obra_social.capitalize()
        obras_sociales_normalizadas = {key.capitalize(): value for key, value in self.__obras_sociales.items()}
        obra_social_descuento_recargo = obras_sociales_normalizadas.get(obra_social, 0)
        
        # Crear el turno y calcular el monto a pagar
        turno = Turno(paciente.id, paciente.nombre, paciente.apellido, paciente.dni, paciente.edad, paciente.fecha_registro, 
                    paciente.obra_social, especialidad, precio_base, obra_social_descuento_recargo)
        
        self.__lista_turnos.append(turno)
        self.guardar_turnos_a_json('turnos.json')
        print("Turno registrado exitosamente.")

    def guardar_turnos_a_json(self, filename: str):
        data = {'turnos': [turno.to_dict() for turno in self.__lista_turnos]}

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, default=str, indent=4)

    def cargar_turnos_desde_json(self, filename: str):
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    for turno_data in data['turnos']:
                        turno = Turno.from_dict(turno_data)
                        self.__lista_turnos.append(turno)
                except json.JSONDecodeError as e:
                    print(f"Error: El archivo {filename} tiene un formato JSON inválido.")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filename}")

    def ordenar_turnos(self, key):
        turnos_dict = [turno.to_dict() for turno in self.__lista_turnos]
        turnos_ordenados = utn.quicksort_ascen(turnos_dict, key)
        turnos_ordenados_objetos = [Turno.from_dict(turno) for turno in turnos_ordenados]
        
        for turno in turnos_ordenados_objetos:
            informacion = (f'{turno.get_id()} | {turno.nombre} | {turno.apellido} | {turno.dni} | '
                        f'{turno.edad} | {turno.fecha_registro} | {turno.obra_social} | '
                        f'{turno.get_especialidad()} | {turno.get_precio_base()} | {turno.get_monto_a_pagar()} | '
                        f'{turno.get_estado_del_turno()}')
            print(informacion)

    def organizar_turnos(self):
        criterio = input("Ordenar por (obra_social/monto_a_pagar): ").strip().lower()
        if criterio == "obra social":
            self.ordenar_turnos("_Paciente__obra_social")
        elif criterio == "monto a pagar":
            self.ordenar_turnos("_Turno__monto_a_pagar")
        else:
            print("Criterio no válido.")   

    def crear_paciente(self):
        ''' (esto es un ejemplo de lo que quiero )informacion de que hace y que retorna '''
        datos_paciente = utn.ingresar_datos() 
        self.alta_paciente(*datos_paciente)        

    def mostrar_pacientes_en_espera(self):
        pacientes_en_espera = [turno for turno in self.__lista_turnos if turno.get_estado_del_turno() == "Activo"]
        for turno in pacientes_en_espera:
            paciente = next((p for p in self.__lista_pacientes if p.id == turno.get_id_paciente()), None)
            if paciente:
                print(f"Paciente: {paciente.nombre} {paciente.apellido}, Turno: {turno.get_especialidad()}")       

    def atender_pacientes(self):
        pacientes_en_espera = [turno for turno in self.__lista_turnos if turno.get_estado_del_turno() == "Activo"]
        if not pacientes_en_espera:
            print("No hay pacientes en espera para atender.")
            return
        
        pacientes_a_atender = pacientes_en_espera[:2]
        
        for turno in pacientes_a_atender:
            turno.finalizar_turno()
        
        self.guardar_turnos_a_json('turnos.json')
        
        print(f"Atención completada para {len(pacientes_a_atender)} paciente(s).")

    def verificar_estados_turnos(self):
        for turno in self.__lista_turnos:
            print(f"Turno ID: {turno.get_id()}, Estado: {turno.get_estado_del_turno()}") 

    def cobrar_atenciones(self):
        for turno in self.__lista_turnos:
            if turno.get_estado_del_turno() == "Finalizado":
                self.__recaudacion += turno.get_monto_a_pagar()
                turno.set_estado_del_turno("Pagado")
        self.guardar_turnos_a_json('turnos.json')
        print(f"Recaudación total: {self.__recaudacion}")    

    def cerrar_caja(self):
        pacientes_pendientes = [turno for turno in self.__lista_turnos if turno.get_estado_del_turno() in ["Activo", "Finalizado"]]
        if pacientes_pendientes:
            print("No se puede cerrar la caja. Aún hay pacientes por atender.")
        else:
            print(f"Total recaudado: {self.__recaudacion}")
            self.guardar_pacientes_a_json('pacientes.json')
            self.guardar_turnos_a_json('turnos.json')
            print("Archivos de pacientes y turnos actualizados.")

    def especialidad_menos_solicitada(self):
        if not self.__lista_turnos:
            print("No hay turnos registrados.")
            return

        especialidad_contador = {}
        for turno in self.__lista_turnos:
            especialidad = turno.get_especialidad()
            if especialidad in especialidad_contador:
                especialidad_contador[especialidad] += 1
            else:
                especialidad_contador[especialidad] = 1

        especialidad_menos_solicitada = min(especialidad_contador, key=especialidad_contador.get)
        print(f"La especialidad menos solicitada es {especialidad_menos_solicitada} con {especialidad_contador[especialidad_menos_solicitada]} solicitudes.")           

    def mostrar_pacientes(self):
        for paciente in self.__lista_pacientes:
            print(f"ID: {paciente.id}|| Nombre: {paciente.nombre}|| Apellido: {paciente.apellido}|| "
                  f"DNI: {paciente.dni}|| Edad: {paciente.edad}|| Fecha de Registro: {paciente.fecha_registro}|| "
                  f"Obra Social: {paciente.obra_social}")
            
    def crear_turno(self):
        self.mostrar_pacientes()
        id_paciente = int(input("ID del paciente: "))
        especialidad = input("Especialidad: ")
        self.alta_turno(id_paciente, especialidad)
