#! /usr/bin/python
#
# __author__ = [pacosalces,]
# __os__ = [RPi4OS_32bit]
#! /usr/bin/python
#
# Toca musica al azar desde disco duro externo usando VLC:
# >>> https://wiki.videolan.org/Python_bindings/
#

import os
import random
import vlc
import sh
import time
from termcolor import colored

# Monta disco duro (si es que no esta ya montado)
punto_montura = "/media/raspberto"
try:
    sh.contrib.sudo.mount("/dev/sda2", punto_montura)
except Exception as e:
    if "already" in str(e) and "mounted" in str(e):
        pass
    else:
        print(e)


# Selecciona una carpeta al azar
print(colored("Seleccionando carpeta de musica al azar.....\n", "red"))
carpeta = punto_montura + "/iTunes/iTunes Media/Music"
subcarpetas = [f.path for f in os.scandir(carpeta) if f.is_dir()]
sc_al_azar = random.choice(subcarpetas)

try:
    albumes = [album for album in os.scandir(sc_al_azar) if album.is_dir()]
    album_al_azar = random.choice(albumes)
except Exception as e:
    print(e)
    album_al_azar = sc_al_azar

print(colored("Hoy toca escuchar:\n", "blue"))
print(colored(album_al_azar.name, "magenta"))
pistas = [pista.name for pista in os.scandir(album_al_azar) if not pista.is_dir() if not pista.name.endswith('.jpg') if not pista.name.endswith('DS_Store')]
print(colored("\nLas pistas son:\n", "blue"))
for j, pista in enumerate(pistas):
    print(colored(pista, "magenta"))

# Ejecuta VLC desde el directorio aleatorio
sh.cd(album_al_azar)
for pista in pistas:
    player = vlc.MediaPlayer("./"+pista)
    player.play()
    time.sleep(1) # En lo que carga la pista
    if player.is_playing():
        print(colored("Ahora suena:\n", "green"))
        print(colored(pista, "magenta"))
        while player.is_playing():
            time.sleep(0.5)
    player.stop()
print(colored("Fin del album... saliendo...", "red"))
