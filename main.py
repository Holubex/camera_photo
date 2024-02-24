from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import Filesharer
import time
import webbrowser

Builder.load_file('frontend.kv')


class CameraScreen(Screen):

    def start(self):
        ''' Starts the camera. '''
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        ''' Stops the camera. '''
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        ''' Capture the photo (current time), saves it and
        move to the Image Screen.'''
        our_time = time.strftime('%Y%m%d-%H%M%S')
        self.filename = our_time + '.png'
        self.ids.camera.export_to_png(self.filename)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filename


class ImageScreen(Screen):

    def create_link(self):
        '''Create a sharable link'''
        file_path = App.get_running_app().root.ids.camera_screen.filename
        fileshare = Filesharer(file_path)
        self.url =fileshare.share()
        self.manager.current_screen.ids.new_label.text = self.url

    def copy_link(self):
        '''Copy link to clipboard'''
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.new_label.text = 'Create a link.'

    def open_link(self):
        '''Open link in browser'''
        try:
            webbrowser.open(self.url)
        except:
            self.ids.new_label.text = 'Create a link.'
class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()