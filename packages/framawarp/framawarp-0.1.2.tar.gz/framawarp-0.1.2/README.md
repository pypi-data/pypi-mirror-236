# framawarp

<div align="center">
  <p>
    <a align="center" href="" target="_blank">
      <img
        width="50%"
        src="resources/logo.png"
      >
    </a>
  </p>
</div>

## Description

`framawarp` is a Python library designed to simplify image manipulation tasks in computer vision projects. It provides a unified interface for wrapping NumPy arrays and PyTorch tensors, making it easy to work with images and perform operations such as color space conversions.

## Installation

To install framawarp, run the following command:

```bash
pip install framawarp
```

## Usage

### Creating a Frame

You can create a `Frame` object by wrapping a NumPy array or a PyTorch tensor:

```python
import numpy as np
from framawarp import Frame

image = np.random.rand(256, 256, 3)  # Example NumPy array
frame = Frame(image)
```

### Manipulating Color Spaces

framawarp makes it easy to convert between different color spaces:

```python
from framawarp import FrameColorSpace

# Convert from RGB to BGR
frame_bgr = frame.cast_color_space(FrameColorSpace.BGR)

# Convert from RGB to HSV with new frame
frame_hsv = frame.cast_color_space(FrameColorSpace.HSV, inplace=False)
```

## Contributing

While we are not actively seeking contributions at the moment, we are always open to suggestions and improvements. Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please feel free to reach out to the maintainer.
