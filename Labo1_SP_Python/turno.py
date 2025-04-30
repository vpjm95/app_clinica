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
from typing import List, Dict, Optional
from paciente import Paciente 
class Turno(Paciente):
    _id_counter = 0  # Contador de IDs autoincremental

    _id_counter = 1

    def __init__(self, id_paciente, nombre, apellido, dni, edad, fecha_de_registro, obra_social, especialidad, precio_base, obra_social_descuento_recargo, monto_a_pagar=None, estado_del_turno="Activo"):
        super().__init__(id_paciente, nombre, apellido, dni, edad, fecha_de_registro, obra_social)
        self.__id = Turno._id_counter
        Turno._id_counter += 1
        self.__especialidad = especialidad
        self.__precio_base = precio_base
        self.__obra_social_descuento_recargo = obra_social_descuento_recargo
        self.__monto_a_pagar = self._calcular_monto(precio_base, obra_social_descuento_recargo)
        self.__estado_del_turno = estado_del_turno
        
        if monto_a_pagar is None:
                self.__monto_a_pagar = self._calcular_monto(precio_base, obra_social_descuento_recargo)
        else:
            self.__monto_a_pagar = monto_a_pagar

            self.__estado_del_turno = estado_del_turno

    def _calcular_monto(self, precio_base, obra_social_descuento_recargo):
        return precio_base + (precio_base * obra_social_descuento_recargo)

    def get_id(self):
        return self.__id

    def get_id_paciente(self):
        return self.id

    def get_especialidad(self):
        return self.__especialidad

    def get_precio_base(self):
        return self.__precio_base

    def get_obra_social_descuento_recargo(self):
        return self.__obra_social_descuento_recargo

    def get_monto_a_pagar(self):
        return self.__monto_a_pagar

    def get_estado_del_turno(self):
        return self.__estado_del_turno

    def set_estado_del_turno(self, nuevo_estado):
        self.__estado_del_turno = nuevo_estado

    def calcular_monto_a_pagar(self):
        base_price = 4000  # Precio base de la atención
        final_discount = self.__obra_social_descuento_recargo

        if self.obra_social == "Swiss Medical":
            final_discount -= 0.40
            if 18 <= self.edad <= 60:
                final_discount -= 0.10
        elif self.obra_social == "Apres":
            final_discount -= 0.25
            if 26 <= self.edad <= 59:
                final_discount -= 0.03
        elif self.obra_social == "PAMI":
            final_discount -= 0.60
            if self.edad >= 80:
                final_discount -= 0.03
        elif self.obra_social == "Particular":
            final_discount += 0.05
            if 40 <= self.edad <= 60:
                final_discount += 0.15

        return base_price * (1 + final_discount)

    def to_dict(self):
        turno_dict = super().to_dict()
        turno_dict.update({
            '_Turno__id': self.__id,
            '_Turno__especialidad': self.__especialidad,
            '_Turno__precio_base': self.__precio_base,
            '_Turno__obra_social_descuento_recargo': self.__obra_social_descuento_recargo,
            '_Turno__monto_a_pagar': self.__monto_a_pagar,
            '_Turno__estado_del_turno': self.__estado_del_turno
        })
        return turno_dict

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_paciente=data['_Paciente__id'],
            nombre=data['_Paciente__nombre'],
            apellido=data['_Paciente__apellido'],
            dni=data['_Paciente__dni'],
            edad=data['_Paciente__edad'],
            fecha_de_registro=data['_Paciente__fecha_de_registro'],
            obra_social=data['_Paciente__obra_social'],
            especialidad=data['_Turno__especialidad'],
            precio_base=data['_Turno__precio_base'],
            obra_social_descuento_recargo=data['_Turno__obra_social_descuento_recargo'],
            estado_del_turno=data['_Turno__estado_del_turno']
        )

    def finalizar_turno(self):
        self.set_estado_del_turno("Finalizado")