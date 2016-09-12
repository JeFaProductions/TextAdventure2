import tkinter as tk
import tead.event
import tead.gui
import tead.command

EVENT_SYSTEM = None
ROOT = None
GUI = None
CMD_PARSER = None

def processInput (text):
    args = text.rstrip().lstrip().split()

    # create Event that text was entered on console
    EVENT_SYSTEM.createEvent(
        tead.event.Event(tead.event.TEXT_ENTERED, {'args' : args}))

    EVENT_SYSTEM.processEvents()

if __name__ == '__main__':
    EVENT_SYSTEM = tead.event.EventSystem()

    ROOT = tk.Tk()
    GUI = tead.gui.MainWindow(ROOT)
    GUI.textin.setOnReturn(processInput)

    CMD_PARSER = tead.command.CommandParser(EVENT_SYSTEM, GUI)

    GUI.mainloop()
