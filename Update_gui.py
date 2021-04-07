import GUI as gui
import time

main = gui.Main_Screen

init_gui = main()

while True:
    main.update(init_gui)
    time.sleep(0.02)
