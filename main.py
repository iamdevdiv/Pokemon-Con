# Pokémon Con
# -- Developed by Divyanshu Tiwari --

# Imports
# from os import environ
# environ["KIVY_AUDIO"] = "android"

from functools import partial
# from jnius import autoclass
# from kivyauth.utils import auto_login, login_providers
from kivyauth.google_auth import initialize_google, logout_google

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ColorProperty, NumericProperty, ObjectProperty, StringProperty


Window.size = (900, 450)  # temporary


# CUSTOM WIDGETS

# Button with rounded corners and some fanciness
class FancyButton(Button):
    # These attributes will be modified on_press via animation to represent click effect
    scale_value_x = NumericProperty(1)
    scale_value_y = NumericProperty(1)

    rounded_btn_img = ObjectProperty(None)  # the image on the left side of the button
    img_source = StringProperty(None)  # source of the rounded_btn_img
    img_width_divisor = NumericProperty(1.4)  # used in center property of the rounded_btn_img to center it properly
    img_height_subtractor = NumericProperty(5)  # used in size property of the rounded_btn_img to fit ir properly

    label_text = StringProperty("")  # text of the label
    label_color = ColorProperty([1, 1, 1, 1])  # color of the label
    label_font_name = StringProperty("Fonts/av_qest.ttf")
    label_font_size_divisor = NumericProperty(1.2)
    label_center_x_subtractor = NumericProperty(5)  # used in center property of the label to center it properly
    label_center_y_addend = NumericProperty(0)  # same as above


# Image which can be rotated
class RotatableImage(Image):  # https://stackoverflow.com/a/17699932/14113019
    angle = NumericProperty()


# Dropdown list with rounded corners and some fanciness
class FancySpinner(Spinner):
    # These attributes will be modified on_press via animation to represent click effect
    scale_value_x = NumericProperty(1)
    scale_value_y = NumericProperty(1)

    label_text = StringProperty("")  # text of the label
    label_color = ColorProperty([1, 1, 1, 1])  # color of the label
    label_center_x_subtractor = NumericProperty(5)  # used in center property of the label to center it properly


# First screen of the game which shows loading progress
class LoadingScreen(Screen):
    loading_bar = ObjectProperty(None)  # gradient blue line on the bottom of the screen to represent loading progress

    def __init__(self) -> None:
        super(LoadingScreen, self).__init__(name="Loading Screen")
        self.app = App.get_running_app()
        # Following event will check continuously whether loading is completed (using go_to_login_screen method) and
        # change the screen to login screen on completion. It will be triggered on_start (App class)
        self.wait_for_loading_completion = Clock.create_trigger(self.go_to_login_screen, 1, True)

    # This method will be used by wait_for_loading_completion Clock event (__init__)
    def go_to_login_screen(self, delta_time=0) -> None:  # NOQA
        if self.app.loading_completed:
            self.app.screen_manager.current = "Login Screen"

    # This method will increase the width of the loading_bar with animation
    def set_loading_progress(self, progress: float) -> None:
        Animation(width=self.app.root.width * progress, duration=0.2).start(self.loading_bar)
        # Set previous_task_completed (App class) to True after 0.2 seconds (same duration as the above animation)
        Clock.schedule_once(partial(self.app.set_task_completed, progress), 0.2)


# Login screen will be shown after completion of loading. Game intro will take place on this screen.
class LoginScreen(Screen):
    skip_intro_msg = ObjectProperty(None)  # the message to tell the player how to skip the intro
    bg_image = ObjectProperty(None)
    bg_image_source = StringProperty("Images/intro_bg.jpg")

    # presented_by widgets
    developer_text = ObjectProperty(None)
    divyanshu_text = ObjectProperty(None)
    dev_text = ObjectProperty(None)
    div_text = ObjectProperty(None)
    dev_div_text = ObjectProperty(None)
    presents_text = ObjectProperty(None)

    # powered_by widgets
    python_powered = ObjectProperty(None)
    and_text = ObjectProperty(None)
    kivy_logo = ObjectProperty(None)
    kivy_text = ObjectProperty(None)

    # Pokémon images
    pokemon_images = ObjectProperty(None)
    the_biggest = ObjectProperty(None)  # Charmander / Charmeleon / Charizard / Mega Charizard X
    aerodactyl = ObjectProperty(None)
    weavile = ObjectProperty(None)
    pikachu = ObjectProperty(None)
    blastoise = ObjectProperty(None)

    # Game's title widgets
    game_title = ObjectProperty(None)
    p_text = ObjectProperty(None)  # pokémon
    o_text = ObjectProperty(None)
    k_text = ObjectProperty(None)
    e_text = ObjectProperty(None)
    m_text = ObjectProperty(None)
    o_2_text = ObjectProperty(None)
    n_text = ObjectProperty(None)
    c_text = ObjectProperty(None)  # con
    o_3_text = ObjectProperty(None)
    n_2_text = ObjectProperty(None)

    # Top buttons
    top_buttons = ObjectProperty(None)  # parent widget of the top buttons
    exit_btn = ObjectProperty(None)
    options_btn = ObjectProperty(None)
    help_btn = ObjectProperty(None)

    exit_content = ObjectProperty(None)
    options_content = ObjectProperty(None)
    music_slider = ObjectProperty(None)
    sfx_slider = ObjectProperty(None)
    email_addr = ObjectProperty(None)

    # Bottom buttons
    bottom_buttons = ObjectProperty(None)  # parent widget of the bottom buttons
    login_btn = ObjectProperty(None)  # Login/Start
    pokeball = ObjectProperty(None)  # not a button but image (on login_btn), will be rotated on loading
    credits_btn = ObjectProperty(None)
    terms_btn = ObjectProperty(None)  # Terms of Use
    pipe_char = ObjectProperty(None)  # not a button but label (between terms_btn and policy_btn)
    policy_btn = ObjectProperty(None)  # Privacy Policy

    def __init__(self) -> None:
        super(LoginScreen, self).__init__(name="Login Screen")
        self.app = App.get_running_app()
        self.intro_completed = False  # prevents button clicks until intro is completed

    def on_enter(self) -> None:
        self.app.intro_music.play()  # start intro music on entering the login screen after loading completion
        Clock.schedule_interval(self.wait_for_music_start, 0.01)

    def wait_for_music_start(self, delta_time=0) -> bool:  # NOQA
        if self.app.intro_music.get_pos() != 0:  # when intro music has started, start the intro
            self.start_intro()
            return False  # stops clock interval

    def start_intro(self) -> None:  # schedules all the intro events
        Clock.schedule_once(self.toggle_intro_msg_opacity, 0)  # shows skip_intro_msg

        Clock.schedule_once(self.show_presented_by, 0.45)
        Clock.schedule_once(self.show_presented_by, 1.55)
        Clock.schedule_once(self.show_presented_by, 2.65)
        Clock.schedule_once(self.show_presented_by, 2.95)
        Clock.schedule_once(self.show_presented_by, 3.15)
        Clock.schedule_once(self.show_presented_by, 3.35)
        Clock.schedule_once(self.show_presented_by, 4.55)

        Clock.schedule_once(self.toggle_intro_msg_opacity, 5)  # hides skip_intro_msg

        Clock.schedule_once(self.show_powered_by, 5.55)
        Clock.schedule_once(self.show_powered_by, 5.8)
        Clock.schedule_once(self.show_powered_by, 6.05)
        Clock.schedule_once(self.show_powered_by, 6.25)

        Clock.schedule_once(self.show_pokemon_images, 6.25)
        Clock.schedule_once(self.show_pokemon_images, 6.85)
        Clock.schedule_once(self.show_pokemon_images, 7.05)
        Clock.schedule_once(self.show_pokemon_images, 8.55)
        Clock.schedule_once(self.show_pokemon_images, 9.1)
        Clock.schedule_once(self.show_pokemon_images, 9.2)
        Clock.schedule_once(self.show_pokemon_images, 9.3)

        Clock.schedule_once(self.show_bottom_buttons, 10.05)
        Clock.schedule_once(self.show_bottom_buttons, 10.55)
        Clock.schedule_once(self.show_bottom_buttons, 10.65)
        Clock.schedule_once(self.show_bottom_buttons, 10.75)

        Clock.schedule_once(self.show_top_buttons, 11.45)
        Clock.schedule_once(self.show_top_buttons, 11.75)
        Clock.schedule_once(self.show_top_buttons, 11.95)

        Clock.schedule_once(self.show_game_title, 12.15)
        Clock.schedule_once(self.show_game_title, 12.85)
        Clock.schedule_once(self.show_game_title, 12.95)
        Clock.schedule_once(self.show_game_title, 14.45)
        Clock.schedule_once(self.show_game_title, 14.75)
        Clock.schedule_once(self.show_game_title, 14.95)
        Clock.schedule_once(self.show_game_title, 15.15)

        Clock.schedule_once(self.hide_everything, 15.95)
        Clock.schedule_once(self.hide_everything, 16.15)
        Clock.schedule_once(self.hide_everything, 16.45)
        Clock.schedule_once(self.hide_everything, 16.65)

        Clock.schedule_once(self.show_everything, 17.35)

    @staticmethod
    def skip_intro() -> None:  # the player can skip the intro by tapping anywhere on the screen
        for event in Clock.get_events():
            # 'Login Screen' included to prevent any other clock events from being cancelled
            # 'wait_for_music_start' excluded to prevent the intro from not starting
            # 'set_intro_completed' excluded to prevent any button's on_release callback from executing when user taps
            # on the screen to skip the intro
            e_name = str(event)  # event's name
            if "Login Screen" in e_name and \
                    ("wait_for_music_start" not in e_name and "set_intro_completed" not in e_name):
                event.get_callback()()  # execute every scheduled callback (from start_intro method) immediately and...
                event.cancel()  # ...then cancel that clock event
            elif "Animation" in e_name:  # to prevent stopping of animation of skip_intro_msg
                event.cancel()

    def toggle_intro_msg_opacity(self, delta_time=0):  # First shows then hides the intro skip instruction
        if delta_time != 0:  # not to run when user skips the intro
            new_opacity = 0.5 if self.skip_intro_msg.opacity == 0 else 0
            Animation(opacity=new_opacity, duration=1.5).start(self.skip_intro_msg)

    def show_presented_by(self, delta_time=0) -> None:  # NOQA
        if self.presents_text.opacity == 1:  # 7 - [BLANK SCREEN]
            self.dev_div_text.opacity = self.presents_text.opacity = 0
        elif self.dev_div_text.opacity == 1:  # 6 - 'DevDiv presents'
            self.presents_text.opacity = 1
        elif self.div_text.opacity == 1:  # 5 - 'DevDiv'
            self.developer_text.opacity = self.divyanshu_text.opacity = 0
            self.dev_text.opacity = self.div_text.opacity = 0
            self.dev_div_text.opacity = 1
        else:
            if self.developer_text.opacity == 0:  # 1 - 'Developer'
                self.developer_text.opacity = 1
            elif self.divyanshu_text.opacity == 0:  # 2 - 'Developer Divyanshu'
                self.divyanshu_text.opacity = 1
            elif self.dev_text.opacity == 0:  # 3 - 'Developer Divyanshu' ('Dev' highlighted)
                self.dev_text.opacity = 1
            else:  # 4 - 'Developer Divyanshu' ('Dev' and 'Div' highlighted)
                self.div_text.opacity = 1

    def show_powered_by(self, delta_time=0) -> None:  # NOQA
        if self.python_powered.opacity == 0:  # 1 - [PYTHON POWERED LOGO]
            self.python_powered.opacity = 1
        elif self.and_text.opacity == 0:  # 2 - '[PYTHON POWERED LOGO] and'
            self.and_text.opacity = 1
        elif self.kivy_logo.opacity == 0:  # 3 - '[PYTHON POWERED LOGO] and [KIVY LOGO]'
            self.kivy_logo.opacity = self.kivy_text.opacity = 1
        else:  # 4 - [BLANK SCREEN]
            self.python_powered.opacity = self.and_text.opacity = self.kivy_logo.opacity = self.kivy_text.opacity = 0

    def show_pokemon_images(self, delta_time=0) -> None:  # NOQA
        if self.aerodactyl.opacity == 0:  # 1 - [AERODACTYL IMAGE]
            self.aerodactyl.opacity = 1
        elif self.weavile.opacity == 0:  # 2 - [WEAVILE IMAGE]
            self.weavile.opacity = 1
        elif self.blastoise.opacity == 0:  # 3 - [BLASTOISE IMAGE]
            self.blastoise.opacity = 1
        elif self.the_biggest.opacity == 0:  # 4 - [CHARMANDER IMAGE]
            self.the_biggest.opacity = 1
        elif self.the_biggest.source == "Images/charmander.png":  # 5 - [CHARMELEON IMAGE]
            self.the_biggest.source = "Images/charmeleon.png"
        elif self.the_biggest.source == "Images/charmeleon.png":  # 6 - [CHARIZARD IMAGE]
            self.the_biggest.source = "Images/charizard.png"
        else:  # 7 - [MEGA CHARIZARD X IMAGE]
            self.the_biggest.source = "Images/mega_charizard_x.png"

    def show_bottom_buttons(self, delta_time=0) -> None:  # NOQA
        if self.login_btn.opacity == 0:  # 1 - 'Login' / 'Start' button
            self.login_btn.opacity = 1
        elif self.credits_btn.opacity == 0:  # 2 - 'Credits' button
            self.credits_btn.opacity = 1
        elif self.terms_btn.opacity == 0:  # 3 - 'Terms of Use' button
            self.terms_btn.opacity = 1
        else:  # 4 - 'Privacy Policy' button
            self.policy_btn.opacity = self.pipe_char.opacity = 1

    def show_top_buttons(self, delta_time=0) -> None:  # NOQA
        if self.exit_btn.opacity == 0:  # 1 - 'Exit' button
            self.exit_btn.opacity = 0.9
        elif self.options_btn.opacity == 0:  # 2 - 'Options' button
            self.options_btn.opacity = 0.9
        else:  # 3 - 'Help' button
            self.help_btn.opacity = 0.9

    def show_game_title(self, delta_time=0) -> None:  # NOQA
        if self.p_text.opacity == 0:  # 1 - 'P'
            self.p_text.opacity = 1
        elif self.k_text.opacity == 0:  # 2 - 'P_k'
            self.k_text.opacity = 1
        elif self.e_text.opacity == 0:  # 3 - 'P_ké'
            self.e_text.opacity = 1
        elif self.m_text.opacity == 0:  # 4 - 'P_kém'
            self.m_text.opacity = 1
        elif self.c_text.opacity == 0:  # 5 - 'P_kém__ C'
            self.c_text.opacity = 1
        elif self.o_text.opacity == 0:  # 6 - 'Pokémo_ Co'
            self.o_text.opacity = self.o_2_text.opacity = self.o_3_text.opacity = 1
        else:  # 7 - 'Pokémon Con'
            self.n_text.opacity = self.n_2_text.opacity = 1

    def hide_everything(self, delta_time=0) -> None:  # NOQA
        if self.top_buttons.opacity == 1:  # 1 - [HIDE TOP BUTTONS]
            self.top_buttons.opacity = 0
        elif self.bottom_buttons.opacity == 1:  # 2 - [HIDE BOTTOM BUTTONS]
            self.bottom_buttons.opacity = 0
        elif self.pokemon_images.opacity == 1:  # 3 - [HIDE POKÉMON IMAGES]
            self.pokemon_images.opacity = 0
        else:  # 4 - [HIDE GAME TITLE] (Everything is hidden now)
            self.game_title.opacity = 0

    def show_everything(self, delta_time=0) -> None:  # NOQA
        self.skip_intro_msg.opacity = 0  # hide skip_intro_msg
        Clock.schedule_once(self.set_intro_completed, 0.1)  # intro_completed will be set to True after .1 seconds delay

        # Show everything at once
        self.top_buttons.opacity = self.bottom_buttons.opacity = 1
        self.pokemon_images.opacity = self.pikachu.opacity = 1
        self.game_title.opacity = 1
        self.bg_image.opacity = 0.6

    def set_intro_completed(self, delta_time=0) -> None:  # NOQA
        self.intro_completed = True

    # Used to hide or show the Pokémon images when user selects or unselects one of the top buttons
    def set_pokemon_imgs_visibility(self, make_visible: bool) -> None:
        if make_visible:
            self.bg_image_source = "Images/intro_bg.jpg"
            self.the_biggest.opacity = 1
            self.weavile.opacity = 1
            self.aerodactyl.opacity = 1
            self.pikachu.opacity = 1
            self.blastoise.opacity = 1
        else:
            self.bg_image_source = "Images/intro_bg_gradient.jpg"
            self.the_biggest.opacity = 0
            self.weavile.opacity = 0
            self.aerodactyl.opacity = 0
            self.pikachu.opacity = 0
            self.blastoise.opacity = 0

    def toggle_top_button(self, button) -> None:  # handles opacity of top buttons, their content and Pokémon images
        if button.opacity in [0.5, 0.9]:  # when no or one button is already selected
            self.exit_btn.opacity = self.options_btn.opacity = self.help_btn.opacity = 0.5
            button.opacity = 1
        else:  # on unselecting the selected button
            self.exit_btn.opacity = self.options_btn.opacity = self.help_btn.opacity = 0.9

        if self.exit_btn.opacity == self.options_btn.opacity == self.help_btn.opacity == 0.9:  # no button selected
            self.set_pokemon_imgs_visibility(True)
        else:  # a button is selected
            self.set_pokemon_imgs_visibility(False)

        # Handle content's opacity
        if self.exit_btn.opacity == 1:
            self.exit_content.opacity = 1
        else:
            self.exit_content.opacity = 0
        if self.options_btn.opacity == 1:
            self.options_content.opacity = 1
        else:
            self.options_content.opacity = 0

    # Used to unselect the exit button and hide its content when user chooses not to exit the game
    def unselect_exit_button(self) -> None:
        self.exit_btn.opacity = self.options_btn.opacity = self.help_btn.opacity = 0.9  # reset opacity to default
        self.exit_content.opacity = 0
        self.set_pokemon_imgs_visibility(True)

    def handle_exit(self, to_exit: bool) -> None:
        if to_exit:
            self.app.stop()
        else:
            self.unselect_exit_button()

    def set_volume(self, target: str, volume: int) -> None:  # volume slider's on_value callback
        if target == "music":
            self.app.music_vol = volume
            self.app.intro_music.volume = volume
            # self.app.credits_music.volume = volume
            # self.app.training_mode_music.volume = volume
            # self.app.online_battle_music.volume = volume
            # self.app.main_menu_music.volume = volume
        elif target == "sfx":
            pass

    def rotate_pokeball(self, delta_time=0) -> None: # NOQA (rotate pokeball to represent loading)
        anim = Animation(angle=self.pokeball.angle - 180, duration=0.1)
        anim.start(self.pokeball)

    def reset_addr(self, addr: str, delta_time=0) -> None:  # NOQA
        if self.email_addr.text != "":
            self.email_addr.text = addr

    def confirm_logout(self):
        addr = self.email_addr.text
        if addr == "Press again to confirm logout":
            logout_google(self.after_logout)
            self.email_addr.text = ""
        else:
            self.email_addr.text = "Press again to confirm logout"
            Clock.schedule_once(partial(self.reset_addr, addr), 2)

    def after_logout(self) -> None:
        self.login_btn.label_text = "Login"
        self.login_btn.img_source = "Images/google.png"
        self.email_addr.text = ""


# Root widget of all the screens and widgets of the game
class PokemonCon(App):
    def __init__(self) -> None:
        super(PokemonCon, self).__init__()
        Window.bind(on_keyboard=self.back_button)
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.login_screen = None

        self.loading_screen = None
        self.previous_task_completed = True  # initially True to allow the first task to start
        self.all_screens_added = False
        self.every_music_loaded = False
        self.loading_completed = False

        self.music_allowed = True
        self.music_vol = 1  # preferred music volume set by the user
        self.sfx_vol = 1  # preferred sound effect volume set by the user

        self.intro_music = None
        self.credits_music = None
        self.training_mode_music = None
        self.online_battle_music = None
        self.main_menu_music = None

    @staticmethod
    def back_button(window, key, *args) -> bool: # NOQA (handle back button click)
        if key == 27:
            return True

    def on_start(self) -> None:
        # auto_login(login_providers.google)
        # autoclass("org.kivy.android.PythonActivity").mActivity.removeLoadingScreen()  # remove pre-splash image

        self.loading_screen = self.screen_manager.get_screen("Loading Screen")
        Clock.schedule_interval(self.load, 0.5)  # try to load screens and music every 0.5 second
        Clock.schedule_once(self.loading_screen.wait_for_loading_completion, 1)  # Check for loading completion every
        # second

    # previous_task_completed will be set to True only after the loading bar's animation has completed
    # This will prevent GUI from getting hung due to the start of the next task (such as music loading)
    def set_task_completed(self, progress: float, delta_time=0) -> None:  # NOQA
        self.previous_task_completed = True
        if progress == 1:  # 1 means loading is completed
            self.loading_completed = True

    def add_screen(self) -> None:  # adds screens to the screen manager
        if "Login Screen" not in self.screen_manager.screen_names:
            self.screen_manager.add_widget(LoginScreen())

            # Load the other Pokémon Images of the login screen to prevent delay later in the intro
            self.login_screen = self.screen_manager.get_screen("Login Screen")
            self.login_screen.the_biggest.source = "Images/charmeleon.png"  # load Charmeleon
            self.login_screen.the_biggest.source = "Images/charizard.png"  # load Charizard
            self.login_screen.the_biggest.source = "Images/mega_charizard_x.png"  # load Mega Charizard X
            self.login_screen.the_biggest.source = "Images/charmander.png"  # set back to the default 'Charmander'
            self.music_vol = self.login_screen.music_slider.value

            self.loading_screen.set_loading_progress(0.5)

            self.all_screens_added = True

    def load_music(self) -> None:  # loads music files
        if self.intro_music is None:
            self.intro_music = SoundLoader.load("Sounds/intro.ogg")
            self.loading_screen.set_loading_progress(1)

            self.every_music_loaded = True

        self.intro_music.loop = True
        self.intro_music.volume = self.music_vol

    def load(self, delta_time=0) -> bool:  # NOQA (this method will add all the screens and load music)
        if self.previous_task_completed:
            self.previous_task_completed = False

            if not self.all_screens_added:
                self.add_screen()
            elif not self.every_music_loaded:
                self.load_music()
            elif self.loading_completed:
                return False  # stops clock interval

    def update_ui(self, addr: str, delta_time=0):  # NOQA (updates UI on_start on successful login)
        if self.login_screen is not None:
            self.login_screen.login_btn.label_text = "Start"
            self.login_screen.login_btn.img_source = "Images/pokeball.png"
            self.login_screen.email_addr.text = f"Logged in as {addr}"

            return False  # stop clock interval after successful update of UI

    def after_login(self, name, email, photo_url) -> None:  # NOQA
        Clock.schedule_interval(partial(self.update_ui, email), 1)  # try updating UI every second until success

    @staticmethod
    def login_error_listener():
        pass

    def build(self) -> ScreenManager:
        # These client IDs and client secrets are now invalid
        # initialize_google(self.after_login, self.login_error_listener, "104284788592-"
        #                                                                "ed1bgndd9e0bnqikgcvrjp6l5s4h1ctc"
        #                                                                ".apps.googleusercontent.com",
        #                   "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")
        # initialize_google(self.after_login, self.login_error_listener, "104284788592-"
        #                                                                "b2tdan570nhjvf9s1jdmkodro1ian3n4"
        #                                                                ".apps.googleusercontent.com")
        self.screen_manager.add_widget(LoadingScreen())
        return self.screen_manager


if __name__ == "__main__":
    PokemonCon().run()
