import logging
from threading import Event
import signal

from .version import __version__
from ._logging import screenFMT
from .utils.checkCLI import checkCLI

# Check for required CLIs
for cli in ['ffmpeg', 'mediainfo']:
  checkCLI( cli )

__doc__     = "Collection of utilities to manipulate video files; " + \
  "namely transcoding, subtitle extraction, audio aligning/downmixing, "+\
  "and metadata editing."


# Set up the logger for the module
log = logging.getLogger( __name__ );                                          # Get root logger based on package name
log.setLevel(logging.DEBUG);                                                  # Set root logger level to debug
log.addHandler( logging.StreamHandler() );
log.handlers[0].setFormatter( screenFMT['formatter'] )
log.handlers[0].setLevel( screenFMT['level'] );            # Set the format tot the screen format
log.handlers[0].set_name( screenFMT['name'] );

# Set up event and link event set to SIGINT and SIGTERM
_sigintEvent  = Event()
_sigtermEvent = Event()

def _handle_sigint(*args, **kwargs):
  _sigintEvent.set()
  log.error('Caught interrupt...')

def _handle_sigterm(*args, **kwargs):
  _sigtermEvent.set()
  log.error('Caught terminate...')

def isRunning():
  return (not _sigintEvent.is_set()) and (not _sigtermEvent.is_set())

signal.signal(signal.SIGINT,  _handle_sigint)
signal.signal(signal.SIGTERM, _handle_sigterm)

del cli, screenFMT;
