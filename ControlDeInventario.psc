// Hola profe, si es que leyes esto, perdon. Queria hacer esto que tambien se guarde en un archivo, pero no importo cuanto buscara, no se podia. No tengo el suficiente conocimiento para esto.
Proceso ControlDeInventario
	Definir nombres Como Caracter
	Definir precios Como Real
	Definir existencias Como Entero
	Definir nombreBuscado Como Caracter
	Definir opcion, cantidad, i, posicion, totalProductos Como Entero
	Definir precio, total Como Real
	Dimension nombres[100], precios[100], existencias[100]
	
	totalProductos <- 0
	
	Repetir
		Escribir ""
		Escribir "=== CONTROL DE INVENTARIO ==="
		Escribir "1. Consultar productos"
		Escribir "2. Agregar producto"
		Escribir "3. Registrar venta"
		Escribir "4. Ver bajo inventario"
		Escribir "5. Salir"
		Leer opcion
		
		Segun opcion Hacer
			1:
				Si totalProductos = 0 Entonces
					Escribir "No hay productos registrados."
				SiNo
					Escribir ""
					Escribir "PRODUCTOS"
					Para i <- 1 Hasta totalProductos Hacer
						Escribir nombres[i], " - $", precios[i], " - ", existencias[i], " existencias"
					FinPara
				FinSi
				
			2:
				Si totalProductos = 100 Entonces
					Escribir "No se pueden registrar más productos."
				SiNo
					Escribir "Nombre del producto:"
					Leer nombreBuscado
					Si nombreBuscado = "" Entonces
						Escribir "El nombre no puede quedar vacío."
					SiNo
						posicion <- BuscarProducto(nombres, totalProductos, nombreBuscado)
						Si posicion <> 0 Entonces
							Escribir "Ese producto ya existe en el inventario."
						SiNo
							Escribir "Precio del producto:"
							Leer precio
							Mientras precio <= 0 Hacer
								Escribir "El precio debe ser mayor que cero."
								Leer precio
							FinMientras
							
							Escribir "Unidades disponibles:"
							Leer cantidad
							Mientras cantidad < 0 Hacer
								Escribir "Ingresa un número mayor o igual que 0."
								Leer cantidad
							FinMientras
							
							totalProductos <- totalProductos + 1
							nombres[totalProductos] <- nombreBuscado
							precios[totalProductos] <- precio
							existencias[totalProductos] <- cantidad
							Escribir "Producto registrado correctamente."
						FinSi
					FinSi
				FinSi
				
			3:
				Escribir "Producto vendido:"
				Leer nombreBuscado
				posicion <- BuscarProducto(nombres, totalProductos, nombreBuscado)
				Si posicion = 0 Entonces
					Escribir "El producto no existe en el inventario."
				SiNo
					Escribir "Cantidad vendida:"
					Leer cantidad
					Mientras cantidad < 1 Hacer
						Escribir "La cantidad debe ser mayor o igual que 1."
						Leer cantidad
					FinMientras
					
					Si cantidad > existencias[posicion] Entonces
						Escribir "Venta cancelada: solo hay ", existencias[posicion], " unidades."
					SiNo
						total <- precios[posicion] * cantidad
						existencias[posicion] <- existencias[posicion] - cantidad
						Escribir "Venta registrada. Total: $", total
						Escribir "Existencias restantes: ", existencias[posicion]
					FinSi
				FinSi
				
			4:
				posicion <- 0
				Para i <- 1 Hasta totalProductos Hacer
					Si existencias[i] < 5 Entonces
						posicion <- posicion + 1
					FinSi
				FinPara
				
				Si posicion = 0 Entonces
					Escribir "No hay productos con bajo inventario."
				SiNo
					Escribir ""
					Escribir "PRODUCTOS CON MENOS DE 5 UNIDADES"
					Para i <- 1 Hasta totalProductos Hacer
						Si existencias[i] < 5 Entonces
							Escribir nombres[i], ": ", existencias[i], " unidades"
						FinSi
					FinPara
				FinSi
				
			5:
				Escribir "Programa finalizado."
			De Otro Modo:
				Escribir "Opción inválida. Selecciona un número del 1 al 5."
		FinSegun
	Hasta Que opcion = 5
FinProceso

Funcion posicion <- BuscarProducto(nombres, totalProductos, nombreBuscado)
	Definir i Como Entero
	posicion <- 0
	Si totalProductos > 0 Entonces
		Para i <- 1 Hasta totalProductos Hacer
			Si Minusculas(nombres[i]) = Minusculas(nombreBuscado) Entonces
				posicion <- i
			FinSi
		FinPara
	FinSi
FinFuncion
