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
class Paciente:
    _id_counter = 1
    def __init__(self,id:int,nombre,apellido,dni,edad,fecha_de_registro,obra_social) -> None:
        Paciente._id_counter += 1
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__edad = edad
        self.__fecha_de_registro = fecha_de_registro
        self.__obra_social = obra_social

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def dni(self):
        return self.__dni

    @property
    def edad(self):
        return self.__edad

    @property
    def fecha_registro(self):
        return self.__fecha_de_registro

    @property
    def obra_social(self):
        return self.__obra_social
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id=int(data["_Paciente__id"]),
            nombre=data["_Paciente__nombre"],
            apellido=data["_Paciente__apellido"],
            dni=data["_Paciente__dni"],
            edad=data["_Paciente__edad"],
            fecha_de_registro=data["_Paciente__fecha_de_registro"],
            obra_social=data["_Paciente__obra_social"]
        )
    
    def to_dict(self):
        return {
            '_Paciente__id': self.__id,
            '_Paciente__nombre': self.__nombre,
            '_Paciente__apellido': self.__apellido,
            '_Paciente__dni': self.__dni,
            '_Paciente__edad': self.__edad,
            '_Paciente__fecha_de_registro': self.__fecha_de_registro,
            '_Paciente__obra_social': self.__obra_social
        }