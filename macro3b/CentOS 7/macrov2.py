# -*- coding: utf-8 -*-
import gtk
import gobject
import ctypes
import time
import json
import os

# 1. CARGAR LIBRERÍAS NATIVAS DE X11 (Cero dependencias externas)
x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")

display = x11.XOpenDisplay(None)

# 2. CARGAR PRODUCTOS DESDE UN ARCHIVO JSON EXTERNO
script_dir = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(script_dir, "productos.json")
if os.path.exists(ruta_json):
    with open(ruta_json, "r") as f:
        productos = json.load(f)
else:
    # Diccionario de respaldo por si el archivo no existe todavía
    productos = {
        "Bolillo": "7501234567891",
        "Hielo 5kg": "7501234567892"
    }

# 3. MOTOR DE ESCRITURA MEDIANTE X11 (Simulación de teclado a nivel de sistema operativo)
def simular_tecleo_codigo(codigo):
    time.sleep(0.3)  # Pausa inicial de seguridad para que la ventana se oculte bien
    
    for digito in codigo:
        keysym = ord(digito) #ord lo que hace es convertir el caracter en su codigo ASCII
        keycode = x11.XKeysymToKeycode(display, keysym)
        
        # Presionar tecla virtualmente
        xtst.XTestFakeKeyEvent(display, keycode, True, 0)
        x11.XFlush(display)
        time.sleep(0.01)
        
        # Soltar tecla virtualmente
        xtst.XTestFakeKeyEvent(display, keycode, False, 0)
        x11.XFlush(display)
        time.sleep(0.01)

    # # Simular la tecla Enter (Código X11 para Return: 0xff0d)
    # enter_keycode = x11.XKeysymToKeycode(display, 0xff0d)
    # xtst.XTestFakeKeyEvent(display, enter_keycode, True, 0)
    # x11.XFlush(display)
    # time.sleep(0.02)
    # xtst.XTestFakeKeyEvent(display, enter_keycode, False, 0)
    # x11.XFlush(display)

    # Volver a mostrar la ventana para el siguiente cobro
    ventana.show_all()
    return False

# 4. FUNCIÓN AL PRESIONAR UN BOTÓN DE PRODUCTO
def al_clic_boton(widget, codigo):
    ventana.hide()  # Oculta la interfaz para que el tecleo vaya al software de cobro
    # Programa la escritura tras 250ms usando el bucle de eventos de GLib/GObject
    gobject.timeout_add(250, simular_tecleo_codigo, codigo)

# 5. MOTOR DEL BUSCADOR (Filtrado dinámico en tiempo real)
def al_escribir(widget_buscador):
    texto_buscado = widget_buscador.get_text().lower()
    for hijo in contenedor_productos.get_children():
        nombre = hijo.get_label().lower()
        if texto_buscado in nombre:
            hijo.show()  # Muestra el botón si coincide con la búsqueda
        else:
            hijo.hide()  # Oculta el botón si no coincide

# ---------------------------------------------------------
# INTERFAZ GRÁFICA (GTK 2)
# ---------------------------------------------------------
ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
ventana.set_title("Códigos Rápidos 3B")
ventana.set_default_size(300, 400)
ventana.set_keep_above(True)  # Mantiene la ventana siempre flotando arriba
ancho_pantalla = gtk.gdk.screen_width()
ancho_ventana = 300
margen_derecho = 15
pos_x = ancho_pantalla - ancho_ventana - margen_derecho
pos_y = 40
ventana.move(pos_x, pos_y)
ventana.connect("destroy", gtk.main_quit)

caja_principal = gtk.VBox(False, 10)
ventana.add(caja_principal)

buscador = gtk.Entry()
buscador.set_tooltip_text("Buscar producto...")
buscador.connect("changed", al_escribir)  # Detecta cada letra que escribas
caja_principal.pack_start(buscador, False, False, 5)

area_scroll = gtk.ScrolledWindow()
caja_principal.pack_start(area_scroll, True, True, 0)

contenedor_productos = gtk.VBox(False, 5)
area_scroll.add_with_viewport(contenedor_productos)

# 6. CREACIÓN DINÁMICA DE BOTONES A PARTIR DEL DICCIONARIO
for nombre, codigo in productos.items():
    btn = gtk.Button(label=nombre)
    btn.set_focus_on_click(False)
    btn.connect("clicked", al_clic_boton, codigo)  # Conecta el clic con la función enviando su código
    contenedor_productos.pack_start(btn, False, False, 0)

ventana.show_all()
gtk.main()