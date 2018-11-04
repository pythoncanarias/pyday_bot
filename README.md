## PyDay Telegram Bot

Prueba de concepto para un bot de telegram que ayude al
asistente a eventos de Python Canarias como el PyDay.

### Prerequisitos

Requiere una Key de la API de telegram, a definir o bien 
como variable de entorno o bien en un fichero `.env`, con
el nombre `TELEGRAM_BOT_TOKEN`. Además, hay que configurar
de igual manera una variable `EVENT_TAG` para identificar
el evento que se va a utilizar. Ahora mismo el valor por
defecto es `pydaytf18`. Lo ideal seria cambiar este sistema
por otro más dinámico.

### Ejecución

Una vez instalados las librerías necesarias declaradas
en el fichero `requirements.txt` y definidas
las variables de entorno comentadas antes, podemos
arrancar el bot con:

    python main.py

Se recomiendo el uso de virtualenv o pipenv para la ejecución del bot.
