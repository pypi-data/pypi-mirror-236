#  Copyright (c) 2023. Photonic Science and Engineering Ltd.
from __future__ import annotations

from abc import ABC, abstractmethod

from PSELPyBaseCamera._abcs_mixins import *  # noqa
from PSELPyBaseCamera.options import OptionSetterResult


class ColourMode(ABC):
    @abstractmethod
    def set_colour_mode(self, mode: str) -> OptionSetterResult:
        raise NotImplementedError()

    def set_color_mode(self, mode: str) -> OptionSetterResult:
        return self.set_colour_mode(mode)


class DeviceCameraMixin(
    AcquisitionABC,
    CameraNameMixin,
    CameraOptionsMixin,
    CameraTypeMixin,
    ColourMode,
    ConnectionABC,
    CoreCamera,
    ExposureABC,
    ImageModeABC,
    SizeABC,
    UpdateSizesMixin,
):
    pass
