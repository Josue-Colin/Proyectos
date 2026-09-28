import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from pynput.keyboard import Controller, Key
import time

# 1. INICIALIZAR EL TECLADO VIRTUAL
teclado = Controller()

# 2. DICCIONARIO DE PRODUCTOS
productos = {
    "Bolillo": "7501234567891",
    "Hielo 5kg": "7501234567892",
    "Garrafón Epura": "7501234567893",
    "Coca Cola 600ml": "7501055300075",
    "Pepsi 600ml": "7501031311309"
}

# 3. EL MOTOR DE ESCRITURA MÁGICA
def ejecutar_escritura(codigo):
    
    # a) Damos un breve tiempo antes de comenzar a "escribir"
    time.sleep(0.3)
    # b) Escribimos numero por numero para simulacion real de tecleo
    for numero in codigo:
        teclado.press(numero)
        teclado.release(numero)
        time.sleep(0.02)
    
    # c) Presionamos y soltamos la tecla Enter (para que la caja registre el producto)
    teclado.press(Key.enter)
    teclado.release(Key.enter)
    
    # d) Volvemos a mostrar nuestra ventana del macro para el siguiente cliente
    ventana.show_all()
    
    # GTK requiere que devolvamos False para no repetir esta acción en bucle
    return False

# 4. FUNCIÓN AL PRESIONAR EL BOTÓN
def boton_presionado(widget, codigo):
    # a) Ocultamos inmediatamente la ventana de productos
    ventana.hide() 
    
    # b) Le decimos a la interfaz: "Espera 500 miliseg undos (0.5s) y ejecuta la escritura"
    GLib.timeout_add(500, ejecutar_escritura, codigo)

# 5. EL MOTOR DEL BUSCADOR (Se mantiene igual)
def al_escribir(widget_buscador):
    texto_buscado = widget_buscador.get_text().lower()
    lista_de_botones = contenedor_productos.get_children()
    
    for boton in lista_de_botones:
        nombre_producto = boton.get_label().lower()
        if texto_buscado in nombre_producto:
            boton.show()
        else:
            boton.hide() 

# ---------------------------------------------------------
# INTERFAZ GRÁFICA (Se mantiene igual)
# ---------------------------------------------------------
ventana = Gtk.Window(title="Códigos Rápidos 3B")
ventana.set_default_size(300, 400)
ventana.set_keep_above(True) # ¡NUEVO! Mantiene la ventana siempre visible por encima de las demás
ventana.connect("destroy", Gtk.main_quit)

caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
ventana.add(caja_principal)

buscador = Gtk.Entry()
buscador.set_placeholder_text("Buscar producto...")
buscador.connect("changed", al_escribir)
caja_principal.pack_start(buscador, False, False, 5)

area_scroll = Gtk.ScrolledWindow()
caja_principal.pack_start(area_scroll, True, True, 0)

contenedor_productos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
area_scroll.add(contenedor_productos)

for nombre, codigo in productos.items():
    boton = Gtk.Button(label=nombre)
    boton.connect("clicked", boton_presionado, codigo)
    contenedor_productos.pack_start(boton, False, False, 0)

ventana.show_all()
Gtk.main()