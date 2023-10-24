from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.numba import transform_matrix, transform_inverse_matrix

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Transform:

    translation: Point = field(default_factory=Point)
    rotation: Rotation = field(default_factory=Rotation)

    def get_matrix(self) -> np.ndarray:
        return transform_matrix(
            self.translation.x,
            self.translation.y,
            self.translation.z,
            self.rotation.roll,
            self.rotation.pitch,
            self.rotation.yaw,
        )

    def get_inverse_matrix(self) -> np.ndarray:
        return transform_inverse_matrix(
            self.translation.x,
            self.translation.y,
            self.translation.z,
            self.rotation.roll,
            self.rotation.pitch,
            self.rotation.yaw,
        )

    def inverse(self) -> "Transform":
        return Transform.from_matrix(self.get_inverse_matrix())

    @classmethod
    def from_matrix(cls, matrix: np.ndarray) -> "Transform":
        return cls(Point(*matrix[:3, 3]), Rotation.from_matrix(matrix))
    
    @classmethod
    def from_6dof(cls, 
                  x:float=0.0, y:float=0.0, z:float=0.0, 
                  roll:float=0.0, pitch:float=0.0, yaw:float=0.0, 
        ) -> 'Transform':
        return cls(Point(x, y, z), Rotation(roll, pitch, yaw))
