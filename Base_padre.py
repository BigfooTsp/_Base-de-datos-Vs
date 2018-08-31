###############################################################################
#                             Base de Datos                                   #
#                             Python 3.7                                      #
#                             8 Agosto 2018                                   #
###############################################################################
import os
import pickle
from dataclasses import InitVar, dataclass
# Gestor de comandos:
#import Base_commands as commands_manager
from typing import Any, Dict, List, Optional, Tuple, Type, Union

# typing alias:
Inmutable = Union[str, int]
TableType = List[Optional[Tuple[Type, Inmutable]]]

# Configuraciones para linter
# pylint:disable=eval-used

###############################################################################
#                         Clase Campo de Base de Datos                        #
###############################################################################


@dataclass
class EntityAttribute:
    """Objeto que forma los atributos de las entidades de la base de datos."""

    tipo: str
    args: InitVar[Dict]  # Argumentos para objeto.
    primary_key: Optional[Inmutable] = None  # Imprescindible al menos 1
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
    """Clase padre de entidad de las tablas.

    Las entidades se crearán mediante factoría para que cumplan ciertas condiciones
    como la organización de sus atributos dentro de una lista.
    Los diferentes tipos compatibles se definen dentro del módulo Base_tipos.
    """

    def __init__(self):
        self.atr: Dict = {'primary_keys': [], 'foraign_keys': [], 'keys': []}


class Table:
    """Objeto tabla de la base de datos."""

    def __init__(self):
        self.tipo = None
        self.table_list: List[Entity] = []

    def __compruebaTipo(self, entity: Entity) -> bool:
        """Comprueba que un objeto Entity pertence al tipo de la tabla."""
        # Crea tipo de tabla con el primer objeto
        ls: TableType = []
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

    def __cambiaAtributos(self, entity_pk: Inmutable,
                          new_entity: Optional[Entity] = None,
                          delete: bool = False) -> bool:
        """Cambia los atributos de un objeto por los de otro.
        
        Las llaves primarias no se pueden modificar.
        Si delete = True se cambian todos los atributos a None.
        """
        atrs_names = ('value', 'foraign_key', 'getCondition', 'getEffects',
                      'updateCondition', 'updateEffects', 'deleteCondition',
                      'deleteEffects')

        entity = self.siExiste(entity_pk, return_object=True)
        if isinstance(entity, Entity):
            for lst in entity.atr.values():
                for attribute in lst:  # pylint: disable=unused-variable
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

    def createEntity(self, attributes_params: List[Dict]) -> int:
        """Añade una entidad a la tabla.
        
        El primer objeto añadido define el tipo de objetos que contiene la tabla y
        como deben de ser los siguientes.
        """
        def addAttribute(entity: Entity,
                         atributo: EntityAttribute) -> Entity:
            """Añade un atributo al objeto Entity."""
            if atributo.primary_key:
                entity.atr['primary_keys'].append(atributo)
            elif atributo.foraign_key:
                entity.atr['foraign_keys'].append(atributo)
            else:
                entity.atr['keys'].append(atributo)
            return entity

        def compruebaEntidad(self, entity: Entity) -> bool:
            """Comprueba si el objeto es correcto.
            
            Dede de ser del mismo tipo de tabla y contener al menos una llave 
            primaria.
            """
            if not entity.atr['primary_keys']:
                if self.__compruebaTipo(entity):
                    return True
            return False

        entity = Entity()
        for atr_dict in attributes_params:
            atributo = EntityAttribute(**atr_dict)
            entity = addAttribute(entity, atributo)
        if compruebaEntidad(self, entity):
            self.table_list.append(entity)
        return 0

    def siExiste(self, primary_key: Inmutable,
                 return_object: bool = False) -> Union[bool, Entity]:
        """Comprueba si existe un determinado objeto Entity en la tabla.
        
        A partir de su llave primaria o el objeto entidad mismo.
        Devuelve True/False o el objeto si se especifica en 'return_object'.
        """
        for entity in self.table_list:
            if primary_key in entity.atr['primary_key']:
                if return_object:
                    return entity
                return True
            return False
        assert False  # for mypy

    def readEntity(self, entity_pk: Inmutable) -> Union[Entity, bool]:
        """Devuelve una copia de un elemento específico ."""
        entity = self.siExiste(entity_pk, return_object=True)
        if entity:
            return entity
        return False

    def updateEntity(self, new_entity: Entity) -> bool:
        """Acutaliza un elemento.
        
        Esto lo hace independientemente para cada atributo por si tuviera efectos
        secundarios definidos.
        Las llaves primarias no se pueden modificar.
        """
        pk = new_entity.atr['primary_keys']
        if self.__compruebaTipo(new_entity) and self.siExiste(pk):
            self.__cambiaAtributos(pk, new_entity)
        return False

    def deleteEntity(self, primary_key: Inmutable) -> bool:
        """Elimina un elemento."""
        entity = self.siExiste(primary_key, return_object=True)
        if isinstance(entity, Entity):
            self.__cambiaAtributos(primary_key, delete=True)
            del (entity)
            return True
        return False


###############################################################################
#                                Clase Base de Datos                          #
###############################################################################


class BaseBbdd:
    """Clase base de la base de datos."""

    def __init__(self):
        # Contiene todas las tablas de la base de datos
        # [ ] Realmente es necesario el __init para una variable constante?
        self._table: Dict[Inmutable, Table] = {}

    def addTable(self, nombre):
        """Añade un campo a la base."""
        if nombre not in self._table:
            self._table.update({nombre: Table()})
            return True
        return False

    def deleteTable(self, table_name):
        """Borra un campo de la base."""
        if table_name in self._table:
            for entity in self._table[table_name]:
                self._table[table_name].deleteEntity(entity.atr['primary_keys'])
                del self._table[table_name]
                return True
        return False

    def searchEntity(self, busqueda: Inmutable,
                     table: Optional[Inmutable] = None
                     ) -> List:
        """Devuelve lista con las claves primarias de la búsqueda."""
        # [] Utilizar expresiones regulares
        result: List[Tuple[Inmutable, List[Inmutable]]] = []
        if not table:
            for table_name, table_obj in self._table.items():
                entity = table_obj.siExiste(busqueda, return_object=True)
                if isinstance(entity, Entity):
                    result.append((table_name, entity.atr['primary_keys']))
        else:
            entity = self._table[table].siExiste(busqueda, return_object=True)
            if isinstance(entity, Entity):
                result.append((table, entity.atr['primary_keys']))
        return result


###############################################################################
#               Clase operadora de la Base de Datos                           #
###############################################################################


class BaseOperator:
    """Clase operadora de la base de datos.
    
    Carga y guarda los archivos de la base de datos.
    Carga el gestor de comandos y desvía a este los comandos.
    """

    def __init__(self,
                 bbdd: BaseBbdd = BaseBbdd(),
                 command: Optional[type] = None # deshabilitado temporalmente
                 ) -> None:
        # Inicializando Base de datos.
        self.bbdd = bbdd
        # Nombre del fichero de la Base de datos.
        self.fichero_bbdd: Optional[str] = None
        # Inicializando gestor de comandos.
        self.com = command

    def loadBbdd(self, fichero_bbdd: str) -> bool:
        """Carga nueva base de datos del tipo actual."""
        fichero_bbdd += ".pickle"
        if os.path.isfile(fichero_bbdd):
            with open(fichero_bbdd, 'r+b') as f:
                self.BBdd = pickle.load(f)
                self.fichero_bbdd = fichero_bbdd
                return True
        return False

    def saveBbdd(self, fichero_bbdd: str = None) -> bool:
        """Guarda la base de datos actualizada."""
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

    def deleteBbdd(self, fichero_bbdd: str) -> bool:
        """Borrado de fichero de base de datos."""
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


######### Tareas  #########
#[ ] Asegurarse de que al modificar un objeto se debe de quedar al menos con una de
#   las llaves primarias.

#[ ] Desarrollar los tests.
