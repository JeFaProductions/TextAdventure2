import tkinter as tk


class ReadonlyText(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)
        self.text.config(bg="black", fg="white")
        self.text.config(state="disabled")
        self.text.config(borderwidth=5, selectbackground="white")

        self.text.pack()

    def put(self, text):
        self.text.config(state="normal")
        self.text.insert("end", text)
        self.text.config(state="disabled")


class TextOutput(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)

        self.text.config(width=60, height=20)

        self.put("> Hello" + "\r\n")

        self.pack(side="left")


class Inventory(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)

        self.text.config(height=20)

        self.pack(side="right")


class TextInput(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text()

        self.text.config(bg="black", fg="white", borderwidth=5, height=1)
        self.text.insert(0.0, "> ")

        self.text.pack(side="bottom", expand=1)
        self.pack(expand=1)


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.overrideredirect(True)

        self.textout = None
        self.inventory = None

        self.setupframes()
        self.setupevents()

    def setupframes(self):
        self.master.config(bg="black", borderwidth=0)
        self.master.maxsize(800, 600)

        topframe = tk.Frame(self)
        self.textout = TextOutput(topframe)
        self.inventory = Inventory(topframe)
        topframe.pack()

        self.textin = TextInput(self)

        self.pack()

    def setupevents(self):
        # Move window
        self.master.bind("<ButtonPress-1>", self.startMove)
        self.master.bind("<ButtonRelease-1>", self.stopMove)
        self.master.bind("<B1-Motion>", self.onMotion)

        self.master.bind("<Escape>", self.onEscape)

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def onMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry("+%s+%s" % (x, y))

    def onEscape(self, event):
        self.master.quit()


root = tk.Tk()
gui = MainWindow(root)
gui.mainloop()
