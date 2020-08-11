# Tarea 3: DCCuatro

## Consideraciones generales :
El programa primero abre una ventana de inicio, desde la cual se puede ingresar un nombre, el 
servidor revisa que no este ocupoado ese nombre y que sea alfanumerico, si no cumple alguna de estas
condiciones pide ingresar otro nombre, si las cumple se entra en la sala de espera. En la sala de 
espera el servidor mantiene actualizado si alguien ingresa o sale de esta, cuando se llena se 
ingresa en la sala de juego. En la sala de juego es donde realmente se juega, es por turnos y se
juega hasta que solo una persona no haya perdido, hasta que solo una persona este activa o que a 
alguien se le acaben las cartas.


### Cosas implementadas y no implementadas:
1. Networking: Hecho completo
    * De host use localhost, y si lo deje en parametros.json, pero el port se me olvido dejarlo ahi,
    use el port 8080 y lo puedes cambiar en el main del servidor y del cliente.

2. Arquitectura cliente-servidor: Hecho completo
    
3. Manejo de bytes: Hecho Completo
    
4. Interfaz Grafica: Hecho Completo
    
5. Reglas del DCCuatro: Hecho Completo
    * Al usar el comando gritar DCCuatro, se roba las cartas inmediatamente, no se espera al turno 
    de quien tenga que robar para que esto ocurra.

6. Bonus: No realizado


## Ejecución:
Los módulos principales de la tarea se llaman main.py, uno esta en la carpeta cliente y el otro en 
la carpeta servidor.
 
Además, en la carpeta del cliente debe estar:  
1. front.py
2. back.py
3. ventana_juego.py
4. funciones.py
5. parametros.json

Además, en la carpeta del servidor debe estar:  
1. funciones.py
2. generador_de_mazos.py
3. parametros.json

## Librerías:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. PyQt5 (se debe descargar): Utilize una serie de clases de esta libreria ya sea para la 
realizacion del front o la comunicacion entre el front y el back.

2. sys (no se debe descargar): Ocupe la funcion exit para el correcto termino del programa.

3. threading (no se debe descargar): Ocupe Threads para escuchar distintos clientes en el servidor.
 
6. socket (no se debe descargar): Lo ocupe para la correcta comunicacion entre el cliente y el 
servidor. 

7. pickle (no se debe descargar): Lo ocupe para mandar ciertos elementos en forma de bytes entre el 
cliente y el servidor.

8. json (no se debe descargar): Lo ocupe para el correcto uso de parametros.json, tanto en el 
cliente como en el servidor.

extra: generador_de_mazos.py: Es el archivo que se nos entrega para sacar las cartas en el servidor
para enviarselas a los clientes y se encuentra en la carpeta servidor.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

En la carpeta cliente:
1. front.py: Contiene todas las clases del front menos la ventana de juego.
2. back.py: Contiene la clase client, que procesa cierta informacion y la envia al servidor.
3. ventana_juego.py: Es la ventana donde mas cosas se pueden realizar, en esta se desarrolla 
la gran mayoria del juego.
4. funciones.py: Son algunas funciones que utilizo en algunas partes del programa del cliente.

En la carpeta servidor:
1. funciones.py: Son algunas funciones que utilizo en algunas partes del programa del servidor.

    extra: generador_de_mazos.py: Es el archivo que se nos entrega para sacar las cartas en el 
    servidor para enviarselas a los clientes.


## Supuestos y consideraciones adicionales:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que al perder (tener 10 o más cartas) no se muestra una ventana especial, 
solo aparece un mensaje que dice que perdiste y no se te deja seguir jugando, sin embargo si se 
mantiene actualizado lo que hace el resto.

## Referencias de código externo:

Para realizar mi tarea saqué código de:
1. La mayoria de la clase client y server fueron sacadas del archivo 3-ejemplos.ipynb de la semana 
14 de este ramo. 
2. Algunas ideas para los metodos del servidor las saque de la actividad formativa 6 de este ramo.
