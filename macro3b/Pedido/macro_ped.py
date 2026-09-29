import ctypes
import ctypes.util
import threading
import time
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# 1. Cargar las librerías gráficas nativas de X11 del sistema
x11_lib = ctypes.CDLL(ctypes.util.find_library("X11"))
xtst_lib = ctypes.CDLL(ctypes.util.find_library("Xtst"))
display = x11_lib.XOpenDisplay(None)

if not display:
  raise RuntimeError("No se pudo conectar a la sesión gráfica X11.")

is_running = False


def presionar_tecla(keysym):
  """Simula la pulsación y liberación de una tecla usando XTest."""
  keycode = x11_lib.XKeysymToKeycode(display, keysym)
  xtst_lib.XTestFakeKeyEvent(display, keycode, 1, 0)
  x11_lib.XFlush(display)
  time.sleep(0.02)
  xtst_lib.XTestFakeKeyEvent(display, keycode, 0, 0)
  x11_lib.XFlush(display)


class VentanaGTK(Gtk.Window):

  def __init__(self):
    super().__init__(title="Macro Cajas a Pedir (GTK)")
    self.set_border_width(15)
    self.set_default_size(280, 200)
    self.set_resizable(False)

    # Contenedor vertical principal
    caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.add(caja)

    # Etiqueta instructiva
    self.label = Gtk.Label(label="Intervalo entre acciones (milisegundos):")
    caja.pack_start(self.label, True, True, 0)

    # Caja de entrada de texto (Entry)
    self.entrada_ms = Gtk.Entry()
    self.entrada_ms.set_text("100")
    self.entrada_ms.set_alignment(0.5)
    caja.pack_start(self.entrada_ms, True, True, 0)

    # Botón de Iniciar
    self.btn_iniciar = Gtk.Button(label="▶ Iniciar Macro")
    self.btn_iniciar.connect("clicked", self.on_iniciar_clicked)
    caja.pack_start(self.btn_iniciar, True, True, 0)

    # Botón de Detener (comienza desactivado)
    self.btn_detener = Gtk.Button(label="⏹ Detener Macro")
    self.btn_detener.set_sensitive(False)
    self.btn_detener.connect("clicked", self.on_detener_clicked)
    caja.pack_start(self.btn_detener, True, True, 0)

  def on_iniciar_clicked(self, widget):
    global is_running
    if not is_running:
      is_running = True
      self.btn_iniciar.set_sensitive(False)
      self.btn_detener.set_sensitive(True)

      # Lanzar el macro en un hilo secundario para no congelar la ventana GTK
      threading.Thread(target=self.ejecutar_bucle, daemon=True).start()

  def on_detener_clicked(self, widget):
    global is_running
    is_running = False
    self.btn_iniciar.set_sensitive(True)
    self.btn_detener.set_sensitive(False)

  def ejecutar_bucle(self):
    global is_running
    texto = self.entrada_ms.get_text()
    try:
      ms = float(texto)
    except ValueError:
      ms = 100

    intervalo = ms / 1000.0
    KEY_0 = 0x30
    KEY_DOWN = 0xFF54

    time.sleep(3)  # Margen de seguridad para enfocar BackOffice
    while is_running:
      presionar_tecla(KEY_0)
      presionar_tecla(KEY_DOWN)
      time.sleep(intervalo)


if __name__ == "__main__":
  win = VentanaGTK()
  win.connect("destroy", Gtk.main_quit)
  win.show_all()
  Gtk.main()