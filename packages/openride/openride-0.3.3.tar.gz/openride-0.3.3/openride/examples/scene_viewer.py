import openride as ride


def main():

    viewer = ride.Viewer()

    viewer.camera.set_position_xyz(-10, 0, 6)
    viewer.camera.set_focus_xyz(4, 0, 0)

    viewer.hud.toggle_fps_count()
    viewer.hud.toggle_cursor_position()

    viewer.draw_grid(delta=5, extent=50)
    viewer.draw_grid(delta=1, alpha=0.3, extent=50)

    point = ride.Point()

    bounding_box = ride.BoundingBox(
        position=ride.Point(5, 4, 1),
        rotation=ride.Rotation(0, 0, 1),
        size=ride.Size(2, 1, 1),
    )

    polyline = ride.Polyline([ride.Point(x + 2, -3) for x in range(10)])

    polygon = ride.Polygon([ride.Point(7, 1), ride.Point(2, 1), ride.Point(3, -1), ride.Point(7, -1, 0.3)])

    while True:
        viewer.draw_point(point, persist=False)
        viewer.labelize("allo", point)
        viewer.draw_bounding_box(bounding_box, color=(0, 1, 0), alpha=0.35)
        viewer.draw_model(ride.Category.Vehicle, bounding_box, color=(0,0,1))
        viewer.draw_polyline(polyline, color=(1, 0, 1), linewidth=3, points_size=10)
        viewer.draw_polygon(polygon, color=(1, 0, 0), alpha=0.7)
        viewer.update()


if __name__ == "__main__":
    main()
