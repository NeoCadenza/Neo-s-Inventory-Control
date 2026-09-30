import json
import os
from pathlib import Path
import sys
import time

if os.name == "nt":
    import msvcrt
else:
    import select

#Pa crear el archivo, este guarda los datos.
Ruta_inventario = Path(__file__).with_name("inventario de papeleria.json")
Ruta_documentos = Path(__file__).with_name("documentos")

def leer_entero(mensaje, minimo):  # Lee un entero dentro del rango permitido.
    while True:  # Repite la solicitud mientras el dato sea inválido.
        try:  # Convierte la entrada y controla errores de formato.
            valor = int(input(mensaje))  # Guarda la cantidad ingresada.
            if valor >= minimo:  # Comprueba el mínimo aceptado.
                return valor  # Devuelve el entero validado.
            print(f"Ingresa un número mayor o igual que {minimo}.")  # Informa el límite.
        except ValueError:  # Atiende texto que no representa un número.
            print("Entrada inválida: escribe un número entero.")  # Solicita corregir.


def leer_precio(mensaje):  # Lee un precio positivo.
    while True:  # Mantiene la validación hasta recibir un precio válido.
        try:  # Convierte la entrada a número decimal.
            precio = float(input(mensaje))  # Guarda el precio ingresado.
            if precio > 0:  # Evita precios iguales o menores que cero.
                return precio  # Devuelve el precio validado.
            print("El precio debe ser mayor que cero.")  # Explica la regla.
        except ValueError:
            print("Entrada inválida: escribe un precio numérico.")  # Solicita corregir.


def mostrar_productos(inventario):  # Presenta el catálogo completo.
    if not inventario:  # Comprueba si el catálogo está vacío.
        print("No hay productos registrados.")  # Informa que no hay datos.
        return  # Termina la consulta sin recorrer el catálogo.
    print("\nPRODUCTOS")  # Identifica la sección de resultados.
    print(f"{'Nombre':<22} {'Precio':>10} {'Existencias':>12}")  # Imprime encabezados.
    for producto in inventario.values():  # Recorre cada producto registrado.
        print(f"{producto['nombre']:<22} ${producto['precio']:>9.2f} {producto['existencias']:>12}")  # Muestra sus datos.


def agregar_producto(inventario):  # Registra un producto nuevo.
    nombre = input("Nombre del producto: ").strip()  # Limpia espacios del nombre.
    clave = nombre.casefold()  # Normaliza el nombre para evitar duplicados.
    if not nombre:  # Rechaza nombres vacíos.
        print("El nombre no puede quedar vacío.")  # Explica el dato requerido.
        return  # Cancela el registro incompleto.
    if clave in inventario:  # Comprueba si el producto ya está registrado.
        print("Ese producto ya existe en el inventario.")  # Evita sobrescribirlo.
        return  # Cancela el registro duplicado.
    precio = leer_precio("Precio del producto: $")  # Solicita un precio válido.
    existencias = leer_entero("Unidades disponibles: ", 0)  # Permite iniciar en cero.
    inventario[clave] = {"nombre": nombre, "precio": precio, "existencias": existencias}  # Guarda el nuevo producto.
    guardar_inventario(inventario)  
    print("Producto registrado correctamente.")  


def registrar_venta(inventario):  # Registra una venta si hay existencias suficientes.
    nombre = input("Producto vendido: ").strip()  # Solicita el nombre del producto.
    clave = nombre.casefold()  # Busca sin distinguir mayúsculas y minúsculas.
    if clave not in inventario:  # Verifica que el producto esté registrado.
        print("El producto no existe en el inventario.")  # Rechaza productos desconocidos.
        return  # Termina la operación sin alterar existencias.
    producto = inventario[clave]  # Obtiene el registro del producto elegido.
    cantidad = leer_entero("Cantidad vendida: ", 1)  # Exige vender al menos una unidad.
    if cantidad > producto["existencias"]:  # Comprueba que alcance el inventario.
        print(f"Venta cancelada: solo hay {producto['existencias']} unidades.")  # Informa el límite disponible.
        return  # Evita vender más unidades de las disponibles.
    total = producto["precio"] * cantidad  # Calcula precio por cantidad vendida.
    producto["existencias"] -= cantidad  # Descuenta las unidades vendidas.
    print(f"Venta registrada. Total: ${total:.2f}")  # Muestra el importe cobrado.
    print(f"Existencias restantes: {producto['existencias']}")  # Confirma el nuevo inventario.
    guardar_inventario(inventario)  

def mostrar_bajo_inventario(inventario):  # Lista productos con menos de cinco unidades.
    productos_bajos = [producto for producto in inventario.values() if producto["existencias"] < 5]  # Filtra existencias bajas.
    if not productos_bajos:  # Comprueba si hay productos por reabastecer.
        print("No hay productos con bajo inventario.")  # Informa que no hay alertas.
        return  # Termina sin mostrar una lista vacía.
    print("\nPRODUCTOS CON MENOS DE 5 UNIDADES")  # Identifica la alerta.
    for producto in productos_bajos:  # Recorre los productos filtrados.
        print(f"{producto['nombre']}: {producto['existencias']} unidades")  # Muestra nombre y cantidad.

def guardar_inventario(inventario):
    with Ruta_inventario.open("w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, ensure_ascii=False, indent=4)


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


def solicitar_fecha():
    """Valida la fecha como DD/MM/AAAA y la devuelve en una tupla."""
    while True:
        fecha_texto = input("Fecha (DD/MM/AAAA, por ejemplo 12/06/2023): ").strip()
        try:
            fecha = time.strptime(fecha_texto, "%d/%m/%Y")
            return fecha.tm_mday, fecha.tm_mon, fecha.tm_year
        except ValueError:
            print("Fecha inválida. Usa día/mes/año, por ejemplo 12/06/2023.")


def mostrar_carga():
    """Muestra un aviso breve de carga, de menos de cinco segundos."""
    print("Cargando programa...")
    time.sleep(2)


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


if __name__ == "__main__":  # Evita iniciar el menú al importar este archivo.
    main()  # Inicia la aplicación de inventario.
