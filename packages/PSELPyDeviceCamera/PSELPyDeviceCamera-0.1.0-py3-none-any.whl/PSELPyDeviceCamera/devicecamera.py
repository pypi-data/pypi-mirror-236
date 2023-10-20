from __future__ import annotations

import logging
from pathlib import Path
from typing import Union

import cv2
import numpy as np
from PSELPyBaseCamera.helper import *
from PSELPyBaseCamera.image_modes import ImageMode, image_mode_to_string
from PSELPyBaseCamera.options import OptionSetterResult

from ._devicecamera_mixin import DeviceCameraMixin

# from PSELBaseCamera import CameraInterface
# from PSELBaseCamera.helper import *
# from PSELBaseCamera.image_modes import ImageMode, image_mode_to_string
# from PSELBaseCamera.logging_tools import log_this_function

_logger = logging.getLogger(__name__)


class DeviceCamera(DeviceCameraMixin):
    def __init__(
        self, _current_working_directory: Union[Path, str], name="DeviceCamera"
    ):
        self._name = name
        self._current_working_directory = Path(
            _current_working_directory
        )  # Path to camera folder
        self._camera_directory = Path(
            self._current_working_directory, self._name
        ).resolve()

        self._dll_path = Path("")
        self.dll = None

        self._mode = ImageMode.RGB
        self._sizemax = (2048, 1280)
        self._size = self._sizemax
        self._grey_mode = False
        self._frame = None
        self._device_id = 0

    def reset_options(self):
        self.colour_mode = image_mode_to_string(self.image_mode())
        self._state = 0
        self.abort_flag = False

        self._camera_options = [
            {
                "name": f"{self.name} settings",
                "type": "group",
                "children": [
                    {
                        "name": "exposure",
                        "title": "Exposure",
                        "type": "int",
                        "value": 1,
                        "dec": True,
                        "step": 1,
                        "minStep": 1,
                        "siPrefix": True,
                        "suffix": "Level",
                        "limits": (5, 16383),
                        "decimals": 10,
                    },
                    {
                        "name": "Camera Mode",
                        "type": "group",
                        "children": [
                            {
                                "name": "colour_mode",
                                "title": "Colour Mode",
                                "type": "list",
                                "limits": [
                                    "RGB",
                                    "BGR",
                                    "GRAY",
                                ],
                                "value": "RGB",
                            },
                        ],
                    },
                ],
            }
        ]

        self._set_camera_option_routing_dict = {
            "exposure": self.set_exposure,
            "colour_mode": self.set_colour_mode,
        }

        self._get_camera_option_routing_dict = {}

        self._device_id, self.def_size, self.sync = self._get_config()

    def _get_config(self) -> tuple[int, tuple[int, int], int]:
        """Read the device configuration from deviceid.dat.

        Returns:
            tuple of: device id, image size, and sync
        """
        path = Path(self._camera_directory, "deviceid.dat").resolve()

        id_dev = 0
        size = (800, 600)
        sync = 0

        if not path.exists():
            return id_dev, size, sync

        with path.open("r") as f:
            lines = f.readlines()

        for line in lines:
            words = line.split("=")
            if len(words) == 2:
                if words[0].strip() == "id":
                    try:
                        id_dev = int(words[1].strip())
                    except:
                        pass
                elif words[0].strip() == "size":
                    from ast import literal_eval

                    try:
                        size = literal_eval(words[1].strip())
                        size = (int(size[0]), int(size[1]))
                    except:
                        pass
                elif words[0].strip() == "sync":
                    try:
                        sync = int(words[1].strip())
                    except:
                        pass

        return id_dev, size, sync

    """Properties"""

    @property
    def name(self) -> str:
        """Name of the camera.

        Returns:
            name of the camera
        """
        return self._name

    @property
    def size(self) -> tuple[int, int]:
        """Size of image currently set in the driver.

        Returns:
            size of images
        """
        return self._size

    @property
    def size_max(self) -> tuple[int, int]:
        """Maximum size image the sensor can output.

        Returns:
            maximum size of an image
        """
        return self._sizemax

    def image_mode(self) -> ImageMode:
        return self._mode

    def update_size_max(self) -> tuple[int, int]:
        return self.size_max

    def update_size(self) -> None:
        pass

    def open(self) -> bool:
        """Open and initialise the system.

        Returns:
            boolean indicating success
        """
        self.reset_options()

        self.cap = cv2.VideoCapture(self._device_id)
        if not self.cap.isOpened():
            if not self.cap.open(self._device_id):
                print("Cannot open camera device %s" % self._device_id)
                return False

        if self.def_size is not None:
            self._sizemax = self._size = self.def_size
            self.cap.set(3, self.size[0])
            self.cap.set(4, self.size[1])
        else:
            self._sizemax = self._size = (self.cap.get(3), self.cap.get(4))

        return True

    def close(self) -> bool:
        """Close connection."""
        self.cap.release()
        return True

    def snap(self) -> bool:
        """Acquire an image. This function will block for the duration of the exposure
        time.

        If syncing is enabled acquire and throw out an image to ensure the returned
        image's exposure began after the snap request was sent.

        the image can be read out with
        :py:meth:`PyDeviceCamera.DeviceCamera.get_image_pointer`,
        :py:meth:`PyDeviceCamera.DeviceCamera.get_image` or
        :py:meth:`PyDeviceCamera.DeviceCamera.get_raw_image`.


        Returns:
            acquisition success or failure
        """
        self._state = 1
        self.abort_flag = False

        # If we are syncing acquire and throw out an image to ensure the returned
        # image's exposure began after the snap request was sent
        if self.sync:
            self.cap.read()

        rep, self._frame = self.cap.read()
        self._size = self._size_max = self._frame.shape[1], self._frame.shape[0]
        self._state = 0

        return rep

    def snap_and_return(self) -> bool:
        """Acquire an image.

        Unlike other PSEL cameras when using this function the camera will block when
        this function is called as the camera does not support non-blocking acquisition.

        .. warning:: this function does not support fusion acquisitions.

        Returns:
            snap success or failure
        """
        self.abort_flag = False
        rep, self._frame = self.cap.read()
        self._size = self._sizemax = self._frame.shape[1], self._frame.shape[0]
        return rep

    def get_status(self) -> bool:
        """This function will always return ``True`` as the camera does not support
        non-blocking image acquisition (see
        :py:meth:`PyDeviceCamera.DeviceCamera.snap_and_return` for details).
        """
        return True

    def abort_snap(self) -> bool:
        self.abort_flag = True
        return True

    def get_image_pointer(self) -> np.ndarray:
        """Unlike other PSEL cameras this function does not return a C-pointer to the
        current image, it instead returns the image itself in a numpy array.

        Returns:
            current image numpy array
        """
        return self._frame.copy()

    def get_raw_image(self) -> tuple[tuple[int, int], np.ndarray]:
        """Return the image size and a numpy array of the image data.

        This function will not apply any corrections or other operations on the image.

        Returns:
            image size, image data

        """
        imp = self.get_image_pointer()
        (Ny, Nx) = imp.shape[0:2]
        return (Nx, Ny), imp

    def get_image(self, imp=None, tsize=None) -> tuple[tuple[int, int], np.ndarray]:
        if imp is None:
            imp = self.get_image_pointer()

        if tsize is None:
            (Ny, Nx) = imp.shape[0:2]
        else:
            (Nx, Ny) = tsize

        if self.colour_mode == "GRAY":
            if len(imp.shape) >= 3:
                imp = cv2.cvtColor(imp, cv2.COLOR_BGR2GRAY)
        elif self.colour_mode == "BGR":
            if len(imp.shape) >= 3:
                imp = cv2.cvtColor(imp, cv2.COLOR_BGR2RGB)

        return (Nx, Ny), imp

    def set_exposure(self, expo: int, unit="Level") -> OptionSetterResult:
        # if unit in "Level":
        return _map_result_to_enum(self.cap.set(15, -expo))

    def set_colour_mode(self, mode) -> OptionSetterResult:
        if mode == "RGB":
            self.colour_mode = mode
            self._mode = ImageMode.RGB
            return OptionSetterResult.COMPLETED
        elif mode == "BGR":
            self.colour_mode = mode
            self._mode = ImageMode.RGB
            return OptionSetterResult.COMPLETED
        elif mode == "GRAY":
            self.colour_mode = mode
            self._mode = ImageMode.L
            return OptionSetterResult.COMPLETED
        else:
            return OptionSetterResult.FAILED
