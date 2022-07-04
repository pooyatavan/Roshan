import logging
import platform
import ctypes
import ctypes.util

class _AnsiColorStreamHandler(logging.StreamHandler):
    DEFAULT = '\x1b[0m'
    RED     = '\x1b[31m'
    GREEN   = '\x1b[32m'
    YELLOW  = '\x1b[33m'
    CYAN    = '\x1b[36m'

    CRITICAL = RED
    ERROR    = RED
    WARNING  = YELLOW
    INFO     = GREEN
    DEBUG    = CYAN

    def __init__(self, stream=None):
        super().__init__(stream)

    def format(self, record):
        text = super().format(record)
        color = self._get_color_code(record.levelno)
        return color + text + self.DEFAULT

    @classmethod
    def _get_color_code(cls, level):
        if level >= logging.CRITICAL:
            return cls.CRITICAL
        elif level >= logging.ERROR:
            return cls.ERROR
        elif level >= logging.WARNING:
            return cls.WARNING
        elif level >= logging.INFO:
            return cls.INFO
        elif level >= logging.DEBUG:
            return cls.DEBUG
        else:
            return cls.DEFAULT

class _WinColorStreamHandler(logging.StreamHandler):
    STD_INPUT_HANDLE     = -10
    STD_OUTPUT_HANDLE    = -11
    STD_ERROR_HANDLE     = -12

    FOREGROUND_BLACK     = 0x0000
    FOREGROUND_BLUE      = 0x0001
    FOREGROUND_GREEN     = 0x0002
    FOREGROUND_CYAN      = 0x0003
    FOREGROUND_RED       = 0x0004
    FOREGROUND_MAGENTA   = 0x0005
    FOREGROUND_YELLOW    = 0x0006
    FOREGROUND_GREY      = 0x0007
    FOREGROUND_INTENSITY = 0x0008
    FOREGROUND_WHITE     = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED

    BACKGROUND_BLACK     = 0x0000
    BACKGROUND_BLUE      = 0x0010
    BACKGROUND_GREEN     = 0x0020
    BACKGROUND_CYAN      = 0x0030
    BACKGROUND_RED       = 0x0040
    BACKGROUND_MAGENTA   = 0x0050
    BACKGROUND_YELLOW    = 0x0060
    BACKGROUND_GREY      = 0x0070
    BACKGROUND_INTENSITY = 0x0080

    DEFAULT  = FOREGROUND_WHITE
    CRITICAL = FOREGROUND_RED | FOREGROUND_INTENSITY
    ERROR    = FOREGROUND_RED | FOREGROUND_INTENSITY
    WARNING  = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
    INFO     = FOREGROUND_GREEN
    DEBUG    = FOREGROUND_CYAN

    def __init__(self, stream=None):
        super().__init__(stream)
        self.output_handle = self._get_output_handle(stream)

    @classmethod
    def _get_output_handle(cls, stream):
        if stream is None:
            return ctypes.windll.kernel32.GetStdHandle(cls.STD_OUTPUT_HANDLE)
        else:
            msvcrt_loc = ctypes.util.find_msvcrt()
            msvcrt_lib = ctypes.cdll.LoadLibrary(msvcrt_loc)
            return msvcrt_lib._get_osfhandle(stream.fileno())

    def emit(self, record):
        color_code = self._get_color_code(record.levelno)
        self._set_color_code(color_code)
        super().emit(record)
        self._set_color_code(self.FOREGROUND_WHITE)

    @classmethod
    def _get_color_code(cls, level):
        if level >= logging.CRITICAL:
            return cls.CRITICAL
        elif level >= logging.ERROR:
            return cls.ERROR
        elif level >= logging.WARNING:
            return cls.WARNING
        elif level >= logging.INFO:
            return cls.INFO
        elif level >= logging.DEBUG:
            return cls.DEBUG
        else:
            return cls.DEFAULT

    def _set_color_code(self, code):
        ctypes.windll.kernel32.SetConsoleTextAttribute(self.output_handle, code)

if platform.system() == "Windows":
    ColorStreamHandler = _WinColorStreamHandler
else:
    ColorStreamHandler = _AnsiColorStreamHandler

_LOG_LEVEL   = logging.DEBUG
_FORMAT      = "%(asctime)s %(levelname)-8s %(message)s"
_DATE_FORMAT = "%H:%M:%S"

def get_logger( name="pyshgck", level=_LOG_LEVEL, log_format=_FORMAT, date_format=_DATE_FORMAT, into_stderr=True, into_log_file=None ):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    if into_stderr:
        stream_handler = ColorStreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if into_log_file is not None:
        file_handler = logging.FileHandler(into_log_file, mode="w")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
