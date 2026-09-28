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
                return precio 
            print("El precio debe ser mayor que cero.") 
        except ValueError:
            print("Entrada inválida: escribe un precio numérico.")


def mostrar_productos(inventario):
    if not inventario: 
        print("No hay productos registrados.") 
        return  
    print("\nPRODUCTOS")  
    print(f"{'Nombre':<22} {'Precio':>10} {'Existencias':>12}") 
    for producto in inventario.values(): 
        print(f"{producto['nombre']:<22} ${producto['precio']:>9.2f} {producto['existencias']:>12}")  

def main():
    inventario = cargar_inventario()
    while True:
        print("\n=== CONTROL DE INVENTARIO ===")
        print("1. Consultar productos ")  
        print("2. Agregar producto") 
        print("3. Registrar venta") 
        print("4. Ver bajo inventario") 
        print("5. Salir") 
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
            print("Programa finalizado.") 
            break 
        else: 
            print("Opción inválida. Selecciona un número del 1 al 5.") 