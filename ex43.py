# ex43.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.adapters.models import SelectableDataItem
from kivy.clock import Clock
import subprocess

class DataItem(SelectableDataItem):
    ans = "asdsa"
    def __init__(self, name, **kwargs):
        self.name = name
        super(DataItem, self).__init__(**kwargs)
        self.ans = "heeee"


class Ex43(BoxLayout):
    #data = ""
    #my_data = ListProperty([data])
    routes = ["hello", "this is my new route"]
    selected_value = StringProperty('Select a button')
    #data_items = ListProperty(routes)
    data_items = ListProperty(DataItem.ans)
    counter = 0

    def __init__(self, **kwargs):
        super(Ex43, self).__init__(**kwargs)

        #Ex43.data_items = ["hola"]
        
        
        Clock.schedule_interval(self.update_list_data, 1)
    
    def update_list_data(self, dt):
        Ex43.counter += 1
        Ex43.routes = ["hell2o", "this is my new rout2e"]
        #print("data {}".format(Ex43.my_data))
        print("counter {}".format(Ex43.counter))
        items = Ex43.data_items
        print("items {}".format(type(items)))
    
    #def change(self,change):
    #    self.selected_value = 'Selected: {}'.format(change.text)

class Ex43App(App):
    def build(self):
        return Ex43()

if __name__ == '__main__':
    Ex43App().run()