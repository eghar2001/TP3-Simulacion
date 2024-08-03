from copy import deepcopy
from typing import List, ClassVar

import numpy.random as random
import matplotlib.pyplot as plt


class Evento:
    _last_id: ClassVar[int] = 0

    def __init__(self, tipo, tiempo):
        self._id = Evento._asignar_id()
        self.tipo = tipo
        self.tiempo = tiempo

    def __str__(self):
        return f"{self.tipo} - {self.tiempo}s"

    def __repr__(self):
        return f"{self._id}-{self.tipo} - {self.tiempo}s"

    def __eq__(self, other):
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)

    @classmethod
    def _asignar_id(cls):
        cls._last_id += 1
        return cls._last_id


def mezclar_listas(lista1: List[Evento], lista2: List[Evento]):
    """Mezcla las listas que le ingresamos, garantizando que hayan mas elementos
    de la lista1 que la lista2 en todo momento"""
    lista1_copy = deepcopy(lista1)

    lista_disponibles = lista1 + lista2
    longitud_lista = len(lista_disponibles)
    lista = []
    cantidad_lista_1 = 0
    cantidad_lista_2 = 0

    for i in range(0, longitud_lista):
        elemento: Evento
        if cantidad_lista_1 > cantidad_lista_2:
            indice_aleatorio = random.randint(0, len(lista_disponibles))
            elemento = lista_disponibles[indice_aleatorio]
            if elemento in lista1:
                cantidad_lista_1 += 1
                lista1_copy.remove(elemento)
            else:
                cantidad_lista_2 += 1
            lista_disponibles.remove(elemento)
        else:
            indice_aleatorio = random.randint(0, len(lista1_copy))
            elemento = lista1_copy[indice_aleatorio]
            lista1_copy.remove(elemento)
            lista_disponibles.remove(elemento)
            cantidad_lista_1 += 1
        lista.append(elemento)

    # Regresarla
    return lista



arribos = random.exponential(size=5, scale=1)
arribos = [Evento('A', tiempo_arribo) for tiempo_arribo in arribos]

servicios = random.exponential(size=5, scale=1)
servicios = [Evento('S', tiempo_servicio) for tiempo_servicio in servicios]

eventos = mezclar_listas(arribos, servicios)

evento1 = Evento('A', 3)
evento2 = Evento('S', 2)

print(eventos)

tipos = [evento.tipo for evento in eventos]

tiempos_entre_intervalos = [evento.tiempo for evento in eventos]

clientes_en_cola = 0
server_ocupado = False

tiempo_actual = 0
tiempos: List = [0]
valores: List = []
intervalos_server_ocupado = []


acumulador_cola = 0
acumulador_server = 0
for (i,evento) in enumerate(eventos):
    acumulador_server += server_ocupado * evento.tiempo
    acumulador_cola += clientes_en_cola * evento.tiempo

    valores.append(clientes_en_cola)
    intervalos_server_ocupado.append(server_ocupado)
    print(server_ocupado)
    tiempo_actual += evento.tiempo
    if evento.tipo == "A":
        if server_ocupado:
            clientes_en_cola += 1
        else:
            server_ocupado = True
    elif evento.tipo == "S":
        if  clientes_en_cola == 0:
            server_ocupado = False
        else:
            clientes_en_cola -= 1

    tiempos.append(tiempo_actual)




    print(acumulador_server)

print(tiempos)
print(valores)

promedio_clientes_en_cola = acumulador_cola / tiempo_actual
utilizacion_server = acumulador_server / tiempo_actual
print(f"{promedio_clientes_en_cola=}")
print(f"{utilizacion_server=}")

#Muestro la cola a lo largo del tiempo

plt.stairs(valores, tiempos, label="Clientes en cola")
plt.stairs(intervalos_server_ocupado, tiempos, label="Uso del servidor")
plt.legend()
plt.title("Uso servidor y clientes en cola a lo largo del tiempo")
plt.show()
