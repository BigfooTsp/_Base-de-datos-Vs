################################################################################
#		Base de Datos                        								   #
# 		Python 3.7		                                                       #
#       8 Agosto 2018    													   #
################################################################################

import pickle
import os
from collections import namedtuple
from dataclasses import dataclass, field
import copy

VEvent = []

''' TAREAS:
	[ ] La clase BDD_Base tiene que ser superclase de las bases de datos
		futuras. Debe de tener los métodos básicos para CRUD y los
		diferentes campos (subclases de BDD_Field) se añadirán en la
		clase BDD final.

	[ ] La clase BDD_Operator debe de crear, cargar y borrar los
		archivos de base de datos y gestionar los eventos virtuales
		creados por cambios en otros campos que influyen en otros campos.

	[ ] La clase BDD_Field deberá de ser sublase de los diferentes módulos
		que crearán en campo. Debe de tener los métodos de crear, editar y 
		borrar los diferentes objetos que tendrá ese campo así como de listar 
		los comandos que gestionarán esos objetos y que asumirá finalmente 
		el gestor de eventos virtuales de la clase operadora.

	[ ] La incorporación de los comandos surge por la necesidad de obtener 
		una respuesta a cada acción para ver si genera un evento virtual y 
		para gestionar estos eventos virtuales cada vez que se realiza un
		cambio. Eventos virtuales son para relacionar los diferentes campos
		de la base de datos cuando se necesita que un cambio en uno de ellos 
		afecte a otros.

	[ ] Para los comandos hay que crear una clase comando y otrs comandos 
		que recogerá los comandos específicos de cada objeto. 
	'''


################################################################################
#		                  Clase Campo de Base de Datos                         #
################################################################################

class Field_element:
	'''clase padre de BDD_field que contendrá los atributos y métodos propios
	que serán gestionados por comandos especificados en esta clase y que se
	gestionqarán desde la clase operadora.'''
	def __init__(self, name:str, **kwargs):
		self.name = name

	def command(self, command:str) -> True or VEvent:
		'''lista de comandos esepcíficos para el tipo de objeto'''


class BDD_Field:
	''' Diccionario que representa un campo y que contendrá parejas 
	{identificador : objeto}. Heredará el tipo de objeto que formarán
	sus elementos y los métodos propios de este se añadirán a los comandos de
	la clase operadora.'''

	def __init__(self, name:str, obj_class):
		self.name = name
		self.obj = obj_class 	# La clase del objeto que se añadirá al campo
		self.element = {} 	# element = {'Name':None, 'Object':None}

	def create_element(self, **kwargs):
		'''Añade un elemento al campo.'''
		self.element[kwargs['name']] = self.obj(**kwargs)
		return True

	def read_element(self, element_name:str) -> True:
		'''Devuelve una copia de un elemento específico.'''
		return copy.deepcopy(self.element[element_name])

	def update_element(self, element:Field_element) -> True:
		'''Acutaliza un elemento.'''
		self.element[element.name] = element
		return True

	def delete_element(self, element_name:str) -> True:
		'''Elimina un elemento.'''
		del self.element[element_name]
		return True

	def command(self, command:str, *arg, **kwargs):
		'''Gestióna comandos del campo.'''
		if command.startswith('create_element'):
			self.create_element(*arg, **kwargs)
		elif command.startswith('read_element'):
			self.read_element(*arg, **kwargs)
		elif command.startswith('update_element'):
			self.update_element(*arg, **kwargs)
		elif command.startswith('delete_element'):
			self.delete_element(*arg, **kwargs)
		else:
			return 'INCORRECT_COMMAND'


################################################################################
#		                     Clase Base de Datos                              #
################################################################################

class BDD_Base:
	''' Clase base de la base de datos. Se añadirán los diferentes campos al
	diccionario 'campos' que serán todos subclases de BDD_Field '''
	def __init__(self, *args):
		self.fields = {}
		for f in args:
			self.fields[f.name] = f

	def search_element(self, field:str, element_name:str) -> list:
		'''Devuelve lista con las claves que coincidan con una búsqueda.'''
		results = []
		for element in self.fields[field]:
			if element_name in element.key():
				results.append(element.key()) 
			return results
		return 'NO_MATCH'

	def command(self, command:str, *arg, **kwargs):
		'''Gestiona los diferentes comandos sobre los campos'''
		if command.startswith('search_element'):
			self.search_element(*arg, **kwargs)
		else:
			return 'INCORRECT_COMMAND'


################################################################################
#		             Clase operadora de la Base de Datos                       #
################################################################################

class BDD_Operator:
	def __init__(self):
		self.Bdd = None 		# Contiene el objeto Base de datos.
		self.ficheroBBdd = None # Nombre del fichero de la Base de datos.
		self.events = []


	def load_BBdd(self, ficheroBBdd):
		'''Carga o crea una nueva base de datos.'''
		ficheroBBdd += ".pickle"
		with open(ficheroBBdd, 'r+b') as f:
			self.Bdd = pickle.load(f)
			self.ficheroBBdd = ficheroBBdd
			return True


	def save_BBdd(self):
		'''Guarda la base de datos actualizada.'''
		with open(self.ficheroBBdd, 'wb') as f:
			pickle.dump(self.Bdd, f)
			return True


	def create_BBdd(self, BBDD, ficheroBBdd):
		'''Crea una nueva base de datos.'''	
		if not os.path.isfile(ficheroBBdd + ".pickle"):
			self.Bdd = BDD_Base()
			ficheroBBdd += ".pickle"
			self.ficheroBBdd = ficheroBBdd
			if self.save_BBdd():
				return True
		else:
			return 'BDD_YA_EXISTE'


	def delete_BBdd(self, ficheroBBdd):
		'''Borrado de fichero de base de datos.'''
		ficheroBBdd += ".pickle"
		if os.path.isfile(ficheroBBdd):
			os.remove(ficheroBBdd)
			return True
		else:
			return 'ARCHIVO_NO_ENCONTRADO'


	def command(self, command:str, *arg, **kwargs):
		'''Recibe y gestiona el comando.
		Cada campo tiene unos comandos genéricos y desde los elementos que 
		forman cada campo se obtendrán los comandos específicos para 
		ese elemento.
		Cada comando generá una respuesta afirmativa, negativa o genera un 
		evento cirtual que deberá ser gestionado.'''
		if command.startswith('load_BBdd'):
			self.load_BBdd(*arg, **kwargs)
		elif command.startswith('save_BBdd'):
			self.save_BBdd(*arg, **kwargs)
		elif command.startswith('create_BBdd'):
			self.create_BBdd(*arg, **kwargs)
		elif command.startswith('delete_BBdd'):
			self.delete_BBdd(*arg, **kwargs)
		else:
			return 'INCORRECT_COMMAND'


################################################################################
#		                 Funcionando como script.                              #
################################################################################

def mainLoop():
	def help_commands():
		'''Imprime lista de comandos.'''
		print (f''' 
		COMANDOS BÁSICOS:
			load_BBdd
			save_BBdd
			create_BBdd
			delete_BBdd
			search_element
			create_element
			read_element
			update_element
			delete_element
			
		COMANDOS ESPECÍFICOS:
			....''')

	def readCommand(com):
		'''Gestiona un comando recibido.'''
		if com == 'help commands':
			help_commands()

	def gestionaVEvent():
		'''Gestiona eventos surgidos por la manipulación de datos.'''
		None


	with VEvent == []:
		com = input('>>> Escribe comando.> ')
		readCommand(com)
	with len(VEvent) > 0:
		gestionaVEvent()

if __name__ == '__main__':
	mainLoop()