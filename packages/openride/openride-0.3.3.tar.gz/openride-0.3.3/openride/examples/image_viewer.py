from openride import ImageViewer, BoundingBox

import numpy as np


if __name__ == "__main__":

    box = BoundingBox.from_raw(x=0, y=0, z=5, roll=0.3)

    v = ImageViewer()
    v.set_fov(resolution=(500, 500), fov_degrees=70)

    image = np.zeros((500, 500, 3)) * 255
    v.set_window_size(image.shape[:2])

    while True:

        box.rotation.pitch += 0.01

        v.draw_image(image)

        v.draw_bounding_box(box, linewidth=5, color=(0,1,0), alpha=0.5)

        v.labelize("allo", pos=box.position, color=(1,0,0), linewidth=2)

        v.draw_rectangle(20, 20, 480, 480, color=(0,0,1), linewidth=1, fill=True, alpha=0.1)

        v.update()
