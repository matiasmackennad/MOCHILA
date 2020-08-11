import funciones
import datetime


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.seguidos = funciones.obtener_seguidos(nombre)

    def seguir(self, seguido):
        self.seguidos.append(seguido)
        with open("seguidores.csv", "r", encoding="utf-8", errors="ignore") as seguidos:
            lista_seguidos = seguidos.readlines()
            lista_seguidos = [linea.strip() for linea in lista_seguidos]
            lista_seguidos_split = [line.split(",") for line in lista_seguidos]
            contador = 0
            while contador < len(lista_seguidos):
                if lista_seguidos_split[contador][0] == self.nombre:
                    lista_seguidos[contador] = ",".join([self.nombre] + self.seguidos)
                    with open("seguidores.csv", "w") as seguidores:
                        for parte in lista_seguidos:
                            seguidores.write(parte)
                            seguidores.write("\n")
                        return seguido
                contador += 1

    def dejar_seguir(self, eliminado):
        self.seguidos.remove(eliminado)
        with open("seguidores.csv", "r", encoding="utf-8", errors="ignore") as seguidos:
            lista_seguidos = seguidos.readlines()
            lista_seguidos = [seguido.strip() for seguido in lista_seguidos]
            lista_seguidos_split = [seguido.split(",") for seguido in lista_seguidos]
            contador = 0
            while contador < len(lista_seguidos):
                if lista_seguidos_split[contador][0] == self.nombre:
                    lista_seguidos[contador] = ",".join([self.nombre] + self.seguidos)
                    with open("seguidores.csv", "w") as seguidores:
                        for parte in lista_seguidos:
                            seguidores.write(parte)
                            seguidores.write("\n")
                        return eliminado
                contador += 1

    def crear_post(self, texto):
        fecha = str(datetime.date.today()).replace("-", "/")
        usuario = self.nombre
        lista_post = [usuario, fecha, texto]
        post = ",".join(lista_post)
        with open("posts.csv", "a", encoding="utf-8", errors="ignore") as posts:
            posts.write(post + ";")
            posts.write("\n")

    def eliminar_post(self):
        with open("posts.csv", "r", encoding="utf-8", errors="ignore") as prograposts:
            lista_posts = prograposts.readlines()
            lista_posts = [post.strip()[0:len(post)] for post in lista_posts]
            lista_posts.sort(key=funciones.ordenar_fechas)
            lista_posts = [prograpost.split(",", 2) for prograpost in lista_posts]
            print("Estos son tus prograposts:")
            posts_propios = list()
            contador = 0
            indice = 0
            while contador < len(lista_posts):
                parte = lista_posts[contador]
                if parte[0] == self.nombre:
                    print("[" + str(indice) + "]", parte[1], parte[2][0:len(parte[2]) - 1])
                    posts_propios.append(lista_posts[contador])
                    indice += 1
                contador += 1
            if posts_propios:
                eliminado = input("Elija el prograpost que desea eliminar:")
                if eliminado.isdigit() and 140 >= int(eliminado) >= 0:
                    lista_posts.remove(posts_propios[int(eliminado)])
                    with open("posts.csv", "w", encoding="utf-8", errors="ignore") as posts:
                        for parte in lista_posts:
                            escribir = ",".join(parte)
                            posts.write(escribir)
                            posts.write("\n")
                    return True
                else:
                    print("Error: Esa opcion no existe")
                    return False
            else:
                print("Error: No tienes prograposts que eliminar")
                return False

    def mostrar_posts_propios(self, orden):
        with open("posts.csv", "r", encoding="utf-8", errors="ignore") as prograposts:
            lista_posts = prograposts.readlines()
            lista_posts = [post.strip()[0:len(post)] for post in lista_posts]
            lista_posts.sort(key=funciones.ordenar_fechas)
            lista_posts = [prograpost.split(",", 2) for prograpost in lista_posts]
            if orden == "1":
                lista_posts.reverse()
            posts_propios = list()
            contador = 0
            while contador < len(lista_posts):
                if lista_posts[contador][0] == self.nombre:
                    posts_propios.append(lista_posts[contador])
                contador += 1
            if posts_propios:
                print("Estos son tus prograposts:", "\n")
                for parte in posts_propios:
                    print(parte[0], parte[1])
                    print(parte[2][0:len(parte[2]) - 1], "\n")
                return True
            else:
                print("Error: No tienes prograposts que mostrar")
                return False

    def mostrar_posts_seguidos(self, orden):
        with open("posts.csv", "r", encoding="utf-8", errors="ignore") as prograposts:
            lista_posts = prograposts.readlines()
            lista_posts = [post.strip()[0:len(post)] for post in lista_posts]
            lista_posts.sort(key=funciones.ordenar_fechas)
            lista_posts = [prograpost.split(",", 2) for prograpost in lista_posts]
            if orden == "1":
                lista_posts.reverse()
            posts_seguidos = list()
            contador = 0
            while contador < len(lista_posts):
                if lista_posts[contador][0] in self.seguidos:
                    posts_seguidos.append(lista_posts[contador])
                contador += 1
            if posts_seguidos:
                print("Estos son los prograposts de los usuarios que sigues:", "\n")
                for parte in posts_seguidos:
                    print(parte[0], parte[1])
                    print(parte[2][0:len(parte[2]) - 1], "\n")
                return True
            else:
                print("Error: No hay prograposts que mostrar")
                return False
























