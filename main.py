import tkinter as tk
import pyfiglet
import tead.gui

if __name__ == '__main__':
    root = tk.Tk()
    gui = tead.gui.MainWindow(root)


    def handle(text):
        if text.rstrip() == "start":
            figlet = pyfiglet.Figlet("starwars")
            gui.output(figlet.renderText("nope"))
            gui.output("\r\n")


    welcomefile = "res/welcome_text"
    gui.set(handle, tead.gui.loadwelcome(welcomefile))

    gui.mainloop()