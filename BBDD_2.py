################################################################################
#		Base de Datos                        								   #
# 		Python 3.7		                                                       #
#       8 Agosto 2018    													   #
################################################################################

import pickle, os, copy
from typing import Dict, Callable, Optional, Any, List, Tuple

################################################################################
#		           Clase para gestión de comandos y eventos                    #
################################################################################

VEvent = []

class CommandsAndEvents:
	'''Clase que constiene todos los comandos y eventos con efectos'''
	global VEvent
	VEvent:       List[str]          = []
	event_dict:   Dict[str:Callable] = {}
	command_list: List[Callable]     = [] 

	@classmethod
	def add_command(cls, func:Callable) -> int:
		'''Añade los comandos que incluye un objeto al ser instanciado.'''
		res = []
		if not func in CommandsAndEvents.command_list:
			CommandsAndEvents.command_list.append(func)
		else:
			res.append(f'El comando {str(func)} ya existe.')
		if len(res) > 0:
			return res
		else:
			return 0


	@classmethod
	def add_event(cls, event:str, func:Callable) -> int:
		res = []
		'''Añade los eventos que incluye un objeto al ser instanciado.'''
		if not func in CommandsAndEvents.event_dict:
			CommandsAndEvents.event_dict.update({event:func})
		else:
			res.append(f'El evento {event} ya existe.')
		if len(res) > 0:
			return res
		else:
			return 0

	def command_help(self, command:Optional[str] = None) -> str:
		'''Ayuda para los comandos. Si no se especifica, entrega lista con 
		todos los comandos.'''
		for c in self.command_list:
			if not command:
				return f'''		AYUDA DE COMANDOS:
				{c.__name__}
				{c.__doc__}
				'''
			elif command:
				if eval(command) in self.command_list:
					i = self.command_list.index(command)
					return self.command_list[i].__doc__
				else:
					return f'Comando {command} no existe.'


	def manageEvents(self) -> int:
		'''Ejecuta los eventos de VEvent.'''
		if len(VEvent) > 0:
			for event in VEvent:
				if event in self.event_dict:
					try:
						self.event_dict[event]
						del event
						return 1
					except Exception as err:
						return f'''Evento {event} no ejecutado. {err}'''


	def manageComands(self, com:str) -> int:
		'''Ejecuta los comandos.'''
		c = com.split(' ', 1)
		command = eval(c[0])
		args = eval(c[1])
		if command in self.command_list:
			i = self.command_list.index(command)
			func = self.command_list[i]
			try:
				func(args)
				return 1
			except Exception as err:
				return f'Comando {str(command)} no ejecutado {err}'
		else:
			return 'Comando no reconocido.'


	def loop(self):
		'''Inicia el bucle que recibe los comandos.'''
		while True:
			com = input('>>> Escriba comando -> ')
			self.manageComands(com)
			self.manageEvents()



################################################################################
#		                  Clase Campo de Base de Datos                         #
################################################################################


class BBDD_Field:
	''' Diccionario que representa un campo y que contendrá parejas 
	{identificador : objeto}. Esto se instanciará con los argumentos 
	[nombre de campo, objeto de campo]'''
	def __init__(self, obj_class:Optional[type] = None):
		# La clase del objeto que se añadirá al campo
		self.obj:     Optional[type] = obj_class
		# Tipo de los elementos del campo = {'Name', type}
		self.element: Dict[str:type] = {}
		# Añadiendo comandos y eventos
		self.addComAndEv()

	############### Introducción de comandos y eventos. #####################
	def addComAndEv(self):
		# newcomand = (func, help)
		basic_commands = ()
		new_commands = ()
		# Nuevo evento = ('Evento', función)
		basic_events = ()
		new_events = ()
		# Añadiendo a lista global de eventos y comandos.
		for com in basic_commands + new_commands:
			CommandsAndEvents.add_command(com)
		for ev in basic_events + new_events:
			CommandsAndEvents.add_event(ev[0], ev[1])


################################################################################
#		                     Clase Base de Datos                              #
################################################################################

class BBDD_Base:
	''' Clase base de la base de datos.
	Se instanciará esta clase con una tupla como argumento que incluirá todos los
	objetos campo que formarán la base de datos. Este objeto debe ser subclase de
	BBDD_Field.'''
	def __init__(self, fields:Optional[Tuple[BBDD_Field]] = None):
		self.fields = []
		for f in fields:
			self.fields.append(f)
		# Añadir los comandos del objeto al modulo.
		self.addComAndEv()
	

	def search_element(self, field:str, search:str) -> List[str]:
		'''Devuelve lista con las claves que coincidan con una búsqueda.'''
		# [] Utilizar expresiones regulares
		results = []
		for element in self.fields[field]:
			if search in element.key():
				results.append(element.key()) 
			return results
		return 'NO_MATCH'


	def create_element(self, field:type, element_name:str, **element_obj:Any) -> int:
		'''Añade un elemento al campo.'''
		if field in self.fields:
			i = self.fields.index(field)
			field = self.fields[i]
			if not element_name in field:
				field.element.update({element_name:field.obj(**element_obj)})
			else:
				return f'El elemento {element_name} ya existe.'
		else:
			return f'El campo {str(field)} no existe.'
		# Evento que provoca
		VEvent.append(f'CREATE ELEMENT ON FIELD {field}')
		return 0


	def read_element(self, field:type, element_name:str) -> Any:
		'''Devuelve una copia de un elemento específico.'''
		if field in self.fields:
			i = self.fields.index(field)
			field = self.fields[i]
			return copy.deepcopy(field.element['element_name'])
		else:
			return 'El elemento {element_name} no existe.'


	def update_element(self, field:str, element_name, element:str) -> int:
		'''Acutaliza un elemento.'''
		self.fields[field].update({element_name:element})
		# Evento que provoca
		VEvent.append(f'UPDATE ELEMENT {element_name} FROM FIELD {field}')
		return 0


	def delete_element(self, field:str, element_name:str) -> int:
		'''Elimina un elemento.'''
		del self.fields[field].element[element_name]
		# Evento que provoca
		VEvent.append(f'DELETE ELEMENT {element_name} FROM FIELD {field}')
		return 0

		
	############### Introducción de comandos y eventos. #####################
	def addComAndEv(self):
		# newcomand = (func, help)
		create_element = self.create_element
		read_element = self.read_element
		update_element = self.update_element,
		delete_element = self.delete_element

		basic_commands = (create_element, read_element, update_element,
								delete_element)
		new_commands = ()
		# Nuevo evento = ('Evento', función)
		basic_events = ()
		new_events = ()
		# Añadiendo a lista global de eventos y comandos.
		for com in basic_commands + new_commands:
			CommandsAndEvents.add_command(com)
		for ev in basic_events + new_events:
			CommandsAndEvents.add_event(ev[0], ev[1])


################################################################################
#		             Clase operadora de la Base de Datos                       #
################################################################################

class BBDD_Operator:
	'''Clase operadora que se encarga de la gestión del archivo de la base de
	datos y los comandos. Esta será la clase que será instanciada para iniciar 
	el trabajo con la base de datos.'''
	def __init__(self):
		# Inicializando Base de datos.
		self.BBdd: BBDD_Base = BBDD_Base()
		# Nombre del fichero de la Base de datos.
		self.ficheroBBdd: str = None
		# Añadir los comaandos del objeto al modulo.
		self.addComAndEv()
		# Inicializando gestor de comandos.
		self.com:  CommandsAndEvents = CommandsAndEvents()


	def load_BBdd(self, ficheroBBdd:str) -> int:
		'''Carga nueva base de datos del tipo actual.
		Argumentos: ficheroBBdd:str -> True'''
		ficheroBBdd += ".pickle"
		if os.path.isfile(ficheroBBdd):
			with open(ficheroBBdd, 'r+b') as f:
				self.BBdd = pickle.load(f)
				self.ficheroBBdd = ficheroBBdd
				return 0
		else:
			return 'El fichero no existe'


	def save_BBdd(self, ficheroBBdd:str = None) -> int:
		'''Guarda la base de datos actualizada.
		Argumentos: ficheroBBdd:str = None -> True'''
		if not ficheroBBdd:
			if self.ficheroBBdd:
				ficheroBBdd = self.ficheroBBdd
			else:
				return 'Introducir nombre de fichero...'
		elif ficheroBBdd:
			ficheroBBdd += ".pickle"
		with open(ficheroBBdd, 'wb') as f:
			pickle.dump(self.BBdd, f)
			return 0


	def delete_BBdd(self, ficheroBBdd:str) -> True:
		'''Borrado de fichero de base de datos.
		Argumentos: ficheroBBdd:str -> True'''
		ficheroBBdd += ".pickle"
		if os.path.isfile(ficheroBBdd):
			os.remove(ficheroBBdd)
			return True
		else:
			return f'Archivo {ficheroBBdd} no encontrado'

	############### Introducción de comandos y eventos. #####################
	def addComAndEv(self):
		# newcomand = (func, help)
		load_BBdd = self.load_BBdd
		save_BBdd = self.save_BBdd
		delete_BBdd = self.delete_BBdd

		basic_commands = (load_BBdd, save_BBdd, delete_BBdd)
		new_commands = ()
		# Nuevo evento = ('Evento', función)
		basic_events = ()
		new_events = ()
		# Añadiendo a lista global de eventos y comandos.
		for com in basic_commands + new_commands:
			CommandsAndEvents.add_command(com)
		for ev in basic_events + new_events:
			CommandsAndEvents.add_event(ev[0], ev[1])


################################################################################
#		                 Funcionando como script.                              #
################################################################################


def mainLoop():
	'''Inicia Operador de la base de datos y se prepara para recibir comandos.'''
	# Inicializa clase operadora que contiene instancia de base de datos
	# e instancia del gestor de comandos.
	op = BBDD_Operator()
	# Inicia bucle desde la instancia de gestor de comandos.
	op.com.loop()


if __name__ == '__main__':
	mainLoop()