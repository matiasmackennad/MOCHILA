# Tarea 0: DCCahuin 

## Consideraciones generales :

Mi tarea entra a un loop donde estan todos los menus (que tambien son loops), en estos se pueden ir seleccionando distintas opciones, ya sea para
ir a otro menu o para realizar una funcion como seguir un usuario o escribir un post (entre otros), el codigo no sale de los loops hasta que se seleccione la opcion 
salir (0) en alguno de los menus.

### Cosas implementadas y no implementadas:

* Menu de usuarios: Hecha completa
    *Menu de inicio: Hecho completo
* Flujo del programa: Hecho completo
    * Menú de Posts: Hecha completa 
    * Menú seguidores: Hecho completo
    * Menú posts: Hecho completo
* Archivos: Hecho completo
    * Fin del programa: Hecho completo
* General:
    * Menus a prueba de errores: Hecho completo
    * El programa esta modularizado: Hecho completo
    * El programa sigue las normas PEP8: Hecho completo

## Ejecución:
El módulo principal de la tarea a ejecutar es  main.py. Además deben estar en la misma carpeta que el codigo principal:
1. seguidores.csv 
2. posts.csv 
3. usuarios.csv 
4. clases.py 
5. funciones.py 

## Librerías:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. datetime (externa, no se debe descargar, uso la funcion date.today() en la libreria clases).

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. clases: En ella esta la clase Usuario.
2. funciones: En ella hay una serie de funciones que uso en el codigo principal y en la libreria clases.

## Supuestos y consideraciones adicionales:
Los supuestos que realicé durante la tarea son los siguientes:

1. Asumi que al querer iniciar sesion, seguir o dejar de seguir a un usuario, el usuario debia escribir el nombre de este y no darle todas las opciones para que seleccione una, esto lo supuse ya que si quiere iniciar sesion, seguir a alguien o dejarlo de seguir se deberia saber el nombre.
2. Asumi que al borrar un prograpost le deberia dar las opciones para seleccionar una, ya que quisas no se acuerde de lo que escribio exactamente ni cuando.

## Referencias de código externo:

Para realizar mi tarea saqué código de:
1. https://www.tutorialspoint.com/How-to-check-if-a-string-has-at-least-one-letter-and-one-number-in-Python, es parte de la funcion validar_usuario y ayuda a determinar si hay por lo menos una letra y un numero.

