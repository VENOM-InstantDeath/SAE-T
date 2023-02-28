# Wificreds

Wificreds es una utilidad para automatizar la conexión a WiFi de SAE, no debe ser usada en sistemas personales ya que funciona en un entorno con condiciones específicas.

## Configuración de la rpi

Para que la utilidad funcione se debe configurar el entorno para que cumpla con las condiciones necesarias. Lo primero que se debe hacer es habilitar el servicio `dhcpcd` y deshabilitar `wpa_supplicant` para que el dispositivo vuelva a conectarse a internet automáticamente la próxima vez que sea encendido.

```
sudo systemctl enable dhcpcd
sudo systemctl disable wpa_supplicant
```


