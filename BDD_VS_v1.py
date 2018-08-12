################################################################################
#		Base de Datos de Operarios y servicios 								   #
# 		Python 3.7		                                                       #
#       23 Julio 2018    													   #
################################################################################

from dataclasses import dataclass, field
import pickle
import os
import time
import copy
from collections import namedtuple
import testBDD # Para la realización de los tests.

################################################################################
#		             Objetos que son campos de la Base de Datos                #
################################################################################

class ObjVacaciones:
	''' Se encargará de gestionar las vacaciones pendientes y disfrutadas
	de los operarios así como un historial de ellas'''
	def __init__(self):
		self.disfrutadas = None
		self.pendientes = None
		self.asigandas = None


class ObjDireccion:
	'''Objeto con la dirección y coordenadas y posiblemente métodos 
	para visualización en GMaps.'''
	def __init__(self, direccion = None): 
		self.dirc = direccion
		self.pos = None
		self.map_link = None


class ObjNota:
	'''Objeto básico que contiene una nota.'''
	def __init__(self, text:str, tag:str):
		self.nota={"text":text, "tag":tag, "fecha":time.strftime("%d-%m-%Y  %H:%M ")}

	def __str__(self):
		cad = (
			f'''
			------------------------------------------
			NOTA: 	{self.nota['fecha']}
			------------------------------------------
			TAG:     {self.nota['tag']}
			
			{self.nota["text"]}
			------------------------------------------	
			''')
		return cad


class ObjNotas:
	'''Objeto de control para las notas.'''
	def __init__(self):
		self.notas=[]


	def add_note(self, text:str, tag:str="nota") -> True:
		'''Añade una nueva nota.''' 
		self.notas.append(ObjNota(text, tag))
		return True


	def search_note(self, text:str=None, tag:str=None) -> tuple:
		'''Busca notas por texto o tag. Devuelve tupla con índices de las notas.'''
		ids=[]
		if not text and not tag:
			return False
		for i, n in enumerate(self.notas):
			if n['tag'] == tag or tag == None:
				if text in n['text'] or text == None:
					ids.append(i)
					return tuple(ids)		


	def edit_note(self, nota_id:int, text:str) -> True:
		'''Edita una nota con un nuevo texto.'''
		if len(self.notas) >= nota_id:
			self.notas[nota_id]['text'] = text
			return True
		return 'Índice de nota incorrecto'


	def view_note(self, *args:tuple) -> list:
		'''Devuelve las notas a partir de sus índice. Sin argumentos devuelve todas las notas.'''
		if not args:
			return self.notas
		elif len(self.notas) >= max(args):
			notas = []
			for i in args:
				notas.append(self.notas[i])
			return notas
		return 'Índices de nota incorrecto'


	def del_note(self, nota_id:int) -> True:
		'''Elimina una nota por su índice.'''
		if len(self.notas) >= nota_id:
			del self.notas[nota_id]
			return True
		return 'Índice de nota incorrecto'


class ObjHistorial(ObjNotas):
	'''Objeto que gestiona la antiguedad, las notas y las vacaciones.'''
	def __init__(self):
		super().__init__() #self.notas = []
		self.vacaciones = ObjVacaciones() 	# Vacaciones (objeto que contiene vacaciones y disfrutadas)
		self.antiguedad = None


@dataclass
class ObjServ:
	''' Objeto servicio de vigilancia '''
	nombre: str 
	telf: str = None
	coordinador : str = None
	gerenteB_1 : str = None
	gerenteB_2 : str = None
	_direccion : ObjDireccion = field(default_factory=ObjDireccion)
	vss_asignados : list = None
	historial : ObjHistorial = field(default_factory=ObjHistorial)

	def __post_init__(self):
		# Se da la posibilidad de inicializar vacío el objeto del campo direccion o
		# de que, si se aporta argumento en str instanciando ObjVs, se cree a partir de este.
		if isinstance(self._direccion, str):
			self._direccion=ObjDireccion(self._direccion)


	def __str__(self):
		cad = (
			f'''
		------------------------------------------
		SERVICIO:   {self.nombre}
		------------------------------------------
		Dirección:		{self._direccion.dirc}
		Telf:			{self.telf}
		Coordinador:	{self.coordinador}
		Gerente B_1:	{self.gerenteB_1}
		Gerente B_2:	{self.gerenteB_2}
		Vss Asignados:  {self.vss_asignados}
		------------------------------------------
			
			''')
		return cad
	
	@property
	def direccion(self):
		'''Lectura de atributo dirección.'''
		return self._direccion.dirc

	@direccion.setter
	def direccion(self,dirc):
		'''Modificado de atributo dirección.'''
		self._direccion.dirc = dirc
		self._direccion.coordenadas = None
		self._direccion.map_link = None
		return True	

@dataclass
class ObjVs:
	''' objeto operarios '''
	nombre:str
	id:int = None			# Nº identificación de empresa
	telf:str = None
	movilidad:str = None				# Fijo en servicio, correturnos o sin servicio.
	tip:int = None				# Nº tarjeta interprofesional
	servicio_asignado:str = None
	historial:ObjHistorial = field(default_factory=ObjHistorial)

	def __str__(self):
		cad = (
			f'''
			------------------------------------------
			OPERARIO:   {self.nombre}
			------------------------------------------
			Servicio Asignado: {self.servicio_asignado}
			Telf:		{self.telf}
			id Empresa:	{self.id}
			TIP: 		{self.tip}
			Movilidad 	{self.movilidad}
			Antigüedad 	{self.historial.antiguedad}
			------------------------------------------
			
			''')
		return cad


################################################################################
#		                     Objeto Base de Datos                              #
################################################################################

class ServVssBdd:
	''' Base de datos de operarios y servicios '''
	def __init__(self):
		self.operarios= {}
		self.servicios= {}


	#	                  CRUD: Create, Read, Update, Delete                   #
	############################################################################


	def create(self, tipo:str, **kwargs) -> True:
		'''Crea un servicio u operario y lo añade a la lista correspondiente.
		El argumento tipo debe de ser 'serv' o 'vs'.'''
		if tipo == 'vs' and not kwargs['nombre'] in self.operarios.keys():
			self.operarios[kwargs['nombre']] = ObjVs(**kwargs)
			self.operarios[kwargs['nombre']].historial.add_note(
				'Añadido vs a la base de datos')
			return True
		elif tipo == 'serv' and not kwargs['nombre'] in self.servicios.keys():
			self.servicios[kwargs['nombre']] = ObjServ(**kwargs)
			self.servicios[kwargs['nombre']].historial.add_note(
				'Añadido servicio a la base de datos')
			return True
		return 'NO_CREADO_(EL_OBJETO_YA_EXISTE)'


	def read(self, tipo:str, nombre:str=None) -> list or namedtuple:
		'''Devuelve una lista con los nombres de todos los objetos de tipo si no se 
		indica nombre o, si se especifica, devuelve namedtuple con el nombre del objeto
		original y una copia comleta del objeto leído.'''
		if not nombre and tipo:
			if tipo == 'vs':
				return sorted(list(self.operarios.keys()))
			elif tipo == 'serv':
				return sorted(list(self.servicios.keys()))
		else:
			if tipo == 'vs':
				lista = self.operarios
			elif tipo == 'serv':
				lista = self.servicios
			else:
				raise TypeError

			if nombre in lista:
				readedObject = namedtuple('readedObject', ['nombre', 'obj'])
				return readedObject(lista[nombre].nombre, copy.deepcopy(lista[nombre]))
			else:
				return 'NO_LEIDO_(EL_OBJETO_NO_EXISTE)'


	def update(self, obj_copy:tuple) -> True:
		'''Actualiza un objeto editado. Comprueba que el nombre no se edita ya que
		si lo hiciera se crearía un nuevo objeto.
		La namedtuple obj_copy contiene (nombre original del objeto, 
										 copia editable del objeto.'''
		nombre_original = obj_copy.nombre
		obj = obj_copy.obj

		if nombre_original == obj.nombre:
			if isinstance(obj, ObjServ):
				self.servicios.update({obj.nombre:obj})
				return True
			elif isinstance(obj, ObjVs):
				self.operarios.update({obj.nombre:obj})
				return True
			return  'NO_ACTUALIZADO_(ERROR_DESCONOCIDO)'
		return 'NO_ACTUALIZADO_(RESTRINGIDO_EDITAR_EL_NOMBRE)'


	def delete(self, name:str, tipo:str=None) -> True:
		'''Borra un operario o servicio por su indice de lista'''
		if tipo == None:
			if isinstance(self.read('serv', name), tuple):
				del self.servicios[name]
				return True
			elif isinstance(self.read('vs', name), tuple):
				del self.operarios[name]
				return True
		elif tipo:
			if tipo == 'serv':
				del self.servicios[name]
				return True
			elif tipo == 'vs':
				del self.operarios[name]
				return True
		return 'NO_BORRADO_(EL_OBJETO_NO_EXISTE)'


	#	           GESTIÓN DE RELACIONES ENTRE SERVICIOS Y OPERARIOS              #
	############################################################################


	def compruebaAsignacion(self, serv:str=None, *vss:str) -> True or dict:
		'''True si existen y no están asignados, detalles en otro caso.'''
		# Comprobando existencia de vss y servicio.
		result = {}
		if serv not in self.servicios.keys():
			result[serv] = 'SERVICIO_NO_EXISTE'
		else:
			result[serv] = self.servicios[serv].vss_asignados
		
		for vs in list(*vss):
			try:
				result[vs] = self.operarios[vs].servicio_asignado
			except KeyError:
				result[vs] = 'VS_NO_EXISTE'

		
		for x in result.values():
			if x:
				return result # Algún objeto no existe o no está libre.
		else:
			return True # Ningún objeto está asignado.


	def new_asig(self, serv:str=None, *vss:str) -> True or dict:
		'''Crea una nueva asignación de operarios a un servicio.'''
		resp = self.compruebaAsignacion(serv, vss)
		# Asignando operarios a servicios mediante sus atributos.
		if resp == True:
			for vs in vss:
				self.operarios[vs].servicio_asignado = serv
				self.operarios[vs].historial.add_note(
					f'Asignado servicio {serv}.', 'cambio')
			self.servicios[serv].vss_asignados = list(vss)
			# Añadiendo log en historial
			cad = str(vss).strip("(),")
			self.servicios[serv].historial.add_note(
				f'Asignados vs: {cad}.', 'cambio')
			return True
		return resp


	def edit_asig(self, serv:str, vs_out:str, vs_in:str) -> True or dict:
		'''Edita las asignaciones de operarios.'''
		resp = self.compruebaAsignacion(serv, (vs_out, vs_in))

		if resp[vs_out] == serv and resp[vs_in] == None:
			# Dando de baja
			self.servicios[serv].vss_asignados.remove(vs_out)
			self.servicios[serv].historial.add_note(
				f'Baja de vs {vs_out}.', 'cambio')
			self.operarios[vs_out].servicio_asignado=None
			self.operarios[vs_out].historial.add_note(
				f'Baja en servicio {serv}.', 'cambio')
			# Dando de alta.
			self.servicios[serv].vss_asignados.append(vs_in)
			self.servicios[serv].historial.add_note(
				f'Asignado vs {vs_in}.', 'cambio')
			self.operarios[vs_in].servicio_asignado=serv
			self.operarios[vs_in].historial.add_note(
				f'Asignado servicio {serv}.', 'cambio')
			return True
		return resp


	def close_serv(self, serv:str) -> True:
		'''Cierra un servicio.'''
		try:
			if self.servicios[serv].vss_asignados != None:
				for vs in self.servicios[serv].vss_asignados:
					self.operarios[vs].servicio_asignado = None
					self.operarios[vs].historial.add_note(
						f'Cerrado servicio: {serv}.', 'cambio')
				self.servicios[serv].vss_asignados = None
				self.servicios[serv].historial.add_note(
					'Cerrado servicio.', 'cambio')
				return True
		except TypeError:
			return 'EL_SERVICIO_NO_EXISTE'


################################################################################
#		             Objeto Cargador de la Base de Datos                       #
################################################################################

class Controler:
	def __init__(self):
		self.Bdd = None 		# Contiene el objeto Base de datos.
		self.ficheroBdd = None 	# Nombre del fichero de la Base de datos.


	def load_Bdd(self, ficheroBdd):
		'''Carga o crea una nueva base de datos.'''
		ficheroBdd += ".pickle"
		with open(ficheroBdd, 'r+b') as f:
			self.Bdd = pickle.load(f)
			self.ficheroBdd = ficheroBdd
			return True


	def save_Bdd(self):
		'''Guarda la base de datos actualizada.'''
		with open(self.ficheroBdd, 'wb') as f:
			pickle.dump(self.Bdd, f)
			return True


	def create_Bdd(self, ficheroBdd):
		'''Crea una nueva base de datos.'''	
		if not os.path.isfile(ficheroBdd + ".pickle"):
			self.Bdd = ServVssBdd()
			ficheroBdd += ".pickle"
			self.ficheroBdd = ficheroBdd
			if self.save_Bdd():
				return True
		else:
			return 'BDD_YA_EXISTE'


	def delete_Bdd(self, ficheroBdd):
		'''Borrado de fichero de base de datos.'''
		ficheroBdd += ".pickle"
		if os.path.isfile(ficheroBdd):
			os.remove(ficheroBdd)
			return True
		else:
			return 'ARCHIVO_NO_ENCONTRADO'


################################################################################
#		                 Funcionando como script.                              #
################################################################################



######### Ejecutando main() ##########
if __name__ == '__main__':
	testBDD.unittest.main(module='testBDD', verbosity=2)
