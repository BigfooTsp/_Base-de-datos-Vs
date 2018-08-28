

class Commands:
	None
	'''Clase que constiene todos los comandos y eventos con efectos'''

"""
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


	def command_help(self, command:Optional[str] = None) -> str:
		'''Ayuda para los comandos. Si no se especifica, entrega lista con 
		todos los comandos.'''
		for c in self.command_list:
			if not command:
				cad = f"\nAYUDA DE COMANDOS:\n==============================="
				cad2 = ''
				for c in self.command_list:
					cad2 += f"\n{c.__name__}	> {c.__doc__}\n"
				return cad+cad2+"==============================="
			elif command:
				if eval(command) in self.command_list:
					i = self.command_list.index(command)
					return self.command_list[i].__doc__
				else:
					return f'Comando {command} no existe.'


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
"""         