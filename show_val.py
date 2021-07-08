from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, BooleanProperty

class Show_Val(Screen):
    message = StringProperty('')
    timer_update = StringProperty('')
    timer_2show_screen = StringProperty('')
    dist_travel = StringProperty('')
    count_down_up = StringProperty('') #average_mph = StringProperty('')
    temp_val = StringProperty('')
    dist_travel_2 = StringProperty('')
    tpms_temp = StringProperty('')
    tpms_pressure = StringProperty('')
    current_color = ListProperty()
    current_value = StringProperty('')
    show_me_data = StringProperty('')
    tire_size = StringProperty('')
    switch_ref = StringProperty('')
    gps_color = ListProperty()
    text_gps = StringProperty('')
    clear_text_input = StringProperty('')
    color_text_gps = ListProperty()
    press_indicator = StringProperty('')
    temperature_indicator = StringProperty('')
    enable_toggle_button = BooleanProperty(False)
    speed_target_indicator = StringProperty()
    pulseCounter = StringProperty('')
    saveRouteInUSB = StringProperty('')
    loadRouteInList = StringProperty('')
    rpi_temp = StringProperty('')
    hidePulseMeasure = BooleanProperty(False)

    