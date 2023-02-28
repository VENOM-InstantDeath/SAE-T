# Wificreds

Wificreds es una utilidad para automatizar la conexión a WiFi de SAE, no debe ser usada en sistemas personales ya que funciona en un entorno con condiciones específicas.

## Configuración de la rpi

Para que la utilidad funcione se debe configurar el entorno para que cumpla con las condiciones necesarias. Lo primero que se debe hacer es habilitar el servicio `dhcpcd` y deshabilitar `wpa_supplicant` para que el dispositivo vuelva a conectarse a internet automáticamente la próxima vez que sea encendido.

```
sudo su
systemctl enable dhcpcd
systemctl disable wpa_supplicant
```

Posteriormente se debe compilar e instalar el programa usando GCC.

```
gcc src_wificreds -o /usr/bin/wificreds
```

# Uso

Esta utilidad intenta buscar en todas las particiones disponibles si se encuentra el archivo *"WIFI"* en el directorio raíz, el cual debe tener contener dos líneas: Una especificando el ssid de la red, y en la otra línea debe estar la contraseña.

Este programa será llamado por SAE, pero si se desea probarlo, primero se debe conectar la usb y luego ejecutar el comando `wificreds` que ya estará disponible. Este programa debe ser ejecutado con permisos de superusuario. Tras ejecutarlo el proceso será automático.
