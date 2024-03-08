from manim import *
import numpy as np
from manim import *

#%% Notes:
""" Groups of object can be grouped using VGroup(object1, object2) and played with as a python list. Operations done on the VGroup is done on all its component
    the method .copy() is very pratical also to add a new object as if it comes from the first one without deleting the first one:
        Obect_1 = Circle(radius=0.5,color=BLUE_C)
        Object_2 = Object_1.copy().shift(UP)
        self.play(ReplacementTransform(Obect_1.copy(),Object_2)) 
        
    Docs:
    https://docs.manim.community/en/stable/reference/manim.utils.color.manim_colors.html
    https://azarzadavila-manim.readthedocs.io/en/latest/animation.html
    https://www.manim.community/"""

class FunctionGraph(Scene):
    def construct(self):
        #%% Config
        # self.camera.background_color = WHITE                                # For a white background (Default is black)
        background_image = ImageMobject("Figures/Code_Bg_Bleu_dark.png")              # Select background image
        self.add(background_image)                                            # Puts selected image as background

        # ACCENTCOLOR = ManimColor([0,0,0], alpha=1.0)                        # Define the accentcolor used througout the plots
        ACCENTCOLOR = WHITE

        #%% Geometry of the beam
        beam = Line(start=RIGHT, end=RIGHT*5, color=BLUE_E)                    # The beam is a line of length 4 (RIGHT = np.array([1., 0., 0.]))

        left_support = Rectangle(
                                height=0.3, width=0.2, 
                                fill_color=DARK_GREY, 
                                fill_opacity=1).move_to(beam.get_start())      # Create the left wall (clamped)

        right_support = Rectangle(height=0.3, width=0.2, fill_color=GREEN_E	
                                , fill_opacity=1).next_to(beam.get_end(),
                                direction=3*RIGHT)                             # Create the right wall (movable)

        displacement_vector = Arrow(beam.get_end(), 
                                    right_support.get_center(), 
                                    buff=0.1, color=RED_E)                     # Create the Dirichlet BC vector
        displacement_label = MathTex("u_L").next_to(displacement_vector, DOWN) # Create the BC label     


        def update_vector(vector, dt):
            """The vector has to be update as the right wall moves, this function takes care of it """
            new_vector = Arrow(beam.get_end(), right_support.get_center(), buff=0.1, color=RED_E)
            vector.become(new_vector)

        def update_vectorlab(vector, dt):
            """The label has to be update as the right wall moves, this function takes care of it """
            displacement_newlabel = MathTex("u_L").next_to(displacement_vector, DOWN)        
            displacement_label.become(displacement_newlabel)

        # Add updater to the displacement vector
        displacement_vector.add_updater(update_vector)
        displacement_label.add_updater(update_vectorlab)

        #%% plot the displacement

        E1 = ValueTracker(100)                                                 # Tracks the value of E1
        E2 = ValueTracker(100)                                                 # Tracks the value of E2
        uL = ValueTracker(0.03)                                                # Tracks the value of u_L
        # Displacement analytical solution
        A = 1                                                                  # Sectino area of the beam
        x_1 = 2.5                                                              # left position of the first body force
        x_2 = 7.5                                                              # right position of the second body force 

        # Defines background plane
        plane1 = (
            NumberPlane(x_range=[0, 10, 2], x_length=5, y_range=[0, 0.05, 0.01], y_length=5)
            .shift(LEFT * 3.5)
        )

        # Defines the analytical displacement that is redrawn whenerver a parameter is updated (enhanced the "always redraw") and add it to plane1
        disp = always_redraw(
         lambda: plane1.plot(
            lambda x: (1/(A*E1.get_value())*(np.exp(-np.pi*(x-x_1)**2)-np.exp(-(x_1**2)*np.pi))) \
        + (2/(A*E2.get_value())*(np.exp(-np.pi*(x-x_2)**2)-np.exp(-(x_2**2)*np.pi))) \
            - (x/(10*A*E1.get_value()))*(np.exp(-(x_1**2)*np.pi)) + (x/(10*A*E2.get_value()))*(np.exp(-(x_2**2)*np.pi))+(x*(uL.get_value()/10))
                            , x_range=[0, 10], color=RED_C
        )
        )


        # Label before adding any parameter (splitting the string so that it can latter be morphed)
        disp_lab = (
            MathTex("u =", "\overline{u}(x)")
            .next_to(plane1, UP, buff=0.2)
            .set_color(ACCENTCOLOR)
            .set_color_by_tex('x', BLUE_C)
            .set(height=0.5)
        )

        # Label after adding the first parameter 
        disp_labE = (
            MathTex("u =", "\sum\limits_{i=1}^m", "\overline{u}_i", "(x)","\lambda_i", "(E)")
            .next_to(plane1, UP, buff=0.2)
            .set_color(ACCENTCOLOR)
            .set_color_by_tex('x', BLUE_C)
            .set_color_by_tex('verl', BLUE_C)
            .set_color_by_tex('E', GREEN_D)
            .set_color_by_tex('lambda', GREEN_D)
            .set(height=1.2)
        )

        # Label after adding the second parameter 
        disp_labE1 = (
            MathTex("u =", "\sum\limits_{i=1}^m", "\overline{u}_i", "(x)","\prod\limits_{j=1}^k" ,"\lambda_i","^j", "(E_j)")
            .set(width=2.5)
            .next_to(plane1, UP, buff=0.2)
            .set_color(ACCENTCOLOR)
            .set_color_by_tex('x', BLUE_C)
            .set_color_by_tex('E', GREEN_D)
            .set_color_by_tex('verl', BLUE_C)
            .set_color_by_tex('lambda', GREEN_D)
            .set_color_by_tex('j', GREEN_D)
            .set(height=1.2)
        )

        self.play(Create(beam), Create(left_support), Create(right_support),Create(displacement_vector),
                LaggedStart(DrawBorderThenFill(plane1)),
                Write(displacement_label))

        self.play(FadeIn(disp),FadeIn(disp_lab))

        # Move the right support by changing the value of uL (rate function changes the interpolation shape between initial and last position (default is linear) see: https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html)
    
        self.play(right_support.animate.next_to(beam.get_end(), direction=LEFT, buff=0),uL.animate.set_value(0), run_time=3, rate_func=smooth)
        displacement_vector.remove_updater(update_vector)

        # Adds the Young'smodulus white lines above the beam
        left_line = Line(beam.get_start()+ UP*0.5, (0.6*beam.get_end()) + UP*0.5, color=ACCENTCOLOR)
        right_line = Line((0.6*beam.get_end())+ UP*0.5, beam.get_end() + UP*0.5, color=ACCENTCOLOR)

        def update_left_line(vector, dt):
            """ Update the vertical position of the left line with the value of E1"""
            new_left_line = Line(beam.get_start()+ (UP*0.5)*E1.get_value()/100, (0.6*beam.get_end()) + (UP*0.5)*E1.get_value()/100, color=ACCENTCOLOR)
            left_line.become(new_left_line)

        def update_right_line(vector, dt):
            """ Update the vertical position of the right line with the value of E2"""
            new_right_line = Line((0.6*beam.get_end())+ (UP*0.5)*E2.get_value()/100, beam.get_end() + (UP*0.5)*E2.get_value()/100, color=ACCENTCOLOR)
            right_line.become(new_right_line)

        left_line.add_updater(update_left_line)
        right_line.add_updater(update_right_line)

        # Add label to the lines 
        left_label = MathTex("E_1").next_to(left_line, UP).set_color(GREEN_D)
        right_label = MathTex("E_2").next_to(right_line, UP).set_color(GREEN_D)
        Elabel = MathTex("E").next_to(beam, 2*UP).set_color(GREEN_D)

        # Update the position of the label to the position of the lines
        def update_Elabel(vector, dt):
            new_labE = MathTex("E").next_to(beam, 2.5*UP*E1.get_value()/100).set_color(GREEN_D)
            Elabel.become(new_labE)
        Elabel.add_updater(update_Elabel)

        # Update the position of the label to the position of the lines
        def update_leftlabel(vector, dt):
            new_left_label = MathTex("E_1").next_to(left_line, UP*E1.get_value()/100).set_color(GREEN_D)
            left_label.become(new_left_label)
        left_label.add_updater(update_leftlabel)

        # Update the position of the label to the position of the lines
        def update_rightlabel(vector, dt):
            new_right_label = MathTex("E_2").next_to(right_line, UP*E2.get_value()/100).set_color(GREEN_D)
            right_label.become(new_right_label)
        right_label.add_updater(update_rightlabel)

        #%% Add smooth comments and text to the screen 

        # Circle out the string " Tensor decomposition"
        TensorDecompSquare =(Rectangle(width=5, height=1, color=BLUE_B).next_to(disp_labE, 12*RIGHT, buff=0.2))
        # Add the string " Tensor decomposition"
        TensorDecomp = (
            Tex("Tensor Decomposition")
            .move_to(TensorDecompSquare.get_center())
            .set_color(WHITE)
            .set(height=0.4)
        )
        # Add legend for the parameter E
        ExtraCoor = (
            Tex(r"* Extra-coordinate",":"," $E$")
            .next_to(TensorDecompSquare, 19*DOWN)
            .set_color(GREEN_D)
            .set(height=0.4)
        )
        # Add legend for the extra-coordinates k=2
        ExtraCoor2 = (
            Tex(r"* Extra-coordinate","s",":"," $k=2$")
            .next_to(TensorDecompSquare, 19*DOWN)
            .set_color(GREEN_D)
            .set(height=0.4)
        )

        self.play(Create(left_line),Create(right_line),Create(TensorDecompSquare), 
                        Write(Elabel),
                        TransformMatchingTex(disp_lab, disp_labE),
                        FadeIn(TensorDecomp,ExtraCoor))


        # Play with only E uniform on the beam (same values for E1 and E2 anf Elabel)
        self.play(E1.animate.set_value(200),E2.animate.set_value(200), run_time=2, rate_func=wiggle)
        self.play(E1.animate.set_value(150),E2.animate.set_value(150), run_time=2, rate_func=wiggle)
        self.remove(Elabel)

        # Play with only E1 and E2 
        self.play(Write(left_label),Write(right_label),TransformMatchingTex(disp_labE, disp_labE1),TransformMatchingTex(ExtraCoor,ExtraCoor2))
        self.play(E1.animate.set_value(200),E2.animate.set_value(10), run_time=2, rate_func=wiggle)
        self.play(E1.animate.set_value(10),E2.animate.set_value(200), run_time=2, rate_func=wiggle)
        self.wait()


  
