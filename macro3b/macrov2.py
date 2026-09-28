# -*- coding: utf-8 -*-
import gtk
import gobject
import ctypes
import time


#Prototipo para linux CentOS 7

# 1. CARGAR LIBRERÍAS NATIVAS DE X11 (Sin dependencias externas)
x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")

display = x11.XOpenDisplay(None)

# 2. MOTOR DE ESCRITURA MEDIANTE X11
def simular_tecleo_codigo(codigo):
    time.sleep(0.3) # Pausa inicial de seguridad
    
    for digito in codigo:
        keysym = ord(digito)
        keycode = x11.XKeysymToKeycode(display, keysym)
        
        # Presionar tecla
        xtst.XTestFakeKeyEvent(display, keycode, True, 0)
        x11.XFlush(display)
        time.sleep(0.02)
        
        # Soltar tecla
        xtst.XTestFakeKeyEvent(display, keycode, False, 0)
        x11.XFlush(display)
        time.sleep(0.02)

    # Simular tecla Enter (código X11 para Return: 0xff0d)
    enter_keycode = x11.XKeysymToKeycode(display, 0xff0d)
    xtst.XTestFakeKeyEvent(display, enter_keycode, True, 0)
    x11.XFlush(display)
    time.sleep(0.02)
    xtst.XTestFakeKeyEvent(display, enter_keycode, False, 0)
    x11.XFlush(display)

    # Volver a mostrar la ventana para el siguiente cobro
    ventana.show_all()
    return False

# 3. FUNCIÓN AL PRESIONAR UN BOTÓN
def al_clic_boton(widget, codigo):
    ventana.hide()
    # Espera 500ms antes de disparar la simulación de tecleo
    gobject.timeout_add(500, simular_tecleo_codigo, codigo)

# 4. MOTOR DEL BUSCADOR (Filtrado en tiempo real)
def al_escribir(widget_buscador):
    texto_buscado = widget_buscador.get_text().lower()
    for hijo in contenedor_productos.get_children():
        nombre = hijo.get_label().lower()
        if texto_buscado in nombre:
            hijo.show()
        else:
            hijo.hide()

# ---------------------------------------------------------
# INTERFAZ GRÁFICA (GTK 2)
# ---------------------------------------------------------
ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
ventana.set_title("Códigos Rápidos 3B")
ventana.set_default_size(300, 400)
ventana.set_keep_above(True) # Mantiene la ventana siempre visible
ventana.connect("destroy", gtk.main_quit)

caja_principal = gtk.VBox(False, 10)
ventana.add(caja_principal)

buscador = gtk.Entry()
buscador.set_tooltip_text("Buscar producto...")
buscador.connect("changed", al_escribir)
caja_principal.pack_start(buscador, False, False, 5)

area_scroll = gtk.ScrolledWindow()
caja_principal.pack_start(area_scroll, True, True, 0)

contenedor_productos = gtk.VBox(False, 5)
area_scroll.add_with_viewport(contenedor_productos)

# 5. DICCIONARIO DE PRODUCTOS
productos = {
    "Bolillo": "7501234567891",
    "Hielo 5kg": "7501234567892",
    "Garrafón Epura": "7501234567893",
    "Coca Cola 600ml": "7501055300075",
    "Pepsi 600ml": "7501031311309"
}

for nombre, codigo in productos.items():
    btn = gtk.Button(label=nombre)
    btn.connect("clicked", al_clic_boton, codigo)
    contenedor_productos.pack_start(btn, False, False, 0)

ventana.show_all()
gtk.main()