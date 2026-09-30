# Importa los modulos necesarios.
import json
import os
from pathlib import Path
import sys
import time

# Detecta el sistema operativo para usar la funcion adecuada.
if os.name == "nt":
    import msvcrt
else:
    import select

#  Crea las rutas de inventario e documento.
Ruta_inventario = Path(__file__).with_name("inventario de papeleria.json")
Ruta_documentos = Path(__file__).with_name("documentos")

# Funcion de lectura de enteros y validacion de los precios.
def leer_entero(mensaje, minimo):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"Ingresa un número mayor o igual que {minimo}.")
        except ValueError:
            print("Entrada inválida: escribe un número entero.")

# Funcion para leer precios y validarlos.
def leer_precio(mensaje):
    while True:
        try:
            precio = float(input(mensaje))
            if precio > 0:
                return precio
            print("El precio debe ser mayor que cero.")
        except ValueError:
            print("Entrada inválida: escribe un precio numérico.")

#Funcion que muestra los productos que hay.
def mostrar_productos(inventario):
    if not inventario:
        print("No hay productos registrados.")
        return
    print("\nPRODUCTOS")
    print(f"{'Nombre':<22} {'Precio':>10} {'Existencias':>12}")
    for producto in inventario.values():
        print(f"{producto['nombre']:<22} ${producto['precio']:>9.2f} {producto['existencias']:>12}")

#Funcion que agrega productos al inventario.
def agregar_producto(inventario):
    nombre = input("Nombre del producto: ").strip()
    clave = nombre.casefold()
    if not nombre:
        print("El nombre no puede quedar vacío.")
        return
    if clave in inventario:
        print("Ese producto ya existe en el inventario.")
        return
    precio = leer_precio("Precio del producto: $")
    existencias = leer_entero("Unidades disponibles: ", 0)
    inventario[clave] = {"nombre": nombre, "precio": precio, "existencias": existencias}
    guardar_inventario(inventario)  
    print("Producto registrado correctamente.")  

#Funcion que registra la venta de algun producto, actualizando el inventario en consecuencia.
def registrar_venta(inventario):
    nombre = input("Producto vendido: ").strip()
    clave = nombre.casefold()
    if clave not in inventario:
        print("El producto no existe en el inventario.")
        return
    producto = inventario[clave]
    cantidad = leer_entero("Cantidad vendida: ", 1)
    if cantidad > producto["existencias"]:
        print(f"Venta cancelada: solo hay {producto['existencias']} unidades.")
        return
    total = producto["precio"] * cantidad
    producto["existencias"] -= cantidad
    print(f"Venta registrada. Total: ${total:.2f}")
    print(f"Existencias restantes: {producto['existencias']}")
    guardar_inventario(inventario)  

#Funcion que demuestra productos con menos de cinco unidades.
def mostrar_bajo_inventario(inventario):
    productos_bajos = [producto for producto in inventario.values() if producto["existencias"] < 5]
    if not productos_bajos:
        print("No hay productos con bajo inventario.")
        return
    print("\nPRODUCTOS CON MENOS DE 5 UNIDADES")
    for producto in productos_bajos:
        print(f"{producto['nombre']}: {producto['existencias']} unidades")

#Funcion que guarda el inventario en el archivo JSON.
def guardar_inventario(inventario):
    with Ruta_inventario.open("w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, ensure_ascii=False, indent=4)

#Funcion que carga el inventario ya guardado en el archivo JSON, si no, crea uno nuevo.
def cargar_inventario():
    if not Ruta_inventario.exists():
        inventario = {}
        guardar_inventario(inventario)
        return inventario

    try:
        with Ruta_inventario.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        print("No se pudo leer el archivo. Se iniciará un inventario vacío.")
        return {}

#Funcion que se encarga de crear los documentos de ejemplo si es que este no existe.
def preparar_documentos():
    """Crea los documentos de ejemplo si aún no existen."""
    Ruta_documentos.mkdir(exist_ok=True)
    ejemplos = {
        "bienvenida.txt": "Documento de bienvenida al sistema de inventario.\n",
        "proveedores.txt": "Proveedor: Papelería Central\nContacto: proveedor@example.com\n",
        "notas.txt": "Notas de operación del inventario.\n",
        "reporte_mensual.txt": "Reporte mensual: agrega aquí el resumen de movimientos.\n",
    }
    for nombre, contenido in ejemplos.items():
        ruta = Ruta_documentos / nombre
        if not ruta.exists():
            ruta.write_text(contenido, encoding="utf-8")

#Funcion que solicita la fecha al usuario y valida el formato.
def solicitar_fecha():
    """Valida la fecha como DD/MM/AAAA y la devuelve en una tupla."""
    while True:
        fecha_texto = input("Fecha (DD/MM/AAAA, por ejemplo 12/06/2023): ").strip()
        try:
            fecha = time.strptime(fecha_texto, "%d/%m/%Y")
            return fecha.tm_mday, fecha.tm_mon, fecha.tm_year
        except ValueError:
            print("Fecha inválida. Usa día/mes/año, por ejemplo 12/06/2023.")

#Funcion que muestra que esta cargando.
def mostrar_carga():
    """Muestra un aviso breve de carga, de menos de cinco segundos."""
    print("Cargando programa...")
    time.sleep(2)

#Funcion que lee una opcion del menu sin bloquearlo mas de diez minutos.
def leer_opcion_con_tiempo(mensaje, segundos=600):
    """Lee una línea sin bloquear el menú más de diez minutos."""
    print(mensaje, end="", flush=True)
    entrada = ""
    for _ in range(segundos):
        if os.name == "nt":
            if msvcrt.kbhit():
                caracter = msvcrt.getwch()
                if caracter in ("\r", "\n"):
                    print()
                    return entrada.strip()
                if caracter == "\b":
                    entrada = entrada[:-1]
                else:
                    entrada += caracter
                    print(caracter, end="", flush=True)
        else:
            disponible, _, _ = select.select([sys.stdin], [], [], 0)
            if disponible:
                return sys.stdin.readline().strip()
        time.sleep(1)
    print()
    return None

#Funcion que permite seleccionar un documento para leerlo o escribir.
def seleccionar_documento(accion):
    """Selecciona un archivo disponible y lo lee o reemplaza de forma segura."""
    documentos = sorted(Ruta_documentos.glob("*.txt"))
    if not documentos:
        print("No hay documentos disponibles.")
        return
    print("\nDocumentos disponibles:")
    for indice, ruta in enumerate(documentos, start=1):
        print(f"{indice}. {ruta.name}")
    nombre = input("Escribe el nombre exacto del documento: ").strip()
    ruta = next((elemento for elemento in documentos if elemento.name == nombre), None)
    if ruta is None:
        print("Documento inexistente o nombre incorrecto.")
        return
    try:
        if accion == "leer":
            print(f"\n--- {ruta.name} ---")
            print(ruta.read_text(encoding="utf-8"))
        else:
            contenido = input("Nuevo contenido: ")
            ruta.write_text(contenido + "\n", encoding="utf-8")
            print("Documento actualizado correctamente.")
    except (OSError, UnicodeDecodeError) as error:
        print(f"No se pudo {accion} el documento: {error}")

#Funcion que permite crear un documento de texto dentro de la carpeta.
def crear_documento():
    """Crea un documento de texto dentro de la carpeta permitida."""
    nombre = input("Nombre del nuevo documento (sin ruta): ").strip()
    if not nombre or Path(nombre).name != nombre:
        print("Nombre inválido. No incluyas carpetas ni dejes el nombre vacío.")
        return
    if not nombre.lower().endswith(".txt"):
        nombre += ".txt"
    ruta = Ruta_documentos / nombre
    try:
        with ruta.open("x", encoding="utf-8") as archivo:
            archivo.write(input("Contenido inicial: ") + "\n")
        print("Documento creado correctamente.")
    except FileExistsError:
        print("Ya existe un documento con ese nombre.")
    except OSError as error:
        print(f"No se pudo crear el documento: {error}")

#Funcion que demuestra el menu de inventario.
def menu_inventario(inventario):
    """Conserva las operaciones originales del control de inventario."""
    while True:
        print("\n=== CONTROL DE INVENTARIO ===")
        print("1. Consultar productos")
        print("2. Agregar producto")
        print("3. Registrar venta")
        print("4. Ver bajo inventario")
        print("5. Volver al menú principal")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            mostrar_productos(inventario)
        elif opcion == "2":
            agregar_producto(inventario)
        elif opcion == "3":
            registrar_venta(inventario)
        elif opcion == "4":
            mostrar_bajo_inventario(inventario)
        elif opcion == "5":
            return
        else:
            print("Opción inválida. Selecciona un número del 1 al 5.")

#Funcion de el menu principal.
def main():
    inventario = cargar_inventario()
    while True:
        nombre_usuario = input("Escribe tu nombre o nickname: ").strip()
        while not nombre_usuario:
            print("El nombre no puede quedar vacío.")
            nombre_usuario = input("Escribe tu nombre o nickname: ").strip()
        print("\n" + "¡Bienvenido/a, " + nombre_usuario + "!" + "\n")
        mostrar_carga()
        dia, mes, anio = solicitar_fecha()
        Fecha = dia, mes, anio
        print(f"Fecha registrada: {Fecha[0]:02d}/{Fecha[1]:02d}/{Fecha[2]}")
        preparar_documentos()

        while True:
            matriz_menu = [
                ["1", "Leer documento"],
                ["2", "Escribir en documento"],
                ["3", "Crear documento"],
                ["4", "Control de inventario"],
                ["5", "Cambiar de usuario"],
                ["6", "Salir"],
            ]
            print(f"\n=== MENÚ PRINCIPAL: {nombre_usuario} ===")
            for fila in matriz_menu:
                print(f"{fila[0]}. {fila[1]}")
            opcion = leer_opcion_con_tiempo("Selecciona una opción: ")
            if opcion is None:
                continuar = input(
                    "Han pasado 10 minutos. ¿Deseas continuar? Escribe si o no: "
                ).strip().casefold()
                if continuar == "si":
                    continue
                if continuar == "no":
                    break
                print("Respuesta no válida; escribe si o no.")
                continue
            if opcion == "1":
                seleccionar_documento("leer")
            elif opcion == "2":
                seleccionar_documento("escribir")
            elif opcion == "3":
                crear_documento()
            elif opcion == "4":
                menu_inventario(inventario)
            elif opcion == "5":
                break
            elif opcion == "6":
                print("Programa finalizado.")
                return
            else:
                print("Opción inválida. Selecciona un número del 1 al 6.")

#Esto permite que el programa se ejecute si es llamado directamente.
if __name__ == "__main__":
    main()
