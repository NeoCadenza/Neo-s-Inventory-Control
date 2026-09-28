import json
from pathlib import Path
#Pa crear el archivo, este guarda los datos.
Ruta_inventario = Path(__file__).with_name("inventario de papeleria.json")

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

def main():
    inventario = cargar_inventario()
    while True:
        print("\n=== CONTROL DE INVENTARIO ===")
        print("1. Consultar productos ")  # Opción para revisar existencias.
        print("2. Agregar producto")  # Opción para registrar un producto.
        print("3. Registrar venta")  # Opción para descontar una venta.
        print("4. Ver bajo inventario")  # Opción para consultar alertas.
        print("5. Salir")  # Opción para cerrar el programa.
        opcion = input("Selecciona una opción: ").strip()  # Lee la selección del usuario.
        if opcion == "1":  # Comprueba si se solicitó el catálogo.
            mostrar_productos(inventario)  # Muestra productos y existencias.
        elif opcion == "2":  # Comprueba si se solicitó un alta.
            agregar_producto(inventario)  # Ejecuta el registro del producto.
        elif opcion == "3":  # Comprueba si se solicitó una venta.
            registrar_venta(inventario)  # Valida y procesa la venta.
        elif opcion == "4":  # Comprueba si se solicitaron alertas.
            mostrar_bajo_inventario(inventario)  # Muestra productos por reabastecer.
        elif opcion == "5":  # Comprueba si se solicitó salir.
            print("Programa finalizado.")  # Informa el cierre del programa.
            break  # Finaliza el ciclo del menú.
        else:  # Atiende opciones fuera del menú.
            print("Opción inválida. Selecciona un número del 1 al 5.")  # Solicita una opción válida.


if __name__ == "__main__":  # Evita iniciar el menú al importar este archivo.
    main()  # Inicia la aplicación de inventario.
