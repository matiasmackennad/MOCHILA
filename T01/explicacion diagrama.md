# Explicacion diagrama: Tarea 1: DCCriaturas fantasticas 

En primer lugar quiero decir que todas las clases se componen a partir del juego, que no es una clase, sino que se refiere
a que todas las clases se componen cuando corre main.py.

En segundo lugar, se componen desde el main 3 clases abstractas y el Dcc, desde el Dcc tambien se componen 2 de las 3
clases abstractas: Alimento y Dccriatura, ambas se agregan a la tercera clase abstracta que es Magizoologo.
 
En tercer lugar, las clases TartaMaleza, HigadoDragon y BuñuloGusarajo heredan de la clase Alimento. Las clases Augurey,
Niffler y Erkling heredan de la clase Dccriatura. Y las clases Docencio, Tareo e Hibrido heredan de la clase Magizoologo.

Por ultimo, cada clase tiene sus propios metodos y atributos, aunque en algunos casos se hacen overrides de ciertos metodos,
como es el caso de el metodo rechazo que la clase BuñueloGusarajo modifica.