from math import * # type: ignore
from manimlib import * # type: ignore
import numpy as np

RADIUS = 1.0
DOT_RADIUS = 0.02

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

        def float_key(f): return round(f, 2)

        z = ValueTracker(-RADIUS)

        axes_3d, sphere = group_3d = Group([
            ThreeDAxes(x_range=(-2,2), y_range=(-2,2), z_range=(-2,2)),
            Sphere(radius=RADIUS, resolution=(500, 500))
        ])

        axes_labels = axes_3d.get_axis_labels() # type: ignore

        sphere.set_color_by_gradient(RED, BLUE, GREEN, RED)
        data_points = sphere.data.copy()

        sphere.set_opacity(0.1)
        group_3d.move_to(LEFT * 3) # type: ignore

        z_map = {}
        for data_point in data_points:
            point = data_point['point']
            z_value = float_key(point[2].__float__()/RADIUS)
            if z_map.get(z_value) is None: z_map[z_value] = [data_point]
            else: z_map[z_value].append(data_point)

        axes2d = Axes(x_range=(-2,2), y_range=(-2,2))
        axes2d.move_to(RIGHT * 3) # type: ignore
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
            z_value = float_key(z.get_value().__float__() / RADIUS) # type: ignore
            if z_map.get(z_value) is None: return None

            sphere_arr = z_map[z_value]
            arr = np.zeros(len(z_map[z_value]), dtype=DotCloud.data_dtype)

            arr['point'] = [[p['point'][0], p['point'][1], p['point'][2]] for p in sphere_arr]
            arr['rgba'] = [p['rgba'] for p in sphere_arr]
            arr['radius'] = np.full((len(sphere_arr), 1), DOT_RADIUS)
            return arr

        number.add_updater(lambda n: n.set_value(z.get_value())) # type: ignore

        circle_2d = DotCloud()
        circle_2d.fix_in_frame()

        circle_3d = DotCloud()

        def updater(obj: Mobject):
            data = compute_data()
            if data is not None:
                obj.set_data(data)
                obj.move_to(axes2d)

        def updater_3d(obj: Mobject):
            data = compute_data()
            if data is not None:
                obj.set_data(data)
                obj.move_to(axes_3d)
                obj.shift([0, 0, z.get_value()]) # type: ignore

        self.add(axes_3d, sphere, axes2d, z_label, axes_labels, axes2d_labels, circle_2d, circle_3d)
            
        # self.play(FadeIn(axes),
        #           FadeIn(sphere),
        #           FadeIn(axes2d),
        #           FadeIn(z_label),
        #           FadeIn(axes_labels),
        #           FadeIn(axes2d_labels),
        #           FadeIn(circle_2d),
        #           FadeIn(circle_3d))   


        circle_2d.add_updater(updater)
        circle_3d.add_updater(updater_3d)
        self.play(z.animate.set_value(RADIUS), run_time=10)
        circle_2d.remove_updater(updater)
        circle_3d.remove_updater(updater_3d)

class HypersphereViz(ThreeDScene):
    def construct(self):
        self.camera.frame.set_euler_angles(phi=75 * DEGREES, theta=30 * DEGREES)
        quaternion = np.array([0.5, 0.5, 0.5, 0.5])
        quaternion = quaternion / np.linalg.norm(quaternion)

        scale = ValueTracker(1)

        sphere = Sphere(radius=1, resolution=(101, 51))
        original_point = sphere.data['point'].copy()

        def sphere_updater(s: Mobject): s.set_points(original_point * scale.get_value())
        sphere.add_updater(sphere_updater)

        axes = ThreeDAxes()
        axes.add_coordinate_labels()

        self.play(FadeIn(axes), FadeIn(sphere))
        self.play(scale.animate.set_value(2), run_time=2)
