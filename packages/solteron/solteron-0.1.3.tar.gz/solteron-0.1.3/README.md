
# Solterón

## Descripción
`Solteron` es un módulo de Python que incluye una meta-clase, del mismo nombre, que puede ser heredada para garantizar una correcta implementación del patrón *'Singleton'* en tipos definidos por el usuario. Esto se logra interfiriendo con el curso de _construcción_ de las instancias de clases marcadas con `metaclass=Solteron`, devolviendo la instancia ya creada o instanciando una nueva sólo en caso que no exista.

## Instalación
Puede decargar e instalar `solteron` utilizando el manejador de paquetes `PIP`, según se indica a continuación:

**Ejecute** el siguiente comando en la `terminal`:

``` Bash
pip install solteron
``` 

## Uso Básico
Puede emplear tanto `Solteron` como `Singleton` en la definición de la clase para garantizar que el patró se aplique.

```python
from solteron import Solteron, Singleton

class MiSingleton(metaclass = Solteron):
    ...

class MiOtroSingleton(metaclass = Singleton)

```
