# ---------- KIVY TUTORIAL PT 4  ----------
 
# In this part of my Kivy tutorial I'll show how to use
# the ListView, ListAdapter and how to create a toolbar
 
# ---------- studentdb.py  ----------
 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.clock import Clock
import subprocess
 
 
class StudentListButton(ListItemButton):
    pass
 
 
class StudentDB(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    #first_name_text_input = ObjectProperty()
    #last_name_text_input = ObjectProperty()
    student_list = ObjectProperty()
    cnt = 0

    list_2 = []
    def __init__(self, **kwargs):
        super(StudentDB, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_list_data, 1)

    def update_list_data(self, dt):
        list_1 = []
        index = -1
        
        #out = subprocess.check_output("ls /home/fabocode/Documents/myRoutes", shell=True)  # test for Lubuntu
        out = subprocess.check_output("ls /home/pi/Documents/myRoutes", shell=True)  # test for RPi
        sp = out.split(".xlsx")

        
        for i in range(len(sp)):
            if(sp[i] != '\n'):
                list_1.append(sp[i].strip())
        if len(list_1) > len(StudentDB.list_2):
            for i in list_1:
                for x in StudentDB.list_2:
                    if i == x:  # in x:
                        #print("item from list 1 {} is in list 2 {}".format(i, x))
                        break
                else:
                    #print("item from list 1 {} is NOT in list 2".format(i))
                    #items = self.list_adapter.data
                    #item = DataItem(i)
                    #items.append(item)
                    self.student_list.adapter.data.extend([i])
                    StudentDB.list_2.append(i)
                        
        if len(list_1) < len(StudentDB.list_2):
            print("current is smaller ")
            for i in StudentDB.list_2: # list 1
                for x in list_1:    # list 2
                    if i == x: #in x: 
                        index += 1
                        #print("item from list 1 {} is in list 2 {} and the index is {}".format(i, x, index))
                        break
                else:
                    index += 1
                    print("item from list 1 {} is NOT in list 2 and I have to delete it and the index is {}".format(i,index))
                    selection = i
                    self.student_list.adapter.data.remove(selection)
                    #items = self.list_adapter.data
                    #item = DataItem(i)
                    #del items[index]
                    del StudentDB.list_2[index]
        #StudentDB.cnt += 1
        #print("cnt {}".format(StudentDB.cnt))
        #student_name = "hello"
        # Add the student to the ListView
        #self.student_list.adapter.data.extend([student_name])



        # Reset the ListView
        #self.student_list._trigger_reset_populate()

    def submit_student(self):
 
        # Get the student name from the TextInputs
        student_name = self.first_name_text_input.text + " " + self.last_name_text_input.text
 
        # Add the student to the ListView
        self.student_list.adapter.data.extend([student_name])
 
        # Reset the ListView
        self.student_list._trigger_reset_populate()
 
    def delete_student(self, *args):
 
        # If a list item is selected
        if self.student_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text
 
            # Remove the matching item
            self.student_list.adapter.data.remove(selection)
 
            # Reset the ListView
            self.student_list._trigger_reset_populate()
 
    def replace_student(self, *args):
 
        # If a list item is selected
        if self.student_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text
 
            # Remove the matching item
            self.student_list.adapter.data.remove(selection)
 
            # Get the student name from the TextInputs
            student_name = self.first_name_text_input.text + " " + self.last_name_text_input.text
 
            # Add the updated data to the list
            self.student_list.adapter.data.extend([student_name])
 
            # Reset the ListView
            self.student_list._trigger_reset_populate()
 
 
class StudentDBApp(App):
    def build(self):
        return StudentDB()
 
 
dbApp = StudentDBApp()
 
dbApp.run()
