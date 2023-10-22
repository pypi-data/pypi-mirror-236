from framawarp import FrameColorSpace


class FrameException(Exception):
    """Base class for exceptions in this module."""

    default_message = "An error occurred about frame."

    def __init__(self, message=None):
        """Initialize VideoStreamException.

        Args:
            message: Exception message.
        """
        super().__init__(message)


class UnsupportedColorSpaceConversion(FrameException):
    """Exception raised when color space conversion is not supported."""

    def __init__(self, from_color: FrameColorSpace, to_color: FrameColorSpace):
        """Initialize UnsupportedColorSpaceConversion.

        Args:
            from_color: Color space to convert from.
            to_color: Color space to convert to.
        """
        default_message = (
            f"Unsupported color space conversion from {from_color} to {to_color}"
        )

        super().__init__(default_message)
