from datetime import datetime


def Tiempo_Estacionado(vehiculo, now):
    tiempo_estacionado = now - datetime.strptime(vehiculo[1], "%H:%M")
    total_minutos = tiempo_estacionado.seconds // 60
    h_estacionado = tiempo_estacionado.seconds // 3600
    m_estacionado = (tiempo_estacionado.seconds % 3600) // 60
    if m_estacionado < 10:
        m_estacionado = f"0{m_estacionado}"

    return h_estacionado, m_estacionado, total_minutos


def Busqueda_Placa(plazas):
    while True:
        try:
            placa_deseada = input("Placa del vehiculo: ")
            for i in range(len(plazas)):
                if len(plazas[i]) > 0 and plazas[i][0] == placa_deseada:
                    return plazas[i]
            raise ValueError
        except ValueError:
            print("Error: Placa no encontrada")


def Busqueda_Plaza(plazas):
    for i in range(len(plazas)):
        try:
            plaza = int(input("Número de plaza: "))
            if plaza <= 0 or plaza > len(plazas) or len(plazas[plaza - 1]) == 0:
                raise IndexError
            else:
                vehiculo = plazas[plaza - 1]
                return vehiculo
        except IndexError:
            print("Error: Número de plaza no válido")


def Ingreso(plazas, now):
    while True:
        try:
            num_plaza = int(input("Número de plaza: "))
            num_plaza -= 1
            if (num_plaza < 0) or (num_plaza >= len(plazas)):
                raise IndexError
            else:
                break
        except ValueError:
            print("Error: Debe ingresar un número entero")
        except IndexError:
            print("Error: Número de plaza no válido")

    placa = input("Placa del vehiculo: ")
    hora_actual = now.strftime("%H:%M")
    hora_entrada = input(f"Hora [{hora_actual}]: ")
    if hora_entrada == "":
        hora_entrada = hora_actual
    plazas[num_plaza] = [placa, hora_entrada]

    return plazas


def Cobro(vehiculo, minutos):
    minutos = int(minutos)
    if minutos <= 15:
        cobro = 0
    elif minutos > 15 and minutos < 540:
        cobro = round(50 * (minutos // 15 - 1) + (minutos % 15) * 50 / 15)
    else:
        cobro = 6500

    return cobro


def Estado(plazas, now):
    for i in range(len(plazas)):
        if len(plazas[i]) != 0:
            h_estacionado, m_estacionado, total_minutos = Tiempo_Estacionado(plazas[i], now)
            print(
                i + 1,
                plazas[i][0],
                plazas[i][1],
                f"({h_estacionado}:{m_estacionado})",
                Cobro(plazas[i], total_minutos)
            )
        else:
            print(f"{i+1} ------")


def main():
    while True:
        try:
            plazas_disp = int(input("Plazas disponibles: "))
            if plazas_disp <= 0:
                raise ValueError
        except ValueError:
            print("Error: Debe ingresar un número entero positivo diferente de cero")
        else:
            break

    plazas = []
    for i in range(plazas_disp):
        plazas.append([])

    now = datetime.now()

    while True:
        try:
            opcion = input("Opcion [I]ngreso [C]obro [E]stado [S]alir: ")
            if opcion in ["I", "i", "C", "c", "E", "e", "S", "s"]:
                opcion = opcion.upper()
            else:
                raise ValueError
        except ValueError:
            print("Error: Opción no válida")

        if opcion == "I":
            plazas = Ingreso(plazas, now)

        elif opcion == "C":
            try:
                metodo_busqueda = input("Buscar por [P]laca o [E]spacio: ")
                if metodo_busqueda in ["P", "p"]:
                    vehiculo = Busqueda_Placa(plazas)
                elif metodo_busqueda in ["E", "e"]:
                    vehiculo = Busqueda_Plaza(plazas)
                else:
                    raise ValueError
            except ValueError:
                print("Error: Opción no válida")

            h_estacionado, m_estacionado, total_minutos = Tiempo_Estacionado(vehiculo, now)
            cobro = Cobro(vehiculo, total_minutos)

            print("Detalle del consumo")
            print(f"Placa: {vehiculo[0]}")
            print(f"Entrada: {vehiculo[1]}")
            print(f"Salida: {now.strftime('%H:%M')}")
            print(f"Tiempo: {h_estacionado}:{m_estacionado}")
            print(f"Monto a pagar: {cobro}")

            plazas[plazas.index(vehiculo)] = []

        elif opcion == "E":
            Estado(plazas, now)

        elif opcion == "S":
            return 0


if __name__ == "__main__":
    main()
