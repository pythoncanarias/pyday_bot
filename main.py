#!/usr/bin/env python

from prettyconf import config
import logging
from functools import wraps
from emoji import emojize

import telegram
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler

import utils
import templates
import inspect
from event import Event

VERSION = "0.1"
MARKDOWN = telegram.ParseMode.MARKDOWN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    )

_kernel = {}


def is_command(f):
    global _kernel
    name = f.__name__

    @wraps(f)
    def wrapper(bot, update, args=None):
        logging.info('received {cmd} command from {user[username]}'.format(
            cmd=name,
            user=update.message.from_user,
            ))
        chat_id = update.message.chat_id
        if args:
            understood, message = f(bot, update, args)
        else:
            understood, message = f(bot, update)
        if not understood:
            message = emojize(
                ":confused: {}".format(message),
                use_aliases=True,
                )
        bot.send_message(chat_id=chat_id, text=message, parse_mode=MARKDOWN)
        if understood:
            logging.info('Command {cmd} sucessfully executed')
        else:
            logging.error('Command {cmd} not executed')

    _kernel[name] = wrapper
    return wrapper


@is_command
def start(bot, update):
    '''Empezar a interactuar con este robot.
    '''
    return True, "Hola, soy tu robot asistente para el PyDay"


@is_command
def status(bot, update):
    '''Obtener información sobre el estado del bot.
    '''
    return True, "I'm ok, current version is {}".format(VERSION)


@is_command
def tags(bot, update):
    '''Listado de tags.
    '''
    return True, templates.render(
        'templates/tags.txt',
        tags=sorted(E.tags.keys())
        )


@is_command
def tag(bot, update, args):
    '''Charlas etiquetadas con un deterinado.
    '''
    tag = args[0].strip().lower()
    if tag in E.tags:
        return True, templates.render(
            'templates/tag.txt',
            talks=E.tags[tag],
            tag=tag,
            )
    else:
        return False, "No reconozco ese tag. El comando `/tags` te "  \
                      " mostrará las etiquetas disponibles."


@is_command
def track(bot, update, args):
    '''Listado de charlas de un track.
    '''
    is_valid, num_track = utils.as_integer(args[0])
    print('is_valid: {}, num_track: {}'.format(is_valid, num_track))
    if is_valid and E.is_valid_track(num_track):
        track = E.tracks[num_track-1]
        text = templates.render(
            'templates/track.txt',
            num_track=num_track,
            track=track,
            talks=track.talks,
            )
        return True, str(text)
    else:
        return False, "Necesito un número entre 1 y {}".format(E.num_tracks)


@is_command
def tracks(bot, update):
    '''Lista de tracks del evento.
    '''
    text = """\
Hay 3 tracks en este evento:

 - Track *1*: *Tatooine*
 - Track *2*: *Hoth*
 - Track *3*: *Dagobah*

Si quieres obtener más información de cada track puedes user `/track <num>`.
Por ejemplo, `/track 1` para ver las charlas del track Tatooine.\
"""
    return True, text


@is_command
def help(bot, update):
    '''Listado de ordenes disponibles.
    '''
    global _kernel
    buff = ['Opciones:\n']
    for name in _kernel:
        buff.append('/{} - {}'.format(
            name, 
            _kernel[name].__doc__.strip()
            ))
    return True, '\n'.join(buff)


def no_entiendo(bot, update):
    '''Handler especial para tratar casos de comandos mal escritos.

    Se codifica aparte para que no aparezca en el menú de ayuda.
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=emojize(
            ":confused: Lo siento, no entiendo esa orden",
            use_aliases=True,
            ),
        parse_mode=MARKDOWN,
        )


if __name__ == '__main__':
    logging.info('Obteniendo informacion del evento')
    E = Event(config('EVENT_TAG'))
    logging.info('OK, evento cargado')
    updater = Updater(config("TELEGRAM_BOT_TOKEN"))
    logging.info('PtDayBot starts')
    dispatcher = updater.dispatcher
    for name in _kernel:
        functor = _kernel[name]
        sig = inspect.signature(functor)
        if len(sig.parameters) == 2:
            cmd_handler = CommandHandler(name, functor)
        else:
            cmd_handler = CommandHandler(name, functor, pass_args=True)
        dispatcher.add_handler(cmd_handler)

    # No hemos capturado ningún comando anes, debe estar mal escrito
    dispatcher.add_handler(
        MessageHandler(Filters.command, no_entiendo)
        )
    updater.start_polling()
    updater.idle()
