###############################################################################
#		Base de Datos                        								  #
# 		Python 3.7		                                                      #
#       8 Agosto 2018                                                         #
###############################################################################

import Base_commands
from dataclasses import dataclass, field, InitVar
import inspect
import copy
import os
import pickle
from typing import Any, Callable, Dict,List, Optional, Tuple, Union

###############################################################################
#		                  Clase Campo de Base de Datos                        #
###############################################################################

@dataclass
class Entity_attribute:
	'''Objeto que forma los atributos de las entidades de la base de datos.'''
	tipo: str
	args: InitVar[Dict] = None # Valor de nuevo objeto o acceso a otro atributo
	primary_key: [str,int] = None # Imprescindible al menos 1
	foraign_key: Any = None # Acceso al atributo de otra entidad
	getCondition: str = 'True'
	getEffects: str = 'None'
	updateCondition: str = 'True'
	updateEffects: str = 'None'
	deleteCondition: str = 'True'
	deleteEffects: str = 'None'

	def __post_init__(self, args):
		self.value = args


	@property
	def value(self):
		if exec(self.getCondition):
			exec(self.getEffects)
			return self._value

	@value.setter
	def value(self, args):
		if exec(self.updateCondition):
			self._value = self.tipo(args)
			exec(self.updateEffects)

	@value.deleter
	def value(self):
		if exec(self.deleteCondition):
			self._value = None
			exec(self.deleteEffects)



class Entity:
	'''Clase padre de entidad de las tablas.Las entidades se crearán mediante 
	factoría para que cumplan ciertas condiciones como la organización de sus 
	atributos dentro de una lista.
	Los diferentes tipos compatibles se definen dentro del módulo Base_tipos'''
	def __init__(self):
		self.atr: Dict = {
			'primary_keys':[],
			'foraign_keys':[],
			'keys':[]
			}


class Table:
	'''Objeto de campo personalizado básico. Para tipos personalizados
	utilizar este, que tiene opción de añadir comandos.'''
	'''Objeto tabla de la base de datos.'''
	def __init__(self):
		self.tipo = None
		self._table_list: List = []
	

	def create_entity(self, attributes_params: List[Dict]) -> int:
		'''Añade una entidad a la tabla. El primer objeto añadido define el 
		tipo de objetos que contiene la tabla y como deben de ser los 
		siguientes'''

		def añade_atributo(entity: Entity, atributo: Entity_attribute) -> Entity:
			'''Añade un atributo al objeto Entity.'''
			if atributo.primary_key == True:
				entity.atr['primary_keys'].append(atributo)
			elif atributo.foraign_key == True:
				entity.atr['foraign_keys'].append(atributo)
			else:
				entity.atr['keys'].append(atributo)
			return Entity				


		def comprueba_entidad(self, entity: Entity) -> bool:
			'''comprueba si el objeto es del mismo tipo de tabla y contiene
			al menos una llave primaria.'''
			# Comprueba que el objeto tenga llaves primarias.
			if len(entity.args['primary_keys']) > 0:
				if self.__comprueba_tipo(entity):
					return True
			return False


		entity = Entity()
		for atr_dict in attributes_params:
			atributo = Entity_attribute(atr_dict)
			entity = añade_atributo(entity, atributo)
		if comprueba_entidad(self, entity):
			self._table_list.append(entity)


	def __comprueba_tipo(self, entity: Entity) -> bool:
		'''Comprueba que un objeto entidad pertence al tipo de la tabla.'''
		# Crea tipo de tabla con el primer objeto
		ls = []
		for atr in entity.atr.values():
			ls.append(atr.tipo, atr.primary_key)
		# Si es el primer objeto, define el tipo.
		if self.tipo == None:
			self.tipo = ls
			return True
		# Comprueba si el objeto es del tipo de la tabla
		elif ls == self.tipo:
			return True
		return False

	
	def __si_existe(self, 
					primary_key: [str, int] = None,
					return_object: bool = None) -> [bool, Entity]:
		'''Comprueba si existe la entidad en la tabla a partir de su llave 
		primaria o el objeto entidad mismo.
		Devuelve True/False o el objeto si se especifica en 'return_object'.'''
		for entity in self._table_list:
			if primary_key in entity.arg['primary_key']:
				if return_object:
					return entity
				else:
					return True
			return False


	def __cambia_atributos(self, entity_pk: [str, int],	new_entity: Entity = None,
							delete: bool = False) -> bool:
		'''Cambia los atributos de un objeto por los de otro. si delete = True
		se cambian todos los atributos a None.'''

		ATRS = ('value', 'foraign_key', 'getCondition', 'getEffects',
				'updateCondition', 'updateEffects', 'deleteCondition',
				'deleteEffects')
		entity = self.__si_existe(entity_pk, return_object=True)

		for new_lst, lst in new_entity.arg.values(), entity.arg.values():
			for new_atr, atr in new_lst, lst:
				# Se modifican los atributos por separado para
				# respetar las condiciones y efectos.
				if new_atr != atr:
					for at in ATRS:
						at = eval(at)
						if delete: # Si se borra el objeto.
							atr.at = None
						else: # Si se actualiza el objeto.
							atr.at = new_atr.at
				return True


	def read_entity(self, entity_pk: [str, int]) -> Entity:
		'''Devuelve una copia de un elemento específico por una de sus 
		llaves primarias.'''
		return copy.deepcopy(self.__si_existe(entity_pk, return_object=True))


	def update_entity(self, new_entity: Entity) -> int:
		'''Acutaliza un elemento.Todas Las llaves primarias no se pueden 
		modificar'''
		pk = new_entity['primary_keys']
		if self.__comprueba_tipo(new_entity) and self.__si_existe(pk):
			self.__cambia_atributos(pk, new_entity)


	def delete_entity(self, primary_key: [str, int]) -> int:
		'''Elimina un elemento.'''
		if self.__si_existe(primary_key):
			self.__cambia_atributos(primary_key, delete=True)
			entity = self.__si_existe(primary_key, return_object=True)
			del entity

################################################################################
#		                     Clase Base de Datos                              #
################################################################################

class Base:
	''' Clase base de la base de datos.
	Se instanciará esta clase con una tupla como argumento que incluirá todos los
	objetos campo que formarán la base de datos. Este objeto debe ser subclase de
	BBDD_Field.'''
	def __init__(self):
		self._table: Dict[str,Table] = {} # Contiene todas las tablas de la base de datos

	
	def add_table(self, nombre):
		'''Añade un campo a la base.'''
		if not nombre in self._table:
			self._table.update({nombre:Table()})
			return True
		return False


	def delete_table(self, nombre):
		'''Borra un campo de la base.'''
		if nombre in self._table:
			del self._table[nombre]
			return True
		return False
	

	def search_entity(self, table: str, search: str) -> List[str]:
		'''Devuelve lista con las claves primarias de las entidades que coincidan 
		con una búsqueda.'''
		# [] Utilizar expresiones regulares
		result = []
		for table in self._table:
			for entity in table._table_list:
				if search in entity.atr.key():
					result = [table, entity.atr.key()]
			return result

		
################################################################################
#		             Clase operadora de la Base de Datos                       #
################################################################################

class Base_Operator:
	'''Clase operadora que se encarga de la gestión del archivo de la base de
	datos y los comandos. Esta será la clase que será instanciada para iniciar 
	el trabajo con la base de datos.'''
	def __init__(self, BBDD: Optional[Base] = Base(), 
				ObjCommand: Optional[Any] = Base_commands.Commands()):
		# Inicializando Base de datos.
		self.BBdd: Base = BBDD
		# Nombre del fichero de la Base de datos.
		self.ficheroBBdd: str = None
		# Inicializando gestor de comandos.


	def load_BBdd(self, ficheroBBdd:str) -> int:
		'''Carga nueva base de datos del tipo actual.
		[ficheroBBdd:str] -> 0'''
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
		[ficheroBBdd:str = None] -> 0'''
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


	def delete_BBdd(self, ficheroBBdd:str) -> int:
		'''Borrado de fichero de base de datos.
		[ficheroBBdd:str] -> 0'''
		ficheroBBdd += ".pickle"
		if os.path.isfile(ficheroBBdd):
			os.remove(ficheroBBdd)
			return 0
		else:
			return f'Archivo {ficheroBBdd} no encontrado'


################################################################################
#		                 Funcionando como script.                              #
################################################################################


def mainLoop():
	'''Inicia Operador de la base de datos y se prepara para recibir comandos.'''
	# Inicializa clase operadora que contiene instancia de base de datos
	# e instancia del gestor de comandos.
	#op = Base_Operator()
	# Inicia bucle desde la instancia de gestor de comandos.
	#op.com.loop()


if __name__ == '__main__':
	mainLoop()
