# Base de datos
---
Programa de práctica en el que creo una base de datos de uso genérico.
Permite el diseño de comandos específicos para cada tipo de objeto en el campo que se desee en la base de datos.
Hay un módulo con las clases base de la que heredarán los correspondientes elementos que forman la base de datos.
El desarrollador diseña los elementos de cada campo según sus necesidades.
Se da opción a generar eventos que son gestionados para relacionar los diferentes campos.
### Clases Base
En el módulo **BBDD_Base** se encuentran las clases que serán la superclases de la base de datos final. 
Pensé en hacerlo de esta forma para aprovechar la modularidad de la programación orientada a objetos descartando la primera versión que solo tenía un fin específico.
De esta forma, puedo adaptar esta base de datos para otras tareas.
### Versatilidad
El punto fuerte de este programa reside en adaptar los campos a las necesidades que se tenga. 
Cada objeto se puede diseñar con las propiedades y atributos que se deseen y estos se especificarán como comandos para poder ser utilizados.
Tan solo se tendrán que ir añadiendo las funcionalidades a un diccionario global siguiendo unas sencillas reglas.

### Gestión de eventos
Los eventos se disparan mediante una lista global llamanda ```VEvent``` que es reconocida por el bucle ```CommandsAndEvents.run()```.
Son iguales que los comandos pero estos son ejecutados automáticamente, no por elección del usuario.
La ejecución de eventos pueden a su vez colocar otros eventos en la lista ```VEevent``` pero hay que tener cuidado con esto para no caer en bucles.
El bucle ejecuta comandos que pueden o no añadir un evento a esta lista. En cuanto se añade una que requiere ser tratada el bucle se encarga de gestionarla.
Al reconocer la variable utiliza un objeto ObjEvent que contiene la información necesaria para resolverla. Estos objetos se crean en la clase _**CommandsAndEvents**_ pero los detalles para crearlos se añaden a traves de las tuplas ```new_events``` y ```basic_events```, que se encuentras en las clases heredadas de tipo _**BBDD**_ y que contienen, dentro de estas tuplas, una o varias ```namedtuples``` como la siguiente:
```new_event = namedtuple('new_event', ['event', 'func', 'command'])```

Cada evento puede derivar en una función o en un comando definidos previamente. Si se elije uno de los casos, en el otro debe indicarse ```None```.
