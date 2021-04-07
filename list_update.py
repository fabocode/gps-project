# -*- coding: utf-8 -*-
from kivy.uix.listview import ListView
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.models import SelectableDataItem
import subprocess
from kivy.uix.listview import ListItemButton

import random

class DataItem(SelectableDataItem):
    def __init__(self, name, **kwargs):
        self.name = name
        super(DataItem, self).__init__(**kwargs)


class MainView(FloatLayout):
    """
    Implementation of a ListView using the kv language.
    """

    list_2 = []

    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)

        data_items = []

        list_item_args_converter = lambda row_index, obj: {'text': obj.name,
                                                           'size_hint_y': None,
                                                           'height': 25}

        self.list_adapter = \
                ListAdapter(data=data_items,
                            args_converter=list_item_args_converter,
                            selection_mode='single',
                            propagate_selection_to_data=False,
                            allow_empty_selection=False,
                            cls=ListItemButton)

        self.list_view = ListView(adapter=self.list_adapter)

        self.add_widget(self.list_view)

        self.toggle = 'adding'

        Clock.schedule_interval(self.update_list_data, 1)

    def update_list_data(self, dt):
        list_1 = []
        index = -1

        out = subprocess.check_output("ls /home/pi/Documents/myRoutes", shell = True)   # Save devices plugged to device into "out"
        sp = out.split(".xlsx")

        for i in range(len(sp)):
            if(sp[i] != '\n'):
                list_1.append(sp[i].strip())
        if len(list_1) > len(MainView.list_2):
            for i in list_1:
                for x in MainView.list_2:
                    if i == x: #in x:
                        #print("item from list 1 {} is in list 2 {}".format(i, x))
                        break
                else:
                    #print("item from list 1 {} is NOT in list 2".format(i))
                    items = self.list_adapter.data
                    item = DataItem(i)
                    items.append(item)
                    MainView.list_2.append(i)

        if len(list_1) < len(MainView.list_2):
            print("current is smaller ")
            for i in MainView.list_2: # list 1
                for x in list_1:    # list 2
                    if i == x: #in x: 
                        index += 1
                        #print("item from list 1 {} is in list 2 {} and the index is {}".format(i, x, index))
                        break
                else:
                    index += 1
                    print("item from list 1 {} is NOT in list 2 and I have to delete it and the index is {}".format(i,index))
                    items = self.list_adapter.data
                    item = DataItem(i)
                    del items[index]
                    del MainView.list_2[index]

        print("new {}".format(list_1))
        print("")
        print("old {}".format(MainView.list_2))
        print("")


if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))