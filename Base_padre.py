###############################################################################
#                             Base de Datos                                   #
#                             Python 3.7                                      #
#                             8 Agosto 2018                                   #
###############################################################################

import os
import pickle
from dataclasses import InitVar, dataclass
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import Base_commands

# pylint:disable=eval-used

###############################################################################
#                         Clase Campo de Base de Datos                        #
###############################################################################


@dataclass
class EntityAttribute:
    '''Objeto que forma los atributos de las entidades de la base de datos.'''

    tipo: str
    args: Optional[InitVar[Dict]] = None  # Argumentos para objeto.
    primary_key: Optional[Union[int, str]] = None  # Imprescindible al menos 1
    foraign_key: Any = None  # Acceso al atributo de otra entidad
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
        return False

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
        self.atr: Dict = {'primary_keys': [], 'foraign_keys': [], 'keys': []}


class Table:
    '''Objeto tabla de la base de datos.'''
    def __init__(self):
        self.tipo = None
        self.table_list: List[Entity] = []

    def create_entity(self, attributes_params: List[Dict]) -> int:
        '''Añade una entidad a la tabla. El primer objeto añadido define el
        tipo de objetos que contiene la tabla y como deben de ser los
        siguientes'''

        def add_atributo(entity: Entity,
                         atributo: EntityAttribute) -> Entity:
            '''Añade un atributo al objeto Entity.'''
            if atributo.primary_key:
                entity.atr['primary_keys'].append(atributo)
            elif atributo.foraign_key:
                entity.atr['foraign_keys'].append(atributo)
            else:
                entity.atr['keys'].append(atributo)
            return entity

        def comprueba_entidad(self, entity: Entity) -> bool:
            '''comprueba si el objeto es del mismo tipo de tabla y contiene
            al menos una llave primaria.'''
            # Comprueba que el objeto tenga llaves primarias.
            if not entity.atr['primary_keys']:
                if self.__comprueba_tipo(entity):
                    return True
            return False

        entity = Entity()
        for atr_dict in attributes_params:
            atributo = EntityAttribute(**atr_dict)
            entity = add_atributo(entity, atributo)
        if comprueba_entidad(self, entity):
            self.table_list.append(entity)
        return 0

    def __comprueba_tipo(self, entity: Entity) -> bool:
        '''Comprueba que un objeto entidad pertence al tipo de la tabla.'''
        # Crea tipo de tabla con el primer objeto
        ls: List[Optional[Tuple[Type, Union[int, str]]]] = []
        for atr in entity.atr.values():
            ls.append((atr.tipo, atr.primary_key))
        # Si es el primer objeto, define el tipo.
        if not self.tipo:
            self.tipo = ls
            return True
        # Comprueba si el objeto es del tipo de la tabla
        if self.tipo == ls:
            return True
        return False

    def __si_existe(self, primary_key: Union[str, int],
                    return_object: bool = False) -> Union[bool, Entity]:
        '''Comprueba si existe la entidad en la tabla a partir de su llave
        primaria o el objeto entidad mismo.
        Devuelve True/False o el objeto si se especifica en 'return_object'.'''
        for entity in self.table_list:
            if primary_key in entity.atr['primary_key']:
                if return_object:
                    return entity
                return True
            return False
        assert False  # for mypy

    def __cambia_atributos(self, entity_pk: Union[str, int],
                           new_entity: Optional[Entity] = None,
                           delete: bool = False) -> bool:
        '''Cambia los atributos de un objeto por los de otro. si delete = True
        se cambian todos los atributos a None.'''

        atrs_names = ('value', 'foraign_key', 'getCondition', 'getEffects',
                      'updateCondition', 'updateEffects', 'deleteCondition',
                      'deleteEffects')

        entity = self.__si_existe(entity_pk, return_object=True)
        if not entity:
            return False
        
        for lst in entity.atr.values():  # type: ignore
            for attribute in lst: # pylint: disable=unused-variable
                for atr_name in atrs_names:
                    prev_value = eval('attribute.'+'atr.name')
                    if delete:
                        new_value = None
                    elif new_entity:
                        new_value = new_entity.atr[atr_name]
                    if prev_value != new_value:
                        prev_value = new_value
                return True
        return False

    def read_entity(self, entity_pk: Union[str, int]) -> Union[Entity, bool]:
        '''Devuelve una copia de un elemento específico por una de sus
        llaves primarias.'''
        # [ ] Fusionar con buscar.
        entity = self.__si_existe(entity_pk, return_object=True)
        if entity:
            return entity
        return False

    def update_entity(self, new_entity: Entity) -> bool:
        '''Acutaliza un elemento.Todas Las llaves primarias no se pueden
        modificar'''
        pk = new_entity.atr['primary_keys']
        if self.__comprueba_tipo(new_entity) and self.__si_existe(pk):
            self.__cambia_atributos(pk, new_entity)
        return False

    def delete_entity(self, primary_key: Union[str, int]) -> bool:
        '''Elimina un elemento.'''
        entity = self.__si_existe(primary_key, return_object=True)
        if entity:
            del entity
            return True
        return False


###############################################################################
#                                Clase Base de Datos                          #
###############################################################################


class BaseBbdd:
    '''Clase base de la base de datos.'''
    def __init__(self):
        # Contiene todas las tablas de la base de datos
        # [ ] Realmente es necesario el __init para una variable constante?
        self._table: Dict[Union[str, int], Table] = {}

    def add_table(self, nombre):
        '''Añade un campo a la base.'''
        if nombre not in self._table:
            self._table.update({nombre: Table()})
            return True
        return False

    def delete_table(self, nombre):
        '''Borra un campo de la base.'''
        if nombre in self._table:
            del self._table[nombre]
            return True
        return False

    def search_entity(self, busqueda: Union[str, int],
                      table: Optional[Union[str, int]] = None
                      ) -> List:
        '''Devuelve lista con las claves primarias de las entidades que 
        coincidan con una búsqueda.'''
        # [] Utilizar expresiones regulares

        def search(busqueda, table, entity):
            result = []  # type: List[Optional[Tuple[Union[str, int], Union[str, int]]]]
            if busqueda in entity.atr['primary_keys']:
                result.append(table, entity.atr['primary_keys'])
            return result          

        if not table:
            for k, v in self._table.items():
                for entity in v.table_list:  # type: Entity
                    return search(busqueda, k, entity)
        else:
            for entity in self._table[table].table_list:
                return search(busqueda, table, entity)
        assert False  # for mypy


###############################################################################
#               Clase operadora de la Base de Datos                           #
###############################################################################


class BaseOperator:
    '''Clase operadora que se encarga de la gestión del archivo de la base
    de datos y los comandos. Esta será la clase que será instanciada para
    iniciar el trabajo con la base de datos.'''
    def __init__(self,
                 bbdd: BaseBbdd = BaseBbdd(),
                 command: Base_commands.Commands = Base_commands.Commands(),
                 ) -> None:
        # Inicializando Base de datos.
        self.bbdd = bbdd
        # Nombre del fichero de la Base de datos.
        self.fichero_bbdd: Optional[str] = None
        # Inicializando gestor de comandos.
        self.com = command

    def load_bbdd(self, fichero_bbdd: str) -> bool:
        '''Carga nueva base de datos del tipo actual.
        [fichero_bbdd:str] -> 0'''
        fichero_bbdd += ".pickle"
        if os.path.isfile(fichero_bbdd):
            with open(fichero_bbdd, 'r+b') as f:
                self.BBdd = pickle.load(f)
                self.fichero_bbdd = fichero_bbdd
                return True
        return False

    def save_bbdd(self, fichero_bbdd: str = None) -> bool:
        '''Guarda la base de datos actualizada.
        [fichero_bbdd:str = None] -> 0'''
        if not fichero_bbdd:
            if self.fichero_bbdd:
                fichero_bbdd = self.fichero_bbdd
            else:
                return False
        elif fichero_bbdd:
            fichero_bbdd += ".pickle"
        with open(fichero_bbdd, 'wb') as f:
            pickle.dump(self.BBdd, f)
            return True

    def delete_bbdd(self, fichero_bbdd: str) -> bool:
        '''Borrado de fichero de base de datos.
        [fichero_bbdd:str] -> 0'''
        fichero_bbdd += ".pickle"
        if os.path.isfile(fichero_bbdd):
            os.remove(fichero_bbdd)
            return True
        return False


###########################################################################
#                        Funcionando como script.                         #
###########################################################################


if __name__ == '__main__':
    pass
