import tkinter as tk
from tkinter import font

class ReadonlyText(tk.Frame):
    lb = "\r\n"

    def __init__(self, master=None):
        super().__init__(master)

        font = tk.font.Font(family="Courier", size=12, weight="bold")

        self.text = tk.Text(self)
        self.text.config(bg="black", fg="white", selectbackground="grey", insertbackground="white")
        self.text.config(state="disabled", borderwidth=5, wrap=tk.WORD, font=font)

        self.text.bind("<Double-Button-1>", lambda e: "break")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

    def put(self, text):
        self.text.config(state="normal")
        self.text.insert("end", text)
        self.text.config(state="disabled")


class TextOutput(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)

        self.put("> Hello" + self.lb)


class Inventory(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)


class TextInput(tk.Frame):
    prompt = "> "

    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)

        self.text.config(bg="black", fg="white", insertbackground="white", insertunfocussed="solid")
        self.text.config(borderwidth=5, height=1, wrap="none")
        # self.text.insert(0.0, self.prompt)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.text.bind("<Return>", self._onEnter)
        # self.text.bind("<BackSpace>", self._onLeft)
        # self.text.bind("<Left>", self._onLeft)
        # self.text.bind("<Button-1>", self._onClick)
        # self.text.bind("<Double-Button-1>", self._onClick)
        # self.text.bind("<B1-Motion>", self._onClick)

        self.onEnterfun = None

    def _onEnter(self, event):
        if self.onEnterfun is not None:
            pass  # self.onEnterfun(self.text.)
        else:
            return "break"

    # def _onLeft(self, event):
    #     index = self._getIndex(event.x, event.y)
    #     if index == 1.2:
    #         return "break"

    # def _onClick(self, event):
    #     index = float(self.text.index("@" + str(event.x) + "," + str(event.y)))
    #     if index <= 1.1:
    #         return "break"
    #
    # def _getIndex(self, x, y):
    #     return float(self.text.index("@" + str(x) + "," + str(y)))

    def setOnEnter(self, fun):
        self.onEnterfun = fun


class InfoBar(tk.Frame):
    bgcolor = "grey"

    def __init__(self, master=None):
        super().__init__(master)

        self.config(height=20)
        self.config(bg=self.bgcolor, borderwidth=5)

        self.info1 = tk.Label(self)
        self.info1.config(text="Hello", bg=self.bgcolor)
        self.info1.grid(row=0, column=0, sticky=tk.W)

        self.info2 = tk.Label(self)
        self.info2.config(text="HI", bg=self.bgcolor)
        self.info2.grid(row=0, column=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.setupevents()

    def setupevents(self):
        # Move window
        self.bind("<ButtonPress-1>", self.startMove)
        self.bind("<ButtonRelease-1>", self.stopMove)
        self.bind("<B1-Motion>", self.onMotion)

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def onMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_toplevel().winfo_x() + deltax
        y = self.winfo_toplevel().winfo_y() + deltay
        self.winfo_toplevel().geometry("+%s+%s" % (x, y))


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.config(bg="black")

        # self.master.overrideredirect(True)
        self.master.title("TEAD")
        self.master.geometry('{}x{}'.format(800, 600))

        self.textout = None
        self.inventory = None

        self.setupframes()

        self.master.bind("<Escape>", self.onEscape)

    def setupframes(self):
        self.master.config(bg="black", borderwidth=1)

        # Make it resizable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Only one column in main frame
        self.columnconfigure(0, weight=1)  # Resizable
        self.rowconfigure(1, weight=1)  # midframe resizable
        self.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.infobar = InfoBar(self)
        self.infobar.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        midframe = tk.Frame(self)

        # All resizable
        midframe.rowconfigure(0, weight=1)
        midframe.columnconfigure(0, weight=1)
        midframe.columnconfigure(1, weight=2)

        self.textout = TextOutput(midframe)
        self.textout.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.inventory = Inventory(midframe)
        self.inventory.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

        midframe.grid(row=1, column=0, sticky=tk.N + tk.E + tk.W + tk.S)

        bottomframe = tk.Frame(self)
        bottomframe.columnconfigure(1, weight=1)

        self.textprompt = tk.Text(bottomframe)
        self.textprompt.insert(0.0, ">")
        self.textprompt.config(width=2, height=1, bg="black", fg="white",
                               insertbackground="white", insertunfocussed="solid",
                               borderwidth=5, state="disabled")
        self.textprompt.grid(row=0, column=0)

        self.textin = TextInput(bottomframe)
        self.textin.grid(row=0, column=1, sticky=tk.N + tk.W + tk.E + tk.S)

        bottomframe.grid(row=2, column=0, sticky=tk.N + tk.E + tk.W + tk.S)

    def onEscape(self, event):
        self.master.quit()


root = tk.Tk()
gui = MainWindow(root)
gui.mainloop()
