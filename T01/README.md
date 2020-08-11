# Tarea 1: DCCriaturas fantasticas 

## Consideraciones generales :

Mi tarea entra a un loop donde estan todos los menus (que tambien son loops), en estos se pueden ir seleccionando 
distintas opciones, ya sea para ir a otro menu o para realizar una funcion como alimentar una dccriatura o comprar un 
alimento (entre otros), el codigo no sale de los loops hasta que se seleccione la opcion salir (0) en alguno de los menus.

### Cosas implementadas y no implementadas:

* Programacion Orientada a Objetos: hecho completo
    * Diagrama: Hecho completo
    * Definicion de clases, atributos y metodos: Hecho completo
    * Relacion entre clases: Hecho completo
* Partidas: Hecho completo
    * Crear partida: Hecha completa 
    * Cargar partida: Hecho completo
    * Guardar: Hecho completo
* Acciones: Hecho completo
    * Cuidar Dccriaturas: Hecho completo
    * DCC: Heacho completo
    * Pasar al dia siguiente: Hecho completo
* Consola: Hecho completo
    * Menus de inicio: Hecho completo
    * Menus de acciones: Hecho completo
    * Menus de dccriaturas: Hecho completo
    * Menus DCC: Hecho completo
    * Pasar al dia siguiente: Hecho completo
    * Robustez: Hecho completo
* Bonus: No realizado
    * Super Magizoologo: No realizado
    * Peleas de Dccriaturas: No realizado

## Ejecución:
El módulo principal de la tarea a ejecutar es  main.py. Además deben estar en la misma carpeta que el codigo principal:
1. magizoologos.csv 
2. criaturas.csv 
3. funciones.py 
4. criaturas.py 
5. DCC.py
6. zoologos.py
7. parametros.py 

## Librerías:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. random (externa, no se debe descargar, uso la funcion randint).
2. abc (externa, no se debe descargar, use ABC y abstractmethod para crear las clases y metodos abstractos)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. funciones.py (En ella hay diversas funciones que utilizo)
2. criaturas.py (En ella estan las clases de las dccriaturas)
3. DCC.py (En ella esta la clase Dcc y las clases de alimentos)
4. zoologos.py (En ella estan las clases de magizoologos)
5. parametros.py (En ella estan todos los valores constantes del programa)

## Supuestos y consideraciones adicionales:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumi que al crear un magizoologo, el nombre debe ter al menos 8 caracteres, para evitar la creacion de nombres 
muy cortos.
2. Asumi que el nombre de una dccriatura debe tener al menos un caracter.




