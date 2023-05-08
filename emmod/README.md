# Emmmod

Una utilidad para simplificar la modificación de las respuestas de SAE.

# Compilación

```
gcc src_emmod.c menu.c ncread.c vector.c -o /usr/bin/emmod -lncurses $(pkg-config -cflags json-c) -ljson-c
```
