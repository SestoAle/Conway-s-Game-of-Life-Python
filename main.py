import kivy
kivy.require('1.9.0')


from kivy.lang import Builder
from kivy.app import App
from kivy.core.window import Window


# Explicitly load the KV file
root = Builder.load_file('./View.kv')

# Our application class.
class MyApp(App):
    def build(self):
        return root

Window.size = (600,700)
MyApp().run()