from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

# Configure for YouTube Shorts (vertical 9:16)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.background_color = "#000000"

class Video(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(
            CoquiService(model_name="tts_models/en/ljspeech/vits")
        )

        # Custom Colors
        CUSTOM_RED = "#FF0000"
        CUSTOM_CYAN = "#00FFFF"
        # Standard Sans-Serif Font (using default Manim sans which is usually decent, or Arial if available)
        # We will stick to the default font to avoid system dependencies, but style it bold.

        # --- Scene 1: Hook (0:00 - 0:05) ---
        # "If you live in Malaysia and you’re under 16, you might get kicked off social media next year."
        
        with self.voiceover(text="If you live in Malaysia and you’re under 16, you might get kicked off social media next year.") as tracker:
            t_under = Text("UNDER 16?", font_size=80, weight=BOLD).move_to(ORIGIN)
            t_banned = Text("BANNED", font_size=100, weight=BOLD, color=CUSTOM_RED)
            t_banned.set_stroke(color=WHITE, width=2) # Add stroke to make it pop
            t_banned.rotate(15 * DEGREES) # Stamp effect angle
            
            t_country = Text("Malaysia 🇲🇾", font_size=40).to_edge(DOWN, buff=3)

            self.play(Write(t_under), run_time=0.5)
            self.play(
                t_under.animate.shift(UP * 3),
                FadeIn(t_banned, scale=2),
                run_time=0.4
            )
            self.play(FadeIn(t_country), run_time=0.5)
            self.wait(tracker.duration - 1.4)

        # Clear Scene 1
        self.play(FadeOut(t_under), FadeOut(t_banned), FadeOut(t_country), run_time=0.5)

        # --- Scene 2: The Core News (0:05 - 0:15) ---
        # "The Malaysian government is planning to ban anyone under 16 from having social media accounts on platforms like Facebook, Instagram, and X."
        
        with self.voiceover(text="The Malaysian government is planning to ban anyone under 16 from having social media accounts on platforms like Facebook, Instagram, and X.") as tracker:
            # Create Icons approximations
            # Facebook
            fb_circle = Circle(radius=1, color=BLUE, fill_opacity=1)
            fb_text = Text("f", font_size=100, weight=BOLD).move_to(fb_circle).shift(DOWN*0.1 + RIGHT*0.1)
            icon_fb = VGroup(fb_circle, fb_text)

            # Instagram
            ig_rect = RoundedRectangle(corner_radius=0.4, height=2, width=2, color=PURPLE, fill_opacity=1)
            ig_ring = Circle(radius=0.5, color=WHITE, stroke_width=8)
            ig_dot = Dot(color=WHITE).move_to(ig_rect.get_corner(UR) + DL * 0.3)
            icon_ig = VGroup(ig_rect, ig_ring, ig_dot)

            # X
            icon_x = Text("X", font_size=120, weight=BOLD).set_color(WHITE)

            icons_group = VGroup(icon_fb, icon_ig, icon_x).arrange(RIGHT, buff=0.8)
            icons_group.move_to(UP * 1)

            # Red Cross
            line1 = Line(icons_group.get_corner(UL), icons_group.get_corner(DR), color=CUSTOM_RED, stroke_width=15)
            line2 = Line(icons_group.get_corner(UR), icons_group.get_corner(DL), color=CUSTOM_RED, stroke_width=15)
            cross = VGroup(line1, line2)

            t_next_year = Text("Starting Next Year", font_size=50, weight=BOLD).next_to(icons_group, DOWN, buff=1.5)

            self.play(FadeIn(icons_group, shift=UP), run_time=1)
            self.play(Create(cross), run_time=0.5)
            self.play(Write(t_next_year), run_time=1)
            self.wait(tracker.duration - 2.5)

        self.play(FadeOut(icons_group), FadeOut(cross), FadeOut(t_next_year), run_time=0.5)

        # --- Scene 3: The Source (0:15 - 0:25) ---
        # "Communications Minister Fahmi Fadzil says they want to stop minors from opening accounts entirely, mandating strict age restrictions."
        
        with self.voiceover(text="Communications Minister Fahmi Fadzil says they want to stop minors from opening accounts entirely, mandating strict age restrictions.") as tracker:
            t_title = Text("Communications Minister", font_size=50)
            t_name = Text("Fahmi Fadzil", font_size=70, weight=BOLD, color=CUSTOM_CYAN)
            
            quote_text = Text('"Barring User Accounts"', font_size=60, slant=ITALIC)
            quote_text.set_color(WHITE)

            self.play(Write(t_title), run_time=1)
            self.play(ReplacementTransform(t_title, t_name), run_time=0.8)
            self.play(t_name.animate.shift(UP * 2), run_time=0.5)
            quote_text.next_to(t_name, DOWN, buff=1)
            self.play(FadeIn(quote_text, shift=UP), run_time=0.8)
            self.wait(tracker.duration - 3.1)

        self.play(FadeOut(t_name), FadeOut(quote_text), run_time=0.5)

        # --- Scene 4: The Global Trend (0:25 - 0:40) ---
        # "They aren't alone. Australia is pushing a similar ban, and countries like France and Norway are already working on systems to verify your age before you can download apps."
        
        with self.voiceover(text="They aren't alone. Australia is pushing a similar ban, and countries like France and Norway are already working on systems to verify your age before you can download apps.") as tracker:
            t_header = Text("NOT JUST MALAYSIA", font_size=50, color=CUSTOM_RED, weight=BOLD).to_edge(UP, buff=2)
            
            list_group = VGroup(
                Text("Australia 🇦🇺", font_size=45),
                Text("France 🇫🇷", font_size=45),
                Text("Norway 🇳🇴", font_size=45),
                Text("USA 🇺🇸", font_size=45),
            ).arrange(DOWN, buff=0.6).next_to(t_header, DOWN, buff=1)

            t_verify = Text("AGE VERIFICATION", font_size=60, color=CUSTOM_CYAN, weight=BOLD).move_to(DOWN * 4)

            self.play(FadeIn(t_header), run_time=0.5)
            self.play(LaggedStart(*[Write(item) for item in list_group], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(t_verify, scale=1.2), run_time=0.5)
            self.wait(tracker.duration - 3.0)

        self.play(FadeOut(t_header), FadeOut(list_group), FadeOut(t_verify), run_time=0.5)

        # --- Scene 5: The Reason (0:40 - 0:50) ---
        # "The goal? To protect children from online risks. Governments are now demanding platforms take responsibility for who is actually behind the screen."
        
        with self.voiceover(text="The goal? To protect children from online risks. Governments are now demanding platforms take responsibility for who is actually behind the screen.") as tracker:
            # Build Shield Icon
            shield_points = [
                [-2, 2, 0], # Top Left
                [2, 2, 0],  # Top Right
                [2, 0, 0],  # Side Right
                [0, -3, 0], # Bottom Tip
                [-2, 0, 0], # Side Left
                [-2, 2, 0]  # Close
            ]
            shield = VMobject()
            shield.set_points_as_corners(shield_points)
            # Smooth the bottom part manually by using CubicBezier if needed, 
            # but rounded corners on a polygon is easier for approximation:
            shield = RoundedRectangle(corner_radius=1, height=5, width=4, color=WHITE).set_stroke(width=8)
            # Clip top to make it flat? No, let's just use a simple box representing a "safe zone"
            
            # Text inside
            t_safety = Text("SAFETY", font_size=40, weight=BOLD).move_to(shield.get_center())
            
            shield_group = VGroup(shield, t_safety)
            
            t_protecting = Text("Protecting Kids", font_size=60, color=CUSTOM_CYAN, weight=BOLD).next_to(shield_group, DOWN, buff=1)

            self.play(DrawBorderThenFill(shield), Write(t_safety), run_time=1)
            self.play(Transform(t_safety, Text("KIDS", font_size=40, weight=BOLD).move_to(shield.get_center())), run_time=0.5)
            self.play(Write(t_protecting), run_time=1)
            self.wait(tracker.duration - 2.5)

        self.play(FadeOut(shield_group), FadeOut(t_safety), FadeOut(t_protecting), run_time=0.5)

        # --- Scene 6: Outro / CTA (0:50 - 1:00) ---
        # "If this passes, the internet changes forever. Do you think 16 is the right age limit? Tell us in the comments and subscribe for more tech news."
        
        with self.voiceover(text="If this passes, the internet changes forever. Do you think 16 is the right age limit? Tell us in the comments and subscribe for more tech news.") as tracker:
            t_question = Text("Is 16 the\nright age?", font_size=70, weight=BOLD, line_spacing=1.2).move_to(UP*2)
            
            # Comment Bubble
            bubble = RoundedRectangle(corner_radius=0.5, height=1.5, width=5, color=WHITE)
            bubble_tail = Triangle(color=WHITE, fill_opacity=0).scale(0.3).rotate(180*DEGREES).next_to(bubble, DOWN, buff=-0.1).shift(LEFT)
            t_comment = Text("Comment...", font_size=30).move_to(bubble)
            bubble_group = VGroup(bubble, bubble_tail, t_comment).move_to(DOWN*1)

            cursor = Arrow(start=DR, end=UL, color=CUSTOM_RED).scale(0.5).move_to(DOWN*3 + RIGHT*2)

            self.play(Write(t_question), run_time=1)
            self.play(FadeIn(bubble_group), run_time=0.5)
            
            # Cursor Animation
            self.play(cursor.animate.move_to(bubble_group.get_right() + DOWN*0.5), run_time=1)
            self.play(Indicate(bubble_group, color=CUSTOM_CYAN), run_time=0.5)

            t_sub = Text("SUBSCRIBE", font_size=90, weight=BOLD, color=CUSTOM_RED)
            
            self.play(
                FadeOut(t_question),
                FadeOut(bubble_group),
                FadeOut(cursor),
                GrowFromCenter(t_sub),
                run_time=0.5
            )
            self.wait(tracker.duration - 3.5)

with tempconfig({'output_file': '/tmp/VIDEO-1856743d80ba466f91dd2fc1547af180.mp4', 'quality': 'low_quality'}):
        scene = Video()
        scene.render()
