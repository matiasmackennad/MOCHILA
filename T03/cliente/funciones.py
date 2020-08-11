def generar_imagen(lista):
    datos = list()
    for parte in lista:
        largo_x = int.from_bytes(parte[4:8], byteorder='little')
        color = parte[8: 8 + largo_x].decode()
        largo_y = int.from_bytes(parte[12 + largo_x: 16 + largo_x], byteorder='little')
        tipo = parte[16 + largo_x: 16 + largo_x + largo_y].decode()
        largo_z = int.from_bytes(parte[20 + largo_x + largo_y: 24 + largo_x + largo_y],
                                 byteorder='little')
        imagen = parte[24 + largo_x + largo_y: 24 + largo_x + largo_y + largo_z]
        datos.append([color, tipo, imagen])
    return datos


def generar_bytes(parte):
    ids = [1, 2, 3]
    carta = bytearray()
    carta.extend(ids[0].to_bytes(4, byteorder='big'))
    carta.extend(len(bytearray(parte[0], encoding="UTF-8")).to_bytes(4, byteorder="little"))
    carta.extend(bytearray(parte[0], encoding="UTF-8"))
    carta.extend(ids[1].to_bytes(4, byteorder='big'))
    carta.extend(len(bytearray(parte[1], encoding="UTF-8")).to_bytes(4, byteorder="little"))
    carta.extend(bytearray(parte[1], encoding="UTF-8"))
    carta.extend(ids[2].to_bytes(4, byteorder='big'))
    carta.extend(parte[2])
    return carta

