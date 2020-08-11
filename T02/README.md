# Tarea 2: DCCafe 

## Consideraciones generales :
El programa primero abre una ventana de inicio, desde la cual se puede iniciar una partida nueva o 
seguir una ya existente, al seleccionar una de las opciones se abre la ventana principal. El juego 
tiene tres fases: pre-ronda (en la cual se permite comprar cosas en la tienda), al apretar el boton 
comenzar parte la ronda en la cual llegan clientes y moviendo el mesero se debe atenderlos, cuando 
se acaban los clientes por atender en la ronda se pasa a la post-ronda en la que se puede guardar,
salir o seguir jugando. 


### Cosas implementadas y no implementadas:
1. Ventana de inicio: Hecho completo

2. Ventana de juego:
    * Generales: Hecho Completo
    * Ventana de Pre-Ronda: Hecho Completo
    * Ventana de Ronda: Hecho Completo
    * Ventana de Post-Ronda: Hecho Completo
    
3. Entidades:
    * Jugador (En mi programa la clase se llama Mesero): Hecho Completo
    * Chefs: Hecho Completo
    * Clientes: Hecho Completo
    * Dccafe: Hecho Completos
    * Bocadillos: Hecho Completo
    
4. Tiempo:
    * Reloj: Hecho Completo
    * Pausa: Hecho Completo
    
5. Funcionalidades extra: Hecho Completo

6. Bonus:
    * Presidente: No realizado
    * Multijugador: No realizado
    * Ratones: No realizado
    * Configuracion de parametros: No realizado


## Ejecución:
El módulo principal de la tarea a ejecutar es  main.py. Además deben estar en la misma carpeta 
que el codigo principal:
1. datos.csv
2. mapa.csv
3. front.py
4. back.py
5. dccafe.py
6. ventana_principal.py
7. funciones.py
8. DragDrop.py
9. parametros.py

## Librerías:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. PyQt5 (se debe descargar): Utilize una serie de clases de esta libreria ya sea para la 
realizacion del front o el desarrollo de los Qthread en el back, ademas de la comunucacion entre 
estos.

2. math (no se debe descargar): Ocupe la funcion floor para el calculo de la reputacion del dccafe.

3. time (no se debe descargar): Ocupe la funcion sleep para manejar el paso del tiempo.

4. sys (no se debe descargar): Ocupe la funcion exit para el correcto termino del programa.

5. threading (no se debe descargar): Ocupe la clase Event para crear el reloj, manejando con este el
 paso del tiempo y la pausa del juego, tambien importe la clase Lock y cree un atributo de la clase 
 Dccafe con esta, pero finalmente no lo ocupe y se me olvido sacarlo del codigo.
 
6. random (no se debe descargar): Ocupe la funcion random y randint de esta libreria para sucesos 
aleatorios como la posicion de algun elemento al partir una nueva partida o para el manejo de 
probabilidades. 

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. front.py: Contiene todas las clases del front menos la ventana principal y las del drag and drop.
2. back.py: Contiene todas las clases del back menos el dccafe.
3. dccafe.py: Contiene el dccafe, es decir, es la parte "logica" del programa.
4. ventana_principal.py: Es la ventana donde mas cosas se pueden realizar, en esta se desarrolla 
la gran mayoria del juego.
5. funciones.py: Son algunas funciones que utilizo en algunas partes del programa.
6. DragDrop.py: Contiene las clases que utilize para hacer funcionar el drag and drop de la tienda.
7. parametros.py: Contiene todos los parametros del programa.

## Supuestos y consideraciones adicionales:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que la reputacion solo se calcula al final de cada ronda.
2. Supuse que al perder (obtener una reputacion igual a cero) no se muestra una ventana especial, 
solo se sobre-escriben los datos y al apretar continuar en la ventana de post-ronda sera como partir
una partida desde cero.

## Referencias de código externo:

Para realizar mi tarea saqué código de:
1. Para realizar el drag and drop tome unas clases de: 
https://stackoverflow.com/questions/50232639/drag-and-drop-qlabels-with-pyqt5 y las modifique un poco.
2. La mayoria de mi clase Mesero esta basado en la clase RickSanchez de la ayudantia 8 de este ramo.