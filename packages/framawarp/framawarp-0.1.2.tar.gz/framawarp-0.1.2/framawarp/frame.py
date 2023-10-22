import copy
import types
from typing import Final

import cv2
import numpy as np
import torch

from framawarp import FrameColorSpace
from framawarp.exceptions import UnsupportedColorSpaceConversion

COLOR_CONVERSIONS: Final = types.MappingProxyType(
    {
        (FrameColorSpace.RGB, FrameColorSpace.BGR): cv2.COLOR_RGB2BGR,
        (FrameColorSpace.RGB, FrameColorSpace.HSV): cv2.COLOR_RGB2HSV,
        (FrameColorSpace.BGR, FrameColorSpace.RGB): cv2.COLOR_BGR2RGB,
        (FrameColorSpace.BGR, FrameColorSpace.HSV): cv2.COLOR_BGR2HSV,
        (FrameColorSpace.HSV, FrameColorSpace.RGB): cv2.COLOR_HSV2RGB,
        (FrameColorSpace.HSV, FrameColorSpace.BGR): cv2.COLOR_HSV2BGR,
    }
)


class Frame:
    """Frame class."""

    def __init__(self, image: np.ndarray, color_space: FrameColorSpace):
        """Initialize Frame.

        Args:
            image: Image.
            color_space: Color space.
        """
        self._image: np.ndarray = image
        self.color_space: FrameColorSpace = color_space

    def cast_color_space(self, color_space: FrameColorSpace) -> None:
        """Cast color space.

        Args:
            color_space: Color space.
        """
        try:
            conversion = COLOR_CONVERSIONS[(self.color_space, color_space)]
            self._image = cv2.cvtColor(self._image, conversion)
            self.color_space = color_space
        except KeyError:
            raise UnsupportedColorSpaceConversion(self.color_space, color_space)

    def copy(self) -> "Frame":
        """Copy frame.

        Returns:
            Copied frame.
        """
        return Frame(
            image=self._image.copy(),
            color_space=self.color_space,
        )

    def deepcopy(self) -> "Frame":
        """Deep copy frame.

        Returns:
            Deep copied frame.
        """
        return Frame(
            image=copy.deepcopy(self._image),
            color_space=copy.copy(self.color_space),
        )

    def __eq__(self, __value: object) -> bool:
        """Compare two frames.

        Args:
            __value: Value to compare.

        Returns:
            True if two frames are equal, False otherwise.
        """
        if not isinstance(__value, Frame):
            return False

        return np.array_equal(self._image, __value._image)

    def image(
        self, color_space: FrameColorSpace = FrameColorSpace.RGB, inplace: bool = True
    ) -> np.ndarray:
        """Get image in specified color space.

        Args:
            color_space: Color space.
            inplace: Whether to convert image inplace.

        Returns:
            Image.
        """
        if self.color_space == color_space:
            return self._image

        # We know that the color space is different from the current one.
        # If inplace is True, we convert the image in place and return it.
        if inplace:
            self.cast_color_space(color_space)
            return self._image

        # If inplace is False, we copy the image and convert it.
        image = self._image.copy()
        image = cv2.cvtColor(image, COLOR_CONVERSIONS[(self.color_space, color_space)])
        return image

    def tensor(
        self,
        device: torch.device,
        color_space: FrameColorSpace = FrameColorSpace.RGB,
        inplace: bool = True,
        half: bool = False,
    ) -> torch.Tensor:
        """Get image as tensor.

        Args:
            device: Device.

        Returns:
            Image as tensor.
        """
        tensor: torch.Tensor = torch.from_numpy(
            self.image(color_space=color_space, inplace=inplace)
        ).to(device)

        tensor = tensor.half() if half else tensor.float()
        return tensor

    @property
    def shape(self) -> tuple:
        """Get frame shape.

        Returns:
            Frame shape.
        """
        return self._image.shape

    @property
    def height(self) -> int:
        """Get frame height.

        Returns:
            Frame height.
        """
        return self._image.shape[0]

    @property
    def width(self) -> int:
        """Get frame width.

        Returns:
            Frame width.
        """
        return self._image.shape[1]

    @property
    def channels(self) -> int:
        """Get frame channels.

        Returns:
            Frame channels.
        """
        return self._image.shape[2]

    def to_dict(self) -> dict:
        """Get dictionary representation.

        Returns:
            Dictionary representation.
        """
        return {
            "image": self._image.tolist(),
            "color_space": self.color_space.value,
        }

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            String representation.
        """
        return f"Frame(shape={self.shape}, color_space={self.color_space})"

    @classmethod
    def from_dict(cls, frame_data: dict) -> "Frame":
        """Create Frame from dictionary.

        Args:
            data: Dictionary.

        Returns:
            Frame.
        """
        return cls(
            image=np.array(frame_data["image"], dtype=np.uint8),
            color_space=FrameColorSpace(frame_data["color_space"]),
        )

    @classmethod
    def converted(cls, frame: "Frame", color_space: FrameColorSpace) -> "Frame":
        """Create converted Frame.

        Args:
            frame: Frame.
            color_space: Color space.

        Returns:
            Converted Frame.
        """
        converted_frame = frame.copy()
        converted_frame.cast_color_space(color_space)
        return converted_frame
