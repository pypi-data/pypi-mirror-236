import numpy as np
import pytest
import torch

from framawarp.frame import Frame, FrameColorSpace, UnsupportedColorSpaceConversion


@pytest.fixture
def sample_rgb_image():
    return np.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
        ],
        dtype=np.uint8,
    )


@pytest.fixture
def sample_frame_rgb(sample_rgb_image: np.ndarray):
    return Frame(sample_rgb_image, FrameColorSpace.RGB)


def test_frame_color_space_enum():
    assert FrameColorSpace.RGB.value == 0
    assert FrameColorSpace.BGR.value == 1
    assert FrameColorSpace.HSV.value == 2


def test_frame_initialization(sample_frame_rgb: Frame, sample_rgb_image: np.ndarray):
    assert np.array_equal(
        sample_frame_rgb.image(FrameColorSpace.RGB, inplace=False), sample_rgb_image
    )
    assert sample_frame_rgb.color_space == FrameColorSpace.RGB


def test_frame_cast_color_space(sample_frame_rgb: Frame):
    sample_frame_rgb.cast_color_space(FrameColorSpace.BGR)
    assert sample_frame_rgb.color_space == FrameColorSpace.BGR

    with pytest.raises(UnsupportedColorSpaceConversion):
        sample_frame_rgb.cast_color_space(FrameColorSpace.BGR)


def test_frame_copy_and_deepcopy(sample_frame_rgb: Frame):
    frame_copy = sample_frame_rgb.copy()
    frame_deepcopy = sample_frame_rgb.deepcopy()

    assert frame_copy == sample_frame_rgb
    assert frame_deepcopy == sample_frame_rgb

    frame_copy._image[0, 0, 0] = 100
    assert frame_copy != sample_frame_rgb

    frame_deepcopy._image[0, 0, 0] = 100
    assert frame_deepcopy != sample_frame_rgb


def test_frame_properties(sample_frame_rgb: Frame):
    assert sample_frame_rgb.shape == (2, 3, 3)
    assert sample_frame_rgb.height == 2
    assert sample_frame_rgb.width == 3
    assert sample_frame_rgb.channels == 3


def test_frame_to_dict_and_from_dict(sample_frame_rgb: Frame):
    frame_dict = sample_frame_rgb.to_dict()
    frame_from_dict = Frame.from_dict(frame_dict)

    assert frame_from_dict == sample_frame_rgb


def test_frame_converted(sample_frame_rgb: Frame):
    converted_frame = Frame.converted(sample_frame_rgb, FrameColorSpace.BGR)
    assert converted_frame.color_space == FrameColorSpace.BGR
    assert converted_frame != sample_frame_rgb


def test_frame_eq_notinstance(sample_frame_rgb: Frame):
    not_a_frame: int = 1
    assert sample_frame_rgb != not_a_frame


def test_frame_image_inplace(sample_frame_rgb: Frame):
    sample_frame_bgr_image_not_inplace = sample_frame_rgb.image(
        FrameColorSpace.BGR, inplace=False
    )
    sample_frame_bgr_image_inplace = sample_frame_rgb.image(
        FrameColorSpace.BGR, inplace=True
    )

    assert np.array_equal(
        sample_frame_bgr_image_not_inplace, sample_frame_bgr_image_inplace
    )


def test_frame_tensor(sample_frame_rgb: Frame):
    sample_frame_rgb_tensor = sample_frame_rgb.tensor(
        device=torch.device("cpu"), color_space=FrameColorSpace.RGB, inplace=True
    )

    assert sample_frame_rgb_tensor.device == torch.device("cpu")
    assert sample_frame_rgb_tensor.dtype == torch.float32
    assert sample_frame_rgb_tensor.shape == (2, 3, 3)

    sample_frame_rgb_tensor_half = sample_frame_rgb.tensor(
        device=torch.device("cpu"),
        color_space=FrameColorSpace.RGB,
        inplace=True,
        half=True,
    )

    assert sample_frame_rgb_tensor_half.device == torch.device("cpu")
    assert sample_frame_rgb_tensor_half.dtype == torch.float16
    assert sample_frame_rgb_tensor_half.shape == (2, 3, 3)


def test_frame_str(sample_frame_rgb: Frame):
    assert (
        str(sample_frame_rgb)
        == "Frame(shape=(2, 3, 3), color_space=FrameColorSpace.RGB)"
    )
