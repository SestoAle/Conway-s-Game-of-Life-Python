
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


    '''text = StringProperty("Start")
    num_cell = NumericProperty(50)
    time = NumericProperty(30)
    heatmap = BooleanProperty(False)
    is_running = BooleanProperty(False)
    arr = ObjectProperty()

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)

        self.img = Image.new('L', (self.num_cell, self.num_cell), "black")

        with self.canvas.after:
            self.bgrect = Rectangle(pos=self.pos, size=(100, 100))

        self.pil_to_texture()

    def on_size(self, *args):
        self.bgrect.pos = self.pos
        self.bgrect.size = self.size

    def pil_to_texture(self):

        if self.heatmap:
            im_bit = self.img.point(lambda p: p > 0 and p*2 + 50)
        else:
            im_bit = self.img.point(lambda p: p > 0 and 255)

        im_resize = im_bit.resize((int(self.size[0]), int(self.size[1])))
        im_rgb = im_resize.convert('RGB')
        texture = Texture.create(size=(int(self.size[0]), int(self.size[1])), colorfmt="rgb")
        arr = np.asanyarray(im_rgb)
        data = arr.tostring()
        texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")
        self.bgrect.texture = texture

    def on_touch_down(self, touch):

        if(not self.collide_point(*touch.pos)):
            return

        self.pixel = self.img.load()
        index = self.transform_coord(touch)

        if self.pixel[index[0], index[1]] == 0:
            self.pixel[index[0], index[1]] = 1
        else:
            self.pixel[index[0], index[1]] = 0

        self.pil_to_texture()


    def on_touch_move(self, touch):

        if (not self.collide_point(*touch.pos)):
            return
        self.pixel = self.img.load()

        index = self.transform_coord(touch)
        try:
            if self.pixel[index[0], index[1]] == 0:
                self.pixel[index[0], index[1]] = 1
        except IndexError:
            print("Move out of bounds")

        self.pil_to_texture()

    def transform_coord(self, touch):

        local_coordinate_x = (touch.pos[0] - Window.size[0] + self.size[0]) / self.size[0]
        local_coordinate_y = (touch.pos[1] - Window.size[1] + self.size[1]) / self.size[1]

        index = []

        index.append(int(local_coordinate_x * (self.num_cell)))
        index.append(int(local_coordinate_y * (self.num_cell)))

        return index

    def filter(self, dt):

        print(dt)

        im_bit = self.img.point(lambda p: p > 0 and 1)

        im_conv = Image.new("L", (self.num_cell + 2, self.num_cell + 2), "black")
        im_conv.paste(im_bit, (1,1))

        new_im = im_conv.filter(ImageFilter.Kernel((3, 3), [2, 2, 2, 2, 1, 2, 2, 2, 2], 1, 0))
        new_im = new_im.crop((1,1,self.num_cell + 1, self.num_cell + 1))

        new_im = new_im.point(self.try_evolve)

        arr1 = np.asarray(self.img)
        arr2 = np.asarray(new_im)
        still_living = arr1*arr2
        still_living = Image.fromarray(still_living)
        self.img = ImageChops.add(new_im, still_living)

        self.pil_to_texture()

    def stop_evolve(self):
        self.is_running = False
        Clock.unschedule(self.filter)

    def start_evolve(self):
        if not self.is_running:
            self.is_running = True
            Clock.schedule_interval(self.filter, 1/self.time)
        else:
            self.stop_evolve()

    def clear(self):
        self.stop_evolve()
        self.img = Image.new('L', (self.num_cell, self.num_cell), "black")
        self.pil_to_texture()

    def on_is_running(self, istance, value):
        if value: self.text = "Stop"
        else: self.text = "Start"

    def try_evolve(self, pixel):

        status = pixel%2

        if(status != 0):
            if(pixel-(status))/2 == 2 or (pixel-(status))/2 == 3:
                pixel = 1
            else:
                pixel = 0
        else:
            if pixel/2 == 3:
                pixel = 1
            else:
                pixel = 0

        return pixel

    def on_num_cell(self, instance, new_size):
        old_size, old_height = self.img.size
        new_im = Image.new("L", (new_size, new_size), "black")
        new_im.paste(self.img, (int((new_size - old_size)/2), int((new_size - old_size)/2)))
        self.img = new_im
        self.pil_to_texture()

    def on_time(self, instance, value):
        if self.is_running:
            Clock.unschedule(self.filter)
            Clock.schedule_interval(self.filter, 1/self.time)


    def on_heatmap(self, instance, value):
        self.pil_to_texture()

    def save(self):
        if self.is_running: self.stop_evolve()
        self.img.save("template/saved.png")

    def load(self, value):
        if self.is_running: self.stop_evolve()
        self.img = Image.open("template/" + value[1] + ".png")
        self.on_num_cell(None, self.num_cell)
        self.pil_to_texture()
        
        

    def on_cols(self, value, pos):

        self.rows = self.cols

        self.clear_widgets()

        for i in range(0, self.cols * self.cols):
            self.add_widget(BoxTable(self.cols * self.cols - i - 1))

        index_mat = (np.asmatrix(range(self.cols*self.cols-1, -1, -1))).reshape(self.cols,self.cols)

        for x, y in product(range(self.cols), range(self.cols)):
            for i, j in product(range(1,-2,-1), range(1,-2,-1)):
                if i != 0 or j != 0:
                    try:
                        if(x+i >= 0 and y+j >= 0):
                            self.children[index_mat[x,y]].set_neighborhood(self.children[index_mat[x+i, y+j]])
                    except IndexError:
                        continue

        print(index_mat)
        print(index_mat[-1,4])


    def let_evolve(self, frame):

        print(frame)
        for child in self.children:
            child.try_evolve()
        for child in self.children:
            child.evolve() '''
