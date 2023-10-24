# cython: language_level=3

from .exceptions cimport UnsupportedExtensionError, check_al_error
from . cimport al, alc

cdef class EventsExtension:
    def __cinit__(self):
        if al.alIsExtensionPresent(b"AL_SOFT_EVENTS") == al.AL_FALSE:
            check_al_error()
            raise UnsupportedExtensionError("ALC_SOFT_EVENTS")
