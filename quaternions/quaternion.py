from math import * # type: ignore
from manimlib import * # type: ignore
import numpy as np

RADIUS = 1.0
DOT_RADIUS = 0.03

def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                     w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2])

class SphereViz(ThreeDScene):
    def construct(self):
        self.camera.frame.set_euler_angles(phi=45 * DEGREES, theta=0 * DEGREES)

        z = ValueTracker(-RADIUS)

        axes = ThreeDAxes(x_range=(-2,2), y_range=(-2,2), z_range=(-2,2))
        axes.move_to(LEFT * 3)
        axes_labels = axes.get_axis_labels()

        sphere = Sphere(radius=RADIUS, resolution=(301, 101))
        sphere.set_color_by_gradient(RED, BLUE, GREEN, RED)
        points = sphere.data.copy()
        sphere.move_to(axes)

        def float_key(f): return round(f, 2)

        map = {}
        for point in points:
            p = point['point']
            z_value = float_key(p[2].__float__())
            if map.get(z_value) is None: map[z_value] = [point]
            else: map[z_value].append(point)

        axes2d = Axes(x_range=(-2,2), y_range=(-2,2))
        axes2d.move_to(RIGHT * 3)
        axes2d_labels = axes2d.get_axis_labels()
        axes2d_labels.make_smooth()
        axes2d_labels.fix_in_frame()
        axes2d.fix_in_frame()

        _, number = z_label = VGroup(
            Text("z = "),
            DecimalNumber(
                0,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        z_label.fix_in_frame()
        z_label.arrange(RIGHT)
        z_label.move_to(UP * 3) # type: ignore

        def compute_data():
            z_value = float_key(z.get_value().__float__()) # type: ignore
            if map.get(z_value) is None: 
                print("fail", z_value)
                return None
            sphere_arr = map[z_value]
            arr = np.zeros(len(map[z_value]), dtype=DotCloud.data_dtype)
            arr['point'][:] = np.array([[p['point'][0], p['point'][1], np.float64(0.0)] for p in sphere_arr]).reshape((len(sphere_arr),3))
            arr['rgba'][:] = np.array([p['rgba'] for p in sphere_arr]).reshape((len(sphere_arr),4))
            arr['radius'][:] = np.array([DOT_RADIUS for _ in range(len(sphere_arr))]).reshape((len(sphere_arr), 1))
            return arr

        number.add_updater(lambda n: n.set_value(z.get_value())) # type: ignore

        new_circle = DotCloud()
        new_circle.fix_in_frame()
        new_circle.set_color(RED)
        new_circle.move_to(axes2d)

        def updater(obj: Mobject):
            data = compute_data()
            if data is not None:
                obj.set_data(data)
            obj.move_to(axes2d)
            
        self.play(FadeIn(axes),
                  FadeIn(sphere),
                  FadeIn(axes2d),
                  FadeIn(z_label),
                  FadeIn(axes_labels),
                  FadeIn(axes2d_labels))

        self.play(FadeIn(new_circle))

        new_circle.add_updater(updater)
        self.play(z.animate.set_value(RADIUS), run_time=10)
        sphere.remove_updater(updater)

class HypersphereViz(ThreeDScene):
    def construct(self):
        self.camera.frame.set_euler_angles(phi=75 * DEGREES, theta=30 * DEGREES)
        quaternion = np.array([0.5, 0.5, 0.5, 0.5])
        quaternion = quaternion / np.linalg.norm(quaternion)

        scale = ValueTracker(1)

        sphere = Sphere(radius=1, resolution=RESOLUTION)
        original_point = sphere.data['point'].copy()

        def sphere_updater(s: Mobject): s.set_points(original_point * scale.get_value())
        sphere.add_updater(sphere_updater)

        axes = ThreeDAxes()
        axes.add_coordinate_labels()

        self.play(FadeIn(axes), FadeIn(sphere))
        self.play(scale.animate.set_value(2), run_time=2)
