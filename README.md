# Proyecto para el modulo de Apoyo Logistico:

## Modulo encargado de la gestion y creacion de solicitudes para todo tipo de eventos.
## Destinado a miembros de la comunidad académica y miembros de la CCSA como multiplataforma de gestion y revision.

### Miembros:

- David Henao Salazar - A00394033
- Miguel Angel Gonzalez Arango - A00395687
- Santiago Castillo - A00395559

#### Code Style Usado: PEP-8

*Codificación para el código de Python que comprende la biblioteca estándar en la distribución principal de Python.*

#### Commit Style Usado: SemVer

*Convención en el formato de los mensajes de los commits para la legibilidad del histórico del repositorio y la automatizacion.*

https://dev.to/achamorro_dev/conventional-commits-que-es-y-por-que-deberias-empezar-a-utilizarlo-23an

> [!IMPORTANT]
> Antes de hacer la ejecución del programa, por favor revisar el *"requerimientos.txt"* para instalar las librerías necesarias con su respectivo comando y nombre mediante *"pip install <libreria_necesaria>"*
>
> 
> Para las pruebas del programa, estas se dividen en unitarias y automáticas, ejecutar el comando respectivo para cada una, siendo estos en el orden mencionado:
>
> 
> Para las unitarias: python *".\manage.py test test/unit"*
>
> 
> Para las de selenium: python *".\manage.py test test/functional"*
>
>Por otro lado para observar el coverage de de las pruebas, ejecuta: python -m coverage run manage.py test .\test\unit\
>
>Para generar reporte (despues de ejecutar las pruebas con coverage): python .\manage.py coverage report
>
>Para generar reporte exluyendo archivos propios de django: python -m coverage report --omit=mysite/settings.py,myapp/migrations/*,test/*,manage.py,myapp/__init__.py,myapp/admin.py,myapp/urls.py,mysite/urls.py,mysite/__init__.py,myapp/apps.py
>