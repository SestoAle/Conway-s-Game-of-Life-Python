
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
import numpy as np
from PIL import Image, ImageFilter, ImageChops


class Model(EventDispatcher):

    image = ObjectProperty()
    texture_to_render = ObjectProperty()
    size_image = 300
    start_text = StringProperty("Start")
    load_text = StringProperty("Load")
    num_cells = NumericProperty(100)
    time = NumericProperty(25)
    heatmap = BooleanProperty(False)
    is_running = BooleanProperty(False)

    max_num_cells = 200
    min_num_cells = 30
    max_time = 60
    min_time = 1

    def __call__(self, *args, **kwargs):
        return self

    def __init__(self):
        super(Model, self).__init__()

        self.image = Image.new('L', (self.size_image, self.size_image), "black")

    def image_to_texture(self):

        # Map to a bitmap or a grey-level image depending on the heatmap value
        if not self.heatmap:
            grey_level = self.image.point(lambda p: 255 if p > 0 else 0)
        else:
            grey_level = self.image.point(lambda p: p*2 + 30 if p > 0 else 0)

        # Crop the image to the size of the chosen grid and assign it to the texture_to_render variable, that triggers
        # the on_texture_image method of GameTable class
        index_0 = int(self.size_image/2 - self.num_cells/2)
        index_1 = int(self.size_image/2 + self.num_cells/2)

        self.texture_to_render = grey_level.crop((index_0, index_0, index_1, index_1))


    def transform_coord(self, instance, touch):
        # Convert the touch down coordinates to cell coordinates

        local_coordinate_x = (touch.pos[0] - Window.size[0] + instance.size[0]) / instance.size[0]
        local_coordinate_y = (touch.pos[1] - Window.size[1] + instance.size[1]) / instance.size[1]

        index = []

        index.append(int(local_coordinate_x * (self.num_cells)))
        index.append(int(local_coordinate_y * (self.num_cells)))

        index[0] = int(self.size_image/2 - self.num_cells/2 + index[0])
        index[1] = int(self.size_image/2 - self.num_cells/2 + index[1])

        return index

    def on_touch_down(self, instance, touch):
        # Convert the clicked cell to a white [black] cell and re-render the image

        if (not instance.collide_point(*touch.pos)):
            return

        index = self.transform_coord(instance, touch)

        pixel = self.image.load()

        if pixel[index[0], index[1]] == 0:
            pixel[index[0], index[1]] = 1
        else:
            pixel[index[0], index[1]] = 0


        self.image_to_texture()

    def on_touch_move(self, instance, touch):
        # Same as the on_touch_down

        if (not instance.collide_point(*touch.pos)):
            return

        index = self.transform_coord(instance, touch)

        pixel = self.image.load()

        try:
            if pixel[index[0], index[1]] == 0:
                pixel[index[0], index[1]] = 1
        except IndexError:
            print("Move out of bounds")

        self.image_to_texture()


    def filter(self, dt):
        # Convolve the image with a kernel [2,2,2,2,1,2,2,2,2,2].
        # Pass the image to the try_evolve() method and then re-render the image

        bitmap = self.image.point(lambda p: p > 0 and 1)

        # Add padding to the image for the convolution
        im_conv = Image.new("L", (self.size_image + 2, self.size_image + 2), "black")
        im_conv.paste(bitmap, (1, 1))

        # Convolve the image and crop it to eliminate the padding
        new_im = im_conv.filter(ImageFilter.Kernel((3, 3), [2, 2, 2, 2, 1, 2, 2, 2, 2], 1, 0))
        new_im = new_im.crop((1, 1, self.size_image + 1, self.size_image + 1))

        # Map the new image with the try_evolve method()
        new_im = new_im.point(self.try_evolve)

        # Calculate the pixel that was living on the previous frame, add them to the new image and re-render it
        # Multiply the old image with the new image. The result is the pixel that was alive in the previous frame
        # PIL multiplication is not usable in this case, must use numpy
        arr1 = np.asarray(self.image)
        arr2 = np.asarray(new_im)
        still_living = arr1 * arr2
        still_living = Image.fromarray(still_living)
        # Add the still_living image to the new image.
        # The result is the new state with the values of how long the cells are alive
        self.image = ImageChops.add(new_im, still_living)

    def try_evolve(self, pixel):
        # If the pixel is even, than the pixel was dead and the value/2 is the number of the neighboours
        # If the pixel is odd, than the pixel was alive and the (value - 1)/2 is the number of the neighbours

        # Map the pixel to the new stage

        status = pixel % 2

        if (status != 0):
            if (pixel - (status)) / 2 == 2 or (pixel - (status)) / 2 == 3:
                pixel = 1
            else:
                pixel = 0
        else:
            if pixel / 2 == 3:
                pixel = 1
            else:
                pixel = 0

        return pixel

    def start_evolve(self):
        # Start the scheduled event

        if not self.is_running:
            self.is_running = True
            self.event = Clock.schedule_interval(lambda x: self.filter(x), 1 / self.time)
        else:
            self.stop_evolve()

    def stop_evolve(self):
        # Stop the scheduled event

        self.is_running = False
        Clock.unschedule(self.event)

    def clear(self):
        # Clear the image

        if self.is_running: self.stop_evolve()
        self.image = Image.new('L', (self.size_image, self.size_image), "black")

    def on_is_running(self, istance, value):
        if value:
            self.start_text = "Pause"
        else:
            self.start_text = "Start"

    def on_num_cells(self, instance, value):
        # Change the size of the displayed image
        self.image_to_texture()

    def on_time(self, instance, value):
        # Change the framerate of the simulation
        if self.is_running:
            self.stop_evolve()
            self.start_evolve()

    def on_heatmap(self, instance, value):
        # Change the value of the heatmap variable
        self.image_to_texture()

    def save(self):
        # Save the state saving the current image

        if self.is_running: self.stop_evolve()
        self.image.save("template/My Image.png")

    def load(self, value):
        # Load a pre-done state loading a image

        if self.is_running: self.stop_evolve()
        if value[1] == "Load":
            return

        load_img = Image.open("template/" + value[1] + ".png")
        self.image = Image.new('L', (self.size_image, self.size_image), "black")
        self.image.paste(load_img, (int(self.size_image/2 - load_img.size[1]/2), int(self.size_image/2 - load_img.size[1]/2)))
        self.image_to_texture()
        value[0].text = "Load"

    def on_image(self, instance, value):
        self.image_to_texture()

Model = Model()
