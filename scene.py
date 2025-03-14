from manim import *

class anim(Scene):
    def construct(self):
        inner_curve = ParametricFunction(
            lambda t: np.array([t, np.sqrt(t), 0]),
            t_range=[0, 4],
            color=BLUE
        )
        
        outer_curve = ParametricFunction(
            lambda t: np.array([t, t/2, 0]),
            t_range=[0, 4],
            color=RED
        )

        self.play(Create(inner_curve), Create(outer_curve), run_time=2)

class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2
        )
        self.wait()

class triangleGraphWithSlice(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-3, 3],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )

        def create_triangle_at_x(x):
            y_val = np.sqrt((36 - 9*x**2)/4)  # Calculate y value at x
            # Create vertices for isosceles right triangle
            t = (x+2) / 4
            color = interpolate_color(RED, YELLOW, t)
            Scolor = interpolate_color(BLUE, PURPLE, t)
            triangle = Polygon(
                [x, y_val, 0],      # Base point 1
                [x, 0, y_val],      # Peak point
                [x, -y_val, 0],     # Base point 2
                color=color,
                fill_opacity=0.5,
                stroke_color=Scolor,  # Add dark purple border
                stroke_width=8,
            )
            return triangle


        x_values = np.linspace(-2, 2, 100)  # Create 50 triangles from x=-2 to x=2
        triangles = VGroup(*[create_triangle_at_x(x) for x in x_values])

        def upper_ellipse(x):
            return np.sqrt((36 - 9*x**2)/4)

        def lower_ellipse(x):
            return -np.sqrt((36 - 9*x**2)/4)

        graph_top = axes.plot(upper_ellipse, x_range=[-2, 2], color=BLUE)
        graph_bot = axes.plot(lower_ellipse, x_range=[-2, 2], color=BLUE)
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        self.add(axes, labels)

        self.play(Create(graph_top), Create(graph_bot), run_time=2)
        self.play(Create(triangles), run_time=5)

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=0, theta=-90*DEGREES)

        sample_triangle = create_triangle_at_x(0)

        target_triangle = sample_triangle.copy()
        #target_triangle.shift(4*RIGHT)

        self.play(
            FadeIn(sample_triangle),
            triangles.animate.set_opacity(0),
        )

        #self.play(Transform(sample_triangle, target_triangle),run_time=2)

        self.wait()
        
        #self.play(triangles.animate.set_opacity(0))
    
        self.move_camera(phi=80*DEGREES, theta=0)

        # Create y-axis label in the same plane as the triangle
        #y_text = Text("y").scale(0.7)
        #y_text.rotate_about_origin(90*DEGREES)
        #y_text.rotate(90*DEGREES)  # Rotate to match camera angle
        #y_text.next_to(sample_triangle, DOWN)
        
        #self.play(Write(y_text))
        #self.wait()

class coneGraph(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )

        # First define the original curves
        def inner(x):
            return np.sqrt(x)

        def outer(x):
            return x/2

        # Parametric surface for inner surface (y=√x)
        def param_surface_inner(u, v):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = np.sqrt(v)  # height from inner curve
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])

        # Parametric surface for outer surface (y=x/2)
        def param_surface_outer(u, v):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = v/2  # height from outer curve
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])

        # Create both rotated surfaces
        surface_inner = Surface(
            lambda u, v: param_surface_inner(u, v),
            u_range=[0, TAU],
            v_range=[0, 4],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(32, 32)
        )

        surface_outer = Surface(
            lambda u, v: param_surface_outer(u, v),
            u_range=[0, TAU],
            v_range=[0, 4],
            checkerboard_colors=[RED_D, RED_E],
            resolution=(32, 32)
        )

        # Plot original curves
        inner_graph = axes.plot(inner, x_range=[0, 4], color=BLUE)
        outer_graph = axes.plot(outer, x_range=[0, 4], color=RED)

        # Start with 2D view
        self.set_camera_orientation(phi=0, theta=0, gamma=90*DEGREES)
        self.add(axes, labels)
        self.play(Create(inner_graph), Create(outer_graph), run_time=2)

        # Move to 3D view and create surfaces
        self.move_camera(phi=75 * DEGREES, theta=-60 * DEGREES, gamma=0)
        self.play(
            Create(surface_inner),
            Create(surface_outer),
            run_time=3
        )

        # Rotate camera to show 3D shape
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()

class washerGraph(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )

        def create_washer_at_y(y):
            # For y=x/2, solve for x to get inner radius: x=2y
            inner_radius = 2*y
            # For y=√x, solve for x to get outer radius: x=y^2
            outer_radius = y*y
            
            # Create washer (ring) at height y
            t = y/2  # for color interpolation
            color = interpolate_color(ORANGE, RED, t)
            
            # Create ring using annulus
            washer = Surface(
                lambda u, v: np.array([
                    (inner_radius + (outer_radius-inner_radius)*v) * np.cos(u),
                    y,
                    (inner_radius + (outer_radius-inner_radius)*v) * np.sin(u)
                ]),
                u_range=[0, TAU],
                v_range=[0, 1],
                checkerboard_colors=[color, color],
                fill_opacity=0.5
            )
            return washer

        # Create 3D parametric curves instead of 2D plots
        inner_curve = ParametricFunction(
            lambda t: np.array([t, np.sqrt(t), 0]),
            t_range=[0, 4],
            color=BLUE
        )
        
        outer_curve = ParametricFunction(
            lambda t: np.array([t, t/2, 0]),
            t_range=[0, 4],
            color=RED
        )

        # Create washers at different y values
        y_values = np.linspace(0, 2, 50)
        washers = VGroup(*[create_washer_at_y(y) for y in y_values])

        # Set up scene and animate
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        self.add(axes, labels)

        self.play(Create(inner_curve), Create(outer_curve), run_time=2)
        self.play(Create(washers), run_time=5)

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(10)
        self.stop_ambient_camera_rotation()

class cylinderGraph(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )

        def create_cylinder_at_x(x):
            # Radius = 2πx
            radius =x#2 * PI * x
            # Height = x^2 + 1
            height = x**2 + 1
            
            # Create hollow cylinder
            t = x  # for color interpolation
            color = interpolate_color(BLUE, RED, t)
            Scolor = interpolate_color(PINK, PURPLE, t)
            cylinder = Surface(
                lambda u, v: np.array([
                    radius * np.cos(u),
                    v * height,
                    radius * np.sin(u)
                ]),
                u_range=[0, TAU],
                v_range=[0, 1],
                checkerboard_colors=[color, color],
                fill_opacity=0.5,
                stroke_color=Scolor,  # Add dark purple border
                stroke_width=4,
            )
            return cylinder

        # Create the original curve y = x^2 + 1
        curve = ParametricFunction(
            lambda t: np.array([t, t**2 + 1, 0]),
            t_range=[0, 1],
            color=YELLOW
        )

        line = Line(start=[1, 0, 0], end=[1, 2, 0], color=BLUE)

        # Create 10 cylinders from x=0 to x=1
        x_values = np.linspace(0.1, 1, 20)  # Avoid x=0 as radius would be 0
        cylinders = VGroup(*[create_cylinder_at_x(x) for x in x_values])

        # Set up scene and animate
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        self.add(axes, labels)

        # Show the original curve first
        self.play(
            Create(curve), 
            Create(line),
            run_time=2
        )
        
        # Create the cylinders
        self.play(Create(cylinders), run_time=15)

        # Rotate camera to show 3D shape
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(15)
        self.stop_ambient_camera_rotation()