# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
"""QP exceptions"""


class QPError(Exception):
    """Base class for errors raised by M3."""

    def __init__(self, *message):
        """Set the error message."""
        super().__init__(' '.join(message))
        self.message = ' '.join(message)

    def __str__(self):
        """Return the message."""
        return repr(self.message)
