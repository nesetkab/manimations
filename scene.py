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

class cylinderGraph1(ThreeDScene): #6.3 number 7 | y=x^2 y=6x-2x^2
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.7), Text("z-axis").scale(0.45)
        )

        def create_cylinder_at_x(x):
            # Radius = x
            radius = x
            # Bottom height from y = x^2
            bottom_height = x**2
            # Top height from y = 6x - 2x**2
            top_height = 6*x - 2*x**2
            
            # Create hollow cylinder
            t = x  # for color interpolation
            color = interpolate_color(BLUE, RED, t)
            Scolor = interpolate_color(PINK, PURPLE, t)
            cylinder = Surface(
                lambda u, v: np.array([
                    radius * np.cos(u),
                    bottom_height + (top_height - bottom_height) * v,  # interpolate between curves
                    radius * np.sin(u)
                ]),
                u_range=[0, TAU],
                v_range=[0, 1],
                fill_color=color,
                fill_opacity=0.9,
                resolution=(16,8),
                checkerboard_colors=[BLUE, BLUE],
            )
            return cylinder

        # Create the original curve y = x^2
        Ocurve = ParametricFunction(
            lambda t: np.array([t, t**2, 0]),
            t_range=[0, 2],
            color=YELLOW
        )
        # Create the original curve 6x - 2x^2
        Icurve = ParametricFunction(
            lambda t: np.array([t, 6*t - 2*t**2, 0]),
            t_range=[0, 2],
            color=YELLOW
        )

        def param_surface_inner(u, v):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = 6*v - 2*v**2 # height from inner curve
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])

        # Parametric surface for outer surface (y=x/2)
        def param_surface_outer(u, v):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = v**2  # height from outer curve
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])

        # Create both rotated surfaces
        surface_inner = Surface(
            lambda u, v: param_surface_inner(u, v),
            u_range=[0, TAU],
            v_range=[0, 2],
            checkerboard_colors=[RED, RED],
            resolution=(16, 8)
        )

        surface_outer = Surface(
            lambda u, v: param_surface_outer(u, v),
            u_range=[0, TAU],
            v_range=[0, 2],
            checkerboard_colors=[RED, RED],
            resolution=(16, 8)
        )

        # Create 10 cylinders from x=0 to x=1
        x_values = np.linspace(0.1, 2, 15)  # Avoid x=0 as radius would be 0
        cylinders = VGroup(*[create_cylinder_at_x(x) for x in x_values])
        
        # Set up scene and animate
        self.set_camera_orientation(zoom=0.6)
        #self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        self.add(axes, labels)

        # Show the original curve first
        self.play(
            Create(Ocurve), 
            Create(Icurve),
            run_time=2
        )
        
        # Create the cylinders
        self.play(Create(cylinders), run_time=15)
        self.wait()
        self.play(
            Create(surface_inner),
            Create(surface_outer),
            run_time=3
        )
        self.play(
            cylinders.set_opacity(0).animate()
        )

        self.move_camera(phi=75 * DEGREES, theta=-20 * DEGREES)
        self.set_camera_orientation(zoom=0.9)

        # Rotate camera to show 3D shape
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(9)
        self.stop_ambient_camera_rotation()

        sample_cylinder = create_cylinder_at_x(1)
        sample_rectangle = Rectangle(height=3, width=(2*3.14159*1), color=GREEN, fill_opacity=1)

        self.move_camera(phi=0, theta=0, gamma=90*DEGREES, zoom=0.6)
        self.play(
            FadeOut(surface_inner),
            FadeOut(surface_outer),
            cylinders.set_opacity(0.1).animate(),
            run_time=3
        )
        self.play(
            FadeIn(sample_cylinder),
            FadeOut(axes,labels),
            FadeOut(Ocurve, Icurve),
            run_time=3
        )
        self.wait(),
        self.play(
            cylinders.animate.set_opacity(0),
            run_time=3
        )
        self.play(
            Transform(sample_cylinder, sample_rectangle),
            run_time=2
        )

        

class graph(ThreeDScene):
    def construct(self):
        # Improve axes appearance
        axes = ThreeDAxes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            z_range=[-5, 5],
            axis_config={
                "color": BLUE_E,
                "stroke_width": 2,
                "include_numbers": True,
                "numbers_to_exclude": [0]
            }
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.7), Text("z-axis").scale(0.45)
        )


        def param_surface_inner(u, v, equation):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = equation 
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])

        # Parametric surface for outer surface (y=x/2)
        def param_surface_outer(u, v, equation):
            # u is the angle of rotation (0 to 2π)
            # v is the x-coordinate in the original plane
            r = v  # radius = original x-coordinate
            y = equation  # height from outer curve
            x = r * np.cos(u)
            z = r * np.sin(u)
            return np.array([x, y, z])
        
        global inner_equation, outer_equation, inverseI_equation, inverseO_equation
        inner_equation = lambda v: ((v-1)**2)
        outer_equation = lambda v: (1/2 * v)
        inverseO_equation = lambda v: (np.sqrt(v)+1)
        inverseI_equation = lambda v: (2*v)
        
        # Find intersection point by solving: 6x-2x² = x²
        # 0 = 3x² - 6x = 3x(x-2)
        # x = 0 or x = 2
        intersection_x = 2  # using x = 2 since x = 0 is the start point
        
        # Improve surface appearance
        surface_inner = Surface(
            lambda u, v: param_surface_inner(u, v, inverseI_equation(v)),
            u_range=[0, TAU],
            v_range=[0.01, 1],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(16, 8),  # Higher resolution
            fill_opacity=0.8,
            stroke_width=0.5
        )

        surface_outer = Surface(
            lambda u, v: param_surface_outer(u, v, inverseO_equation(v)),
            u_range=[0, TAU],
            v_range=[0.01, 1],
            checkerboard_colors=[RED_D, RED_E],
            resolution=(16, 8),
            fill_opacity=0.8,
            stroke_width=0.5
        )

        # Improve curve appearance
        Ocurve = ParametricFunction(
            lambda t: np.array([t, (2*t), 0]),
            t_range=[0, intersection_x],
            color=YELLOW,
            shade_in_3d=True,
            stroke_width=4,
            stroke_opacity=1.0
        )
        
        Icurve = ParametricFunction(
            lambda t: np.array([t, (np.sqrt(t)+1), 0]),
            t_range=[0, intersection_x],
            color=YELLOW,
            shade_in_3d=True,
            stroke_width=4,
            stroke_opacity=1.0
        )

        # Better camera positioning and animation
        self.set_camera_orientation(
            phi=60 * DEGREES, 
            theta=-45 * DEGREES,
            zoom=0.7,
            frame_center=[0, 2, 0]  # Center the view on the interesting part
        )
        self.add(axes, labels)

        # Smoother animations
        self.play(
            Create(Ocurve), 
            Create(Icurve),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            Create(surface_inner),
            Create(surface_outer),
            #FadeOut(Icurve, Ocurve),
            run_time=3,
            rate_func=linear
        )

        # Smoother camera movement
        self.move_camera(
            phi=75 * DEGREES,
            theta=-20 * DEGREES,
            zoom=0.9,
            run_time=2,
            rate_func=smooth
        )

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(9)
        self.stop_ambient_camera_rotation()

class cylinderGraph2(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
            axis_config={"color": WHITE},
        )

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.7), Text("z-axis").scale(0.45)
        )

        def create_cylinder_at_x(x):
            # Radius = x
            radius = x
            # Bottom height from y = (x-1)^2
            bottom_height = (x-1)**2
            # Top height from y = x/2
            top_height = x/2
            
            # Create hollow cylinder
            t = x/4  # for color interpolation
            color = interpolate_color(BLUE, RED, t)
            Scolor = interpolate_color(PINK, PURPLE, t)
            cylinder = Surface(
                lambda u, v: np.array([
                    radius * np.cos(u),
                    bottom_height + (top_height - bottom_height) * v,
                    radius * np.sin(u)
                ]),
                u_range=[0, TAU],
                v_range=[0.5, 1],
                fill_color=color,
                fill_opacity=0.9,
                resolution=(16,8),
                checkerboard_colors=[BLUE, BLUE],
            )
            return cylinder

        # Create the original curves
        line = ParametricFunction(
            lambda t: np.array([t, t/2, 0]),
            t_range=[1/2, 2],
            color=YELLOW
        )
        
        parabola = ParametricFunction(
            lambda t: np.array([t, (t-1)**2, 0]),
            t_range=[1/2, 2],
            color=YELLOW
        )

        # Find intersection points by solving: x/2 = (x-1)^2
        # x/2 = x^2 - 2x + 1
        # 0 = 2x^2 - 4x - x + 2 = 2x^2 - 5x + 2
        # Using quadratic formula: x = (5 ± √(25-16))/4 = (5 ± 3)/4
        # x ≈ 2 is our intersection point of interest

        # Create cylinders
        x_values = np.linspace(0.1, 2, 15)
        cylinders = VGroup(*[create_cylinder_at_x(x) for x in x_values])
        
        # Set up scene and animate
        self.set_camera_orientation(zoom=0.6)
        self.add(axes, labels)

        # Show the original curves first
        self.play(
            Create(line), 
            Create(parabola),
            run_time=2
        )
        
        # Create the cylinders
        self.play(Create(cylinders), run_time=5)

        # Move camera for better view
        self.move_camera(phi=75 * DEGREES, theta=-20 * DEGREES)
        self.set_camera_orientation(zoom=0.9)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(9)
        self.stop_ambient_camera_rotation()

