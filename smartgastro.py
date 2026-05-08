class Producto:
    def __init__(self, nombre, precio, stock):
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    def get_nombre(self):
        return self._nombre

    def get_precio(self):
        return self._precio

    def get_stock(self):
        return self._stock

    def aumentar_stock(self, cantidad):
        if cantidad > 0:
            self._stock += cantidad

    def descontar_stock(self, cantidad):
        if cantidad <= 0:
            return False
        if cantidad > self._stock:
            return False
        self._stock -= cantidad
        return True


class Inventario:
    def __init__(self):
        self._productos = []

    def buscar_producto(self, nombre):
        for producto in self._productos:
            if producto.get_nombre().lower() == nombre.lower():
                return producto
        return None

    def agregar_producto(self, nombre, precio, stock):
        existente = self.buscar_producto(nombre)
        if existente is not None:
            existente.aumentar_stock(stock)
            return "Producto existente, se sumo stock."
        nuevo = Producto(nombre, precio, stock)
        self._productos.append(nuevo)
        return "Producto agregado correctamente."

    def registrar_venta(self, nombre, cantidad):
        producto = self.buscar_producto(nombre)
        if producto is None:
            return "Error: el producto no existe."
        ok = producto.descontar_stock(cantidad)
        if not ok:
            return "Error: stock insuficiente o cantidad invalida."
        total = producto.get_precio() * cantidad
        return f"Venta registrada. Total: ${total}"

    def mostrar_inventario(self):
        if len(self._productos) == 0:
            print("No hay productos cargados.")
            return
        print("\nInventario actual:")
        for producto in self._productos:
            print(f"- {producto.get_nombre()} | Precio: ${producto.get_precio()} | Stock: {producto.get_stock()}")


class Foodtruck:
    def __init__(self, nombre):
        self._nombre = nombre
        self._inventario = Inventario()

    def ejecutar(self):
        while True:
            print("\n--- SMARTGASTRO ---")
            print("1. Agregar producto")
            print("2. Registrar venta")
            print("3. Mostrar inventario")
            print("4. Salir")

            opcion = input("Elegi una opcion: ").strip()

            if opcion == "1":
                nombre = input("Nombre del producto: ").strip()
                if nombre == "":
                    print("Error: nombre invalido.")
                    continue

                try:
                    precio = float(input("Precio: "))
                    stock = int(input("Stock inicial: "))
                except ValueError:
                    print("Error: precio o stock invalido.")
                    continue

                if precio <= 0 or stock < 0:
                    print("Error: precio o stock invalido.")
                    continue

                mensaje = self._inventario.agregar_producto(nombre, precio, stock)
                print(mensaje)

            elif opcion == "2":
                nombre = input("Nombre del producto a vender: ").strip()
                try:
                    cantidad = int(input("Cantidad a vender: "))
                except ValueError:
                    print("Error: cantidad invalida.")
                    continue

                mensaje = self._inventario.registrar_venta(nombre, cantidad)
                print(mensaje)

            elif opcion == "3":
                self._inventario.mostrar_inventario()

            elif opcion == "4":
                print("Saliendo del sistema...")
                break

            else:
                print("Opcion invalida.")


if __name__ == "__main__":
    sistema = Foodtruck("SmartGastro")
    sistema.ejecutar()