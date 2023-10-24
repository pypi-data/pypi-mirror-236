import time
import vtk

from typing import Any


class Hud:
    def __init__(self, viewer, position=(0, 0)):

        self.viewer = viewer
        self.viewer.set_callback(self.update)
        self.position = position
        self.time = time.perf_counter()
        self._elements = {}

        self.text = vtk.vtkTextActor()
        self.text.SetPosition(self.position[0], self.position[1])
        self.text.GetTextProperty().SetFontSize(16)
        self.viewer.renderer.AddActor(self.text)

        self.fps_count: bool = False
        self.cursor_position: bool = False

    def update(self):
        if self.fps_count:
            self.add("fps", int(1 / (time.perf_counter() - self.time)))
        if self.cursor_position:
            cursor = self.viewer.interactor.get_cursor_in_world()
            self.add("cursor", f"x:{cursor.x:.3f}, y:{cursor.y:.3f}, z:{cursor.z:.3f}")
        text = ""
        for element in self._elements:
            text += f"{element}: {str(self._elements[element])}\n"
        self.text.SetInput(text)
        self.time = time.perf_counter()

    def toggle_fps_count(self):
        self.fps_count = not self.fps_count

    def toggle_cursor_position(self):
        self.cursor_position = not self.cursor_position

    def add(self, name:str, value:Any):
        self._elements[name] = str(value)
