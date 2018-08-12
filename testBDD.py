################################################################################
#		                Test para Base de datos de vss                         #
################################################################################

import unittest
import BDD_VS_v1 as BDD
import os

################################################################################
#		                Configuración del test		                           #
################################################################################

ALL 	= True 	# Ejecutar todos los tests:
T_1 	= None  # Tests de manipulación de ficheros de la base de datos.
T_2 	= None  # Tests para objetos de la clase Notas.
T_3 	= None  # Tests para opción CREATE de la base de datos.
T_4 	= None  # Tests para opción READ de la base de datos.
T_5 	= None  # Tests para opción UPDATE de la base de datos.
T_6 	= None  # Tests para opción DELETE de la base de datos.
T_7 	= None  # Tests sobre la gestión de relaciones entre operarios y servicios.
T_8 	= None  # Tests complementarios.

################################################################################
#		           		     Clases para los tests                             #
################################################################################

@unittest.skipUnless(T_1 or ALL, 'Test no activado en configuración')
class Manipulando_ficheros_BDD(unittest.TestCase):
	'''....> Creación, carga y borrado de los ficheros base de datos.'''

	def test_Instanciando_Controlador(self):
		'''....> Creando instancia del controlador de la base de datos.'''
		Bdd = BDD.Controler()
		self.assertIsInstance(Bdd, BDD.Controler, 'NO se ha creado la instancia')

	def test_Crear_BDD(self):
		'''....> Creando una base de datos.'''
		cont = BDD.Controler()
		res = cont.create_Bdd('Test_arch')
		os.remove('Test_arch.pickle')
		self.assertEqual(res, True, 'NO se ha creado la Base de Datos')

	def test_Cargar_BDD(self):
		'''....> Cargando un fichero de base de datos.'''
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		res = cont.load_Bdd('Test_arch')
		os.remove('Test_arch.pickle')
		self.assertEqual(res, True, 'NO se ha cargado la Base de Datos')

	def test_Borrando_Ficheros_pickle(self):
		'''....> Borrando ficheros de base de datos.'''
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		res = cont.delete_Bdd('Test_arch')
		self.assertEqual(res, True, 'NO se ha borrado la Base de Datos')

@unittest.skipUnless(T_2 or ALL, 'Test no activado en configuración')
class Test_Notas_Historial(unittest.TestCase):
	'''Creación y edición de notas.'''

	def test_Crear_nota(self):
		'''....> Creando una nota directamente por instancia ObjHistorial.'''
		hist = BDD.ObjHistorial()
		self.assertTrue(hist.add_note('Probando nota'),
						 'NO se ha creado la nota')

	def test_Leer_nota(self):
		'''....> Creando una nota directamente por instancia ObjHistorial.'''
		hist = BDD.ObjHistorial()
		hist.add_note('Probando nota')
		self.assertIsInstance(hist.view_note(0), list,
						 'NO se ha leído la nota')

@unittest.skipUnless(T_3 or ALL, 'Test no activado en configuración')
class Test_Create(unittest.TestCase):
	'''Comprobando creación de objetos en base de datos.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd 

	def test_addVsToBDD(self):
		'''....> Añadiendo VS a la base de datos.'''
		res = self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado='Calle Leones')

		self.assertEqual(res, True, 
			'El vs no se ha podido crear en la base de datos.')

	def test_ExceptionChek_addVStoBDD_YaExiste(self):
		'''....> Comprobando excepción al intentar añadir VS ya existente.'''
		self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado='Calle Leones')

		res = self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado='Calle Leones')
			
		self.assertEqual(res, 'NO_CREADO_(EL_OBJETO_YA_EXISTE)', 
			'Error al indicar que el vs ya existe.')
	
	def test_addServToBdd(self):
		'''....> Añadiendo servicio a la base de datos.'''
		res = self.bdd.create('serv',
			nombre = 'Pedro José Piña', 
			telf = 544055032,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.assertEqual(res, True, 
			'El servicio no se ha podido crear en la base de datos.')

	def test_ExceptionChek_addServToBDD_YaExiste(self):
		'''....> Comprobando excepción al intentar añadir servicio ya existente.'''
		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		res = self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')
			
		self.assertEqual(res, 'NO_CREADO_(EL_OBJETO_YA_EXISTE)', 
			'Error al indicar que el servicio ya existe.')

	def tearDown(self):
		os.remove('Test_arch.pickle')

@unittest.skipUnless(T_4 or ALL, 'Test no activado en configuración')
class Test_Read(unittest.TestCase):
	'''Comprobando lectura de objetos de la base de datos.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd

		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.bdd.create('serv',
			nombre = 'Mercado Cabañal', 
			telf = 544054444,
			coordinador = 'Carlos I',
			gerenteB_1 = 'Laura',
			gerenteB_2 = 'Luis',
			_direccion = 'Calle Cabañal, 21, Valencia')

		self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado='Calle Leones')

		self.bdd.create('vs',
			nombre='David Carrera', 
			id=509113, 
			telf=544895032,
			movilidad='Fijo',
			tip=171831,
			servicio_asignado='Calle Cabañal')


	def test_readVsToBDD(self):
		'''....> Leyendo vs de la base de datos.'''
		res = self.bdd.read('vs', 'Pedro José Piña')
		self.assertIsInstance(res, tuple)

	def test_ExceptionChek_VsNoExiste(self):
		'''....> Intentando leer vs no existente.'''
		res = self.bdd.read('vs', 'Pedro José ...')
		self.assertEqual(res, 'NO_LEIDO_(EL_OBJETO_NO_EXISTE)')

	def test_readAllVs(self):
		'''....> Leyendo todos los vss.'''
		res = self.bdd.read('vs')
		self.assertIsInstance(res, list)

	def test_readServToBDD(self):
		'''....> Leyendo servicio de la base de datos.'''
		res = self.bdd.read('serv', 'Mercado Cabañal')
		self.assertIsInstance(res, tuple)

	def test_ExceptionChek_ServNoExiste(self):
		'''....> Intentando leer servicio no existente.'''
		res = self.bdd.read('serv', 'Mercado ...')
		self.assertEqual(res, 'NO_LEIDO_(EL_OBJETO_NO_EXISTE)')

	def test_readAllServs(self):
		'''....> Leyendo todos los servicios.'''
		res = self.bdd.read('serv')
		self.assertIsInstance(res, list)


	def tearDown(self):
		os.remove('Test_arch.pickle')

@unittest.skipUnless(T_5 or ALL, 'Test no activado en configuración')
class Test_Update(unittest.TestCase):
	'''Comprobando la edición y actualización de los objetos de la BDD.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd

		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.bdd.create('vs',
			nombre='David Carrera', 
			id=509113, 
			telf=544895032,
			movilidad='Fijo',
			tip=171831,
			servicio_asignado='Calle Cabañal')

	def test_EditUpdate_vs(self):
		'''....> Editando y actualizando un objeto vs de la base de datos.'''
		vs = self.bdd.read('vs', 'David Carrera')
		vs.obj.movilidad = 'Correturnos'
		res = self.bdd.update(vs)
		self.assertEqual(res, True, 
			'No se ha podido actualizar el objeto en la base de datos.')

	def test_ExceptionCheck_EditNameVs(self):
		'''....> Controlando excepción al intentar cambiar el nombre de vs.'''
		vs = self.bdd.read('vs', 'David Carrera')
		vs.obj.nombre = 'OtroNombre'
		res = self.bdd.update(vs)
		self.assertEqual(res, 'NO_ACTUALIZADO_(RESTRINGIDO_EDITAR_EL_NOMBRE)',
			'Error al indicar la advertencia de que no puede modificarse el nombre.')

	def test_EditUpdate_serv(self):
		'''....> Editando y actualizando un objeto serv de la base de datos.'''
		serv = self.bdd.read('serv', 'Mercado Leones')
		serv.obj.gerenteB_2 = 'Alfredo'
		res = self.bdd.update(serv)
		self.assertEqual(res, True, 
			'No se ha podido actualizar el objeto en la base de datos.')

	def test_ExceptionCheck_EditNameServ(self):
		'''....> Controlando excepción al intentar cambiar el nombre de serv.'''
		serv = self.bdd.read('serv', 'Mercado Leones')
		serv.obj.nombre = 'Alfredo'
		res = self.bdd.update(serv)
		self.assertEqual(res, 'NO_ACTUALIZADO_(RESTRINGIDO_EDITAR_EL_NOMBRE)', 
			'No se ha podido actualizar el objeto en la base de datos.')

	def tearDown(self):
		os.remove('Test_arch.pickle')

@unittest.skipUnless(T_6 or ALL, 'Test no activado en configuración')
class Test_Delete(unittest.TestCase):
	'''Comprobando el borrado de objetos de la BDD.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd

		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.bdd.create('vs',
			nombre='David Carrera', 
			id=509113, 
			telf=544895032,
			movilidad='Fijo',
			tip=171831,
			servicio_asignado='Calle Cabañal')

	def test_borrandoVs_soloNombre(self):
		'''....> Borrando objeto vs de la base de datos (solo con nombre como argumento).'''
		res = self.bdd.delete('David Carrera')
		self.assertEqual(res, True, 'No se ha podido eliminar el objeto vs.')

	def test_ExceptionCheck_BorrandoVsNoExistente(self):
		'''....> Comprobando mensaje de aviso al intentar borrar vs no existente con nombre únicamente como argumentos.'''
		res = self.bdd.delete('David Picazo')
		self.assertEqual(res, 'NO_BORRADO_(EL_OBJETO_NO_EXISTE)',
		 'No se ha indicado correctamente aviso por intentar borrar vs no existente.')

	def test_borrandoServ_TipoYNombre(self):
		'''....> Borrando objeto Serv de la base de datos (Con tipo y nombre como argumentos).'''
		res = self.bdd.delete('Mercado Leones', 'serv')
		self.assertEqual(res, True, 'No se ha podido eliminar el objeto serv.')

	def test_ExceptionCheck_BorrandoServNoExistente(self):
		'''....> Comprobando mensaje de aviso al intentar borrar Serv no existente con tipo y nombre como argumentos.'''
		res = self.bdd.delete('Otro')
		self.assertEqual(res, 'NO_BORRADO_(EL_OBJETO_NO_EXISTE)',
		 'No se ha indicado correctamente aviso por intentar borrar serv no existente.')

	def tearDown(self):
		os.remove('Test_arch.pickle')

@unittest.skipUnless(T_7 or ALL, 'Test no activado en configuración')
class Test_GestionandoAsignaciones(unittest.TestCase):
	'''Comprobando la gestión de asignaciones entre serv y vs.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd

		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.bdd.create('serv',
			nombre = 'Mercado Cabañal', 
			telf = 544054444,
			coordinador = 'Carlos I',
			gerenteB_1 = 'Laura',
			gerenteB_2 = 'Luis',
			_direccion = 'Calle Cabañal, 21, Valencia')

		self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado=None)

		self.bdd.create('vs',
			nombre='David Carrera', 
			id=509113, 
			telf=544895032,
			movilidad='Fijo',
			tip=171831,
			servicio_asignado=None)
		
	def test_creandoAsignacion(self):
		'''....> Creando nueva asignación de vs a servicio.'''
		res = self.bdd.new_asig('Mercado Leones', 
			'David Carrera', 'Pedro José Piña')
		self.assertEqual(res, True, 'No se ha podido crear la asignación.')
	
	def test_ComprobandologCreandoAsignacion(self):
		'''....> Comprobando que se ha registrado correctamente en el historial de los objetos la asignación nueva.'''
		self.bdd.new_asig('Mercado Leones', 'Pedro José Piña', 'David Carrera')
		log1 = self.bdd.operarios['Pedro José Piña'].historial.notas[-1].nota['text']
		log2 = self.bdd.operarios['David Carrera'].historial.notas[-1].nota['text']
		log3 = self.bdd.servicios['Mercado Leones'].historial.notas[-1].nota['text']
	
		if (log1 == 'Asignado servicio Mercado Leones.') and (
			log2 == 'Asignado servicio Mercado Leones.') and (
			log3 == "Asignados vs: 'Pedro José Piña', 'David Carrera'."):
			res = True
		else:
			res = 'ERROR DE LOG'

		self.assertEqual(res, True, 'No se ha añadido nota en historial correctamente al asignar servicio')
	
	def test_ExcepcionCheck_creandoAsignConVsNoExiste(self):
		'''....> Comprobando que no se puede crear una asignación de un servicio a un vs inexistente.'''
		res = self.bdd.new_asig('Mercado Leones', 
			'David Carrera', 'Pedro José Error')
		self.assertIsInstance(res, dict, 'No se ha podido crear la asignación.')

	def test_ExcepcionCheck_creandoAsignConServNoExiste(self):
		'''....> Comprobando que no se puede crear una asignación de un vs a un servicio inexistente.'''
		res = self.bdd.new_asig('Mercado Error', 
			'David Carrera', 'Pedro José Piña')
		self.assertIsInstance(res, dict, 'No se ha podido crear la asignación.')

	def test_ExcepcionCheck_creandoAsignConVsYServNoExiste(self):
		'''....> Comprobando que no se puede crear una asignación entre vs y servicio inexistentes.'''
		res = self.bdd.new_asig('Mercado Error', 
			'David Carrera', 'Pedro José Error')
		self.assertIsInstance(res, dict, 'No se ha podido crear la asignación.')

	def test_editandoAsignDeVs(self):
		'''....> Cambiando de vs en el servicio.'''
		self.bdd.new_asig('Mercado Leones', 'Pedro José Piña')
		res = self.bdd.edit_asig('Mercado Leones', 'Pedro José Piña', 'David Carrera')
		self.assertEqual(res, True, 'No se ha podido editar la asignación.')

	def test_CompruebaLogCambioDeVs(self):
		'''....> Comprueba que se registra en historial el cambio de vs.'''
		self.bdd.new_asig('Mercado Leones', 'Pedro José Piña')
		self.bdd.edit_asig('Mercado Leones', 'Pedro José Piña', 'David Carrera')
		log1 = self.bdd.operarios['Pedro José Piña'].historial.notas[-1].nota['text']
		log2 = self.bdd.operarios['David Carrera'].historial.notas[-1].nota['text']
		log3 = self.bdd.servicios['Mercado Leones'].historial.notas[-2].nota['text']
		log4 = self.bdd.servicios['Mercado Leones'].historial.notas[-1].nota['text']
		if (log1 == 'Baja en servicio Mercado Leones.') and (
			log2 == 'Asignado servicio Mercado Leones.') and (
			log3 == 'Baja de vs Pedro José Piña.') and (
			log4 == 'Asignado vs David Carrera.'):
			res = True
		self.assertEqual(res, True, 'No se ha añadido nota en historial correctamente al modificar servicio')

	def test_cerrandoServicio(self):
		'''....> Cierra un servicio y libera a los vs.'''
		self.bdd.new_asig('Mercado Leones', 'Pedro José Piña', 'David Carrera')
		res = self.bdd.close_serv('Mercado Leones')
		self.assertEqual(res, True, 'No se ha podido cerrar el servicio.')


	def test_CompruebaLogCierreServicio(self):
		'''....> Comprueba que se registra en historial el cierre de servicio.'''
		self.bdd.new_asig('Mercado Leones', 'Pedro José Piña', 'David Carrera')
		self.bdd.close_serv('Mercado Leones')
		log1 = self.bdd.operarios['Pedro José Piña'].historial.notas[-1].nota['text']
		log2 = self.bdd.operarios['David Carrera'].historial.notas[-1].nota['text']
		log3 = self.bdd.servicios['Mercado Leones'].historial.notas[-1].nota['text']
		if (log1 == 'Cerrado servicio: Mercado Leones.') and (
			log2 == 'Cerrado servicio: Mercado Leones.') and (
			log3 == 'Cerrado servicio.'):
			res = True
		self.assertEqual(res, True, 'No se ha añadido nota en historial correctamente al modificar servicio')


	def tearDown(self):
		os.remove('Test_arch.pickle')

@unittest.skipUnless(T_8 or ALL, 'Test no activado en configuración')
class Test_OtrasPruebas(unittest.TestCase):
	'''Otras pruebas complementarias.'''
	def setUp(self):
		cont = BDD.Controler()
		cont.create_Bdd('Test_arch')
		self.bdd = cont.Bdd

		self.bdd.create('serv',
			nombre = 'Mercado Leones', 
			telf = 544055054,
			coordinador = 'Paco León',
			gerenteB_1 = 'Maria',
			gerenteB_2 = 'Alberto',
			_direccion = 'Calle Leones, 21, Valencia')

		self.bdd.create('serv',
			nombre = 'Mercado Cabañal', 
			telf = 544054444,
			coordinador = 'Carlos I',
			gerenteB_1 = 'Laura',
			gerenteB_2 = 'Luis',
			_direccion = 'Calle Cabañal, 21, Valencia')

		self.bdd.create('vs',
			nombre='Pedro José Piña', 
			id=509013, 
			telf=544055032,
			movilidad='Fijo',
			tip=171830,
			servicio_asignado=None)

		self.bdd.create('vs',
			nombre='David Carrera', 
			id=509113, 
			telf=544895032,
			movilidad='Fijo',
			tip=171831,
			servicio_asignado=None)


	def test_ModificandoAtributo_direccion(self):
		'''....> Comprbando que la lectura y edición del atributo _direccion de ObjServ se ejecuta correctamente.'''
		res1 = self.bdd.servicios['Mercado Leones'].direccion
		res2 = self.bdd.servicios['Mercado Leones'].direccion = 'Barcelona'
		if res1 == 'Calle Leones, 21, Valencia' and res2 == 'Barcelona':
			res = True

		self.assertEqual(res, True, 
			'Las propiedades de set y read del obj dirección no responden adecuadamente.')


	def tearDown(self):
		os.remove('Test_arch.pickle')


################################################################################
#		                       Ejecutando test                                 #
################################################################################
if __name__ == '__main__':
	unittest.main(
		defaultTest=None,
		testRunner=None, 
		testLoader=unittest.defaultTestLoader, 
		exit=True, 
		verbosity=2, 
		failfast=None, 
		catchbreak=None, 
		warnings=None
		) 
