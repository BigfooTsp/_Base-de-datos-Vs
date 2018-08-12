################################################################################
#		Base de Datos de Operarios y servicios 								   #
# 		Python 3.7		                                                       #
#       8 Agosto 2018    													   #
################################################################################

import time
from dataclasses import dataclass, field
from BBDD_2 import BBDD_Base, BBDD_Field, BBDD_Operator, Field_element, mainLoop

################################################################################
#                    Clases para atributos de elementos                        #
################################################################################

class ObjNotas:
	'''Objeto de control para las notas.'''
	def __init__(self):
		self.notas=[]

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

	def add_note(self, text:str, tag:str="nota") -> True:
		'''Añade una nueva nota.''' 
		self.notas.append(self.ObjNota(text, tag))
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


class ObjVacaciones:
	''' Se encargará de gestionar las vacaciones pendientes y disfrutadas
	de los operarios así como un historial de ellas'''
	def __init__(self):
		self.disfrutadas = None
		self.pendientes = None
		self.asigandas = None


class ObjDireccion:
	None


class ObjAntiguedad:
	'''Clase que contiene información sobre la antigüedad del operario.'''
	def __init__(self, fecha=None):
		self.fecha = None

	def get_antiguedad(self):
		'''Calcula y devuelve el tiempo que lleva el operario en la empresa
		teniendo en cuenta la fecha del dispositivo actual.'''
		None
################################################################################
#                    Clases para los campos de la Base de Datos                #
################################################################################

@dataclass
class ObjVs(Field_element):
	'''Campo que contiene los operarios.'''
	nombre:str
	id:int = None			# Nº identificación de empresa
	telf:str = None
	movilidad:str = None	# Fijo en servicio, correturnos o sin servicio.
	tip:int = None			# Nº tarjeta interprofesional
	servicio_asignado:str = None
	antiguedad:ObjAntiguedad = field(default_factory=ObjAntiguedad)
	vacaciones:ObjVacaciones = field(default_factory=ObjVacaciones)
	historial:ObjNotas = field(default_factory=ObjNotas)

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
			Antigüedad 	{self.antiguedad.fecha}
			------------------------------------------
			
			''')
		return cad

	def runFieldComand(self, comand:str) -> str:
		'''lista de comandos esepcíficos para el tipo de objeto. Devuelve 
		evento en forma de texto que será procesado por la clase operadora'''
		# [ ] Añade nota en historial
		# [ ] Busca nota en historial
		# [ ] Edita nota en historial
		# [ ] Muestra nota de historial
		# [ ] Borra nota de historial
		# [ ] Obtiene antigüedad del operario


class ObjServ(BBDD_Field):
	'''Campo que contiene los servicios.'''
	None


class ObjRelaciones(BBDD_Base):
	'''Campo que relaciona los vs y servicios de la base de datos.'''
	None	


################################################################################
#                         Clases para  la Base de Datos                        #
################################################################################

class BBDD_Serv_Vs(BBDD_Base):
	None	

################################################################################
#		                 Funcionando como script.                              #
################################################################################

def main():
	mainLoop()

if __name__ == '__main__':
	main()