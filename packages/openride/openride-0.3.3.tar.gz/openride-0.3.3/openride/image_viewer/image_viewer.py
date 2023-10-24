from openride import Point, BoundingBox, PointCloud, BoundingBoxCollection, Polyline

import cv2
import numpy as np

from typing import List, Tuple, Union



class ImageViewer:
    def __init__(
        self, title: str = "Openride Image Viewer", camera_matrix: np.ndarray = np.eye(3), distortion: List[float] = []
    ):
        self.title = title
        self.camera_matrix = camera_matrix
        self.distortion = distortion

        cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
        cv2.setMouseCallback(title, self.mouse_callback)

        self.display = None

    def set_window_size(self, size:Tuple[int, int]):
        cv2.resizeWindow(self.title, size[0], size[1])

    def update(self):
        if self.display is None:
            return
        cv2.imshow(self.title, self.display[..., ::-1])
        cv2.waitKey(1)

    def draw_image(self, image: np.ndarray):
        self.display = image / 256


    def draw_point(self, point: Point, color: tuple = (1, 1, 1), size: int = 3, alpha:float=1.0):

        if point.z < 0:
            return
        
        point2d = self.__project_points(np.array((point.x, point.y, point.z))).astype(int)

        if alpha >= 1.0:
            for p in point2d:
                cv2.circle(self.display, p, size, color, -1)

        elif alpha > 0.0:
            tmp = np.zeros_like(self.display)
            for p in point2d:
                cv2.circle(tmp, p, size, color, -1)
            mask = tmp.astype(bool)
            self.display[mask] = cv2.addWeighted(self.display, 1-alpha, tmp, alpha, 0)[mask]


    def labelize(self, label: str, pos: Point, color: tuple = (1,1,1), fontsize: float = 1.0, linewidth:int=1):
        point2d = self.__project_points(np.array((pos.x, pos.y, pos.z))).astype(int)
        if point2d.size == 0:
            return
        self.display = cv2.putText(self.display, label, point2d[0], cv2.FONT_HERSHEY_SIMPLEX, fontsize, color, linewidth)


    def draw_rectangle(self, xmin:float, ymin:float, xmax:float, ymax:float, color:tuple=(1,1,1), linewidth:int=1, fill:bool=False, alpha:float=1.0):
        _linewidth = linewidth if not fill else -1 * linewidth
        if alpha >= 1.0:
            self.display = cv2.rectangle(self.display, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, _linewidth)
        elif alpha > 0.0:
            tmp = np.zeros_like(self.display)
            tmp = cv2.rectangle(tmp, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, _linewidth)
            mask = tmp.astype(bool)
            self.display[mask] = cv2.addWeighted(self.display, 1-alpha, tmp, alpha, 0)[mask]


    def draw_point_cloud(
        self,
        pcloud: PointCloud,
        color: tuple = (1, 1, 1),
        alpha: float = 1.0,
    ):
        mask = np.where(pcloud.get_point_cloud()[:, 2] > 0.0)[0]
        points2d = self.__project_points(pcloud.get_point_cloud()[mask]).astype(int)

        points2d = points2d[np.where(points2d[:,0] >= 0)]
        points2d = points2d[np.where(points2d[:,1] >= 0)]
        points2d = points2d[np.where(points2d[:,0] < self.display.shape[1]-1)]
        points2d = points2d[np.where(points2d[:,1] < self.display.shape[0]-1)]

        if alpha >= 1.0:
            self.display[points2d[:,1], points2d[:,0]] = color
        elif alpha > 0.0:
            tmp = np.zeros_like(self.display)
            tmp[points2d[:,1], points2d[:,0]] = color
            mask = tmp.astype(bool)
            self.display[mask] = cv2.addWeighted(self.display, 1-alpha, tmp, alpha, 0)[mask]


    def draw_bounding_box(
        self,
        bounding_box: Union[BoundingBox, BoundingBoxCollection],
        color: tuple = (1, 1, 1),
        linewidth: int = 2,
        alpha: float = 1.0,
    ):
        if isinstance(bounding_box, BoundingBoxCollection):
            [self.draw_bounding_box(box, color, linewidth, alpha) for box in bounding_box]
            return

        lines = np.array(self.__get_box_projection(bounding_box))

        if alpha >= 1.0:    
            cv2.polylines(self.display, lines, False, color, linewidth)
        elif alpha > 0.0:
            tmp = np.zeros_like(self.display)
            cv2.polylines(tmp, lines, False, color, linewidth)
            mask = tmp.astype(bool)
            self.display[mask] = cv2.addWeighted(self.display, 1-alpha, tmp, alpha, 0)[mask]


    def draw_polyline(
        self,
        line: Polyline,
        color: tuple = (1, 1, 1),
        linewidth: int = 2,
        alpha :float = 1.0,
    ):
                
        if len(line) < 2:
            return
        
        for i in range(len(line)-1):
            if np.sign(line[i].z) != np.sign(line[i+1].z):
                new_line = Polyline([line[i], line[i+1]]).resample(1)
                new_line.vertices = new_line.vertices[np.where(new_line.vertices[:, 2] > 0.0)[0]]
                self.draw_polyline(new_line, color, linewidth, alpha)

        mask = np.where(line.vertices[:, 2] > 0.0)[0]
        if mask.shape[0] < 2:
            return
        points2d = self.__project_points(line.vertices[mask]).astype(int)

        if alpha >= 1.0:
            cv2.polylines(self.display, [points2d.reshape((-1, 1, 2))], False, color, linewidth)
        elif alpha > 0.0:
            tmp = np.zeros_like(self.display)
            cv2.polylines(self.display, [points2d.reshape((-1, 1, 2))], False, color, linewidth)
            mask = tmp.astype(bool)
            self.display[mask] = cv2.addWeighted(self.display, 1-alpha, tmp, alpha, 0)[mask]


    def mouse_callback(self, event, x, y, *_):
        pass

    def close(self):
        cv2.destroyWindow(self.title)

    def __project_points(self, points: np.ndarray) -> np.ndarray:
        if points.shape[0] == 0:
            return np.empty((0, 2))
        R = T = np.zeros((3, 1))
        pts2d, _ = cv2.projectPoints(
            points.astype(float), R, T, self.camera_matrix, np.array(self.distortion)
        )
        return pts2d[:, 0, :]

    def __get_box_projection(self, box: BoundingBox) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:

        lines: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        vertices = box.get_vertices()
        mask = vertices[:, 2] >= 0
        pts2d = self.__project_points(vertices)

        indices = [6, 7, 7, 1, 1, 0, 0, 6, 4, 5, 5, 3, 3, 2, 2, 4, 6, 4, 7, 5, 0, 2, 1, 3]
        for i in range(0, len(indices) - 1, 2):
            if not mask[indices[i]] or not mask[indices[i + 1]]:
                continue
            p1 = tuple(pts2d[indices[i]].astype(int))
            p2 = tuple(pts2d[indices[i + 1]].astype(int))
            lines.append((p1, p2))
        return lines
    

    def set_camera_matrix(self, matrix:np.ndarray):
        self.camera_matrix = matrix

    def set_fov(self, resolution:Tuple[int, int], fov_degrees:float):
        matrix = np.identity(3)
        matrix[0,2] = resolution[0]/2
        matrix[1,2] = resolution[1]/2
        matrix[0,0] = matrix[1,1] = resolution[0]/(2*np.tan(fov_degrees * np.pi / 360.0))
        self.set_camera_matrix(matrix)
