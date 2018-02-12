
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture


class GameTable(FloatLayout):

    texture_image = ObjectProperty()

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

        with self.canvas.after:
            self.bgrect = Rectangle(pos=self.pos, size=(100, 100))

    def on_size(self, *args):
        self.bgrect.pos = self.pos
        self.bgrect.size = self.size

    def on_texture_image(self, instance, value):
        # Render the image
        # Resize image to the size of the background
        im_resize = self.texture_image.resize((int(self.bgrect.size[0]), int(self.bgrect.size[1])))
        # Create the blank texture
        texture = Texture.create(size=(int(self.bgrect.size[0]), int(self.bgrect.size[1])), colorfmt="luminance")
        # Convert the image to the texture
        data = im_resize.tobytes()
        texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="luminance")
        # Attach the texture to the table
        self.bgrect.texture = texture
