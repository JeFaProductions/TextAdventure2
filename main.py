import tkinter as tk
import tead.event
import tead.gui
import tead.command

if __name__ == '__main__':
    eventSystem = tead.event.EventSystem()
    root = tk.Tk()
    gui = tead.gui.MainWindow(eventSystem, root)
    cmdParser = tead.command.CommandParser(eventSystem, gui)
    
    gui.mainloop()