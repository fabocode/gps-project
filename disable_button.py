from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""
<Example>:
    cols: 3
    Button:
        text: "Disable right button"
        on_press: my_button.enabled = False
    Button:
        text: "enabled right button"
        on_press: my_button.enabled = True
    MyButton:
        id: my_button
        text: "My button"
        on_press: print "It is enabled"
""")

class MyButton(Button):
    enabled = BooleanProperty(True)

    def on_enabled(self, instance, value):
        if value:
            self.background_color = [1,1,1,1]
            self.color = [1,1,1,1]
        else:
            self.background_color = [1,1,1,.3]
            self.color = [1,1,1,.5]

    def on_touch_down( self, touch ):
        if self.enabled:
            return super(self.__class__, self).on_touch_down(touch)

class Example(GridLayout):    
    pass

class MyApp(App):
    def build(self):
        return Example()

if __name__=="__main__":
    MyApp().run()