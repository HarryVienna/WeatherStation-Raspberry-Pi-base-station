from kivy.app import App
from kivy.lang import Builder
from itertools import chain

from kivy.graphics.texture import Texture

kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Test color.Test
RelativeLayout:
    BoxLayout
        id: box
        on_kv_post: print(get_color_from_hex("E91E63"))
        canvas:
            Rectangle:
                size: (10,80)
                pos: self.pos
                texture: Test.vertical(get_color_from_hex("#2FC7C6"),get_color_from_hex("#302E97"))
"""



class Test(App):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def build(self):
        return Builder.load_string(kv)



Test().run()