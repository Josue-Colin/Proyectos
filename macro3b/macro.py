import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# 1. DICCIONARIO DE PRODUCTOS (Agregué un par más para probar el buscador)
productos = {
    "Bolillo": "7501234567891",
    "Hielo 5kg": "7501234567892",
    "Garrafón Epura": "7501234567893",
    "Coca Cola 600ml": "7501055300075",
    "Pepsi 600ml": "7501031311309"
}

def boton_presionado(widget, codigo):
    print(f"El código a escribir es: {codigo}")

# ---------------------------------------------------------
# NUEVA FUNCIÓN: EL MOTOR DEL BUSCADOR
# ---------------------------------------------------------
def al_escribir(widget_buscador):
    # a) Obtenemos el texto que el usuario acaba de escribir y lo pasamos a minúsculas
    texto_buscado = widget_buscador.get_text().lower()

    # b) Pedimos la lista de todos los botones que están dentro de nuestro contenedor
    lista_de_botones = contenedor_productos.get_children()

    # c) Revisamos botón por botón
    for boton in lista_de_botones:
        # Sacamos el nombre del producto de ese botón en específico y lo pasamos a minúsculas
        nombre_producto = boton.get_label().lower()

        # d) Comparamos: ¿Lo que escribimos está dentro del nombre de este producto?
        if texto_buscado in nombre_producto:
            boton.show()  # Si coincide, asegúrate de que el botón sea visible
        else:
            boton.hide()  # Si no coincide, oculta el botón

# ---------------------------------------------------------
# INTERFAZ GRÁFICA
# ---------------------------------------------------------
ventana = Gtk.Window(title="Códigos Rápidos 3B")
ventana.set_default_size(300, 400) # La hice un poco más alta
ventana.connect("destroy", Gtk.main_quit)

# Caja principal que guardará el buscador arriba y los productos abajo
caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
ventana.add(caja_principal)

# --- 1. CREAR LA BARRA DE BÚSQUEDA ---
buscador = Gtk.Entry()
buscador.set_placeholder_text("Buscar producto...")
# Conectamos la señal "changed" (cuando el texto cambia) a nuestra función "al_escribir"
buscador.connect("changed", al_escribir)
caja_principal.pack_start(buscador, False, False, 5)

# --- 2. CREAR UN ÁREA DESLIZABLE (SCROLL) ---
# Necesario para que si tenemos 100 productos, podamos bajar con la rueda del ratón
area_scroll = Gtk.ScrolledWindow()
caja_principal.pack_start(area_scroll, True, True, 0)

# --- 3. CAJA PARA METER LOS BOTONES ---
# Esta caja va dentro del área de scroll
contenedor_productos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
area_scroll.add(contenedor_productos)

# --- 4. GENERAR LOS BOTONES ---
for nombre, codigo in productos.items():
    boton = Gtk.Button(label=nombre)
    boton.connect("clicked", boton_presionado, codigo)
    contenedor_productos.pack_start(boton, False, False, 0)

ventana.show_all()
Gtk.main()