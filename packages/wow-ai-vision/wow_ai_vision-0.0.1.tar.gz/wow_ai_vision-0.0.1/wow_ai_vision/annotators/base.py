from abc import ABC, abstractmethod

import numpy as np

from wow_ai_vision.detection.core import Detections


class BaseAnnotator(ABC):
    @abstractmethod
    def annotate(self, scene: np.ndarray, detections: Detections) -> np.ndarray:
        pass
