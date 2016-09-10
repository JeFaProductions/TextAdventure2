import tkinter as tk

# Global "theme" for all widgets.
conf = dict(
    bg="black", fg="white", selectbackground="grey", insertbackground="white",
    borderwidth=5, font="System 8 bold")


class ReadonlyText(tk.Frame):
    lb = "\r\n"

    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)

        self.text.config(state="disabled", wrap=tk.WORD)
        self.text.config(**conf)

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

        self.put("inventory")


class TextInput(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)

        self.text.config(height=1, wrap="none")
        self.text.config(**conf)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.text.bind("<Return>", self._onEnter)

        self.onEnterFun = None

    def _onEnter(self, event):
        if self.onEnterFun is not None:
            self.onEnterFun(self.text.get(1.0, tk.END))
            self.text.delete(1.0, tk.END)
        return "break"

    def setOnEnter(self, fun):
        self.onEnterFun = fun


class Prompt(tk.Text):
    DEFAULT_PROMPT = ">"

    def __init__(self, master=None):
        super().__init__(master)

        self.setPrompt(self.DEFAULT_PROMPT)

        self.config(width=2, height=1, state="disabled")
        self.config(**conf)

    def setPrompt(self, prompt):
        if len(prompt) is 1:
            self.delete(1.0, tk.END)
            self.insert(1.0, prompt)


class InfoBar(tk.Frame):
    bgcolor = "grey"

    def __init__(self, master=None):
        super().__init__(master)

        self.config(height=20, bg=self.bgcolor)

        self.infoleft = tk.Label(self)
        self.infoleft.config(bg=self.bgcolor, font=conf["font"])
        self.infoleft.grid(row=0, column=0, sticky=tk.W)

        self.inforight = tk.Label(self)
        self.inforight.config(bg=self.bgcolor, font=conf["font"])
        self.inforight.grid(row=0, column=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.outleft("Text Adventure 2")
        self.outright("GUI prototype")

        self._setupevents()

    def _setupevents(self):
        # Move window
        self.bind("<ButtonPress-1>", self._startMove)
        self.bind("<ButtonRelease-1>", self._stopMove)
        self.bind("<B1-Motion>", self._onMotion)

    def _startMove(self, event):
        self.x = event.x
        self.y = event.y

    def _stopMove(self, event):
        self.x = None
        self.y = None

    def _onMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_toplevel().winfo_x() + deltax
        y = self.winfo_toplevel().winfo_y() + deltay
        self.winfo_toplevel().geometry("+%s+%s" % (x, y))

    def outleft(self, text):
        self.infoleft.config(text=text)

    def outright(self, text):
        self.inforight.config(text=text)


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.config(bg="black")

        self.master.title("TEAD")
        self.master.geometry('{}x{}'.format(800, 600))

        self.infobar = None
        self.textout = None
        self.inventory = None
        self.textprompt = None
        self.textin = None

        self.setupframes()

        self.master.bind("<Escape>", self._onEscape)

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

        self.textprompt = Prompt(bottomframe)
        self.textprompt.grid(row=0, column=0)

        self.textin = TextInput(bottomframe)
        self.textin.grid(row=0, column=1, sticky=tk.N + tk.W + tk.E + tk.S)

        bottomframe.grid(row=2, column=0, sticky=tk.N + tk.E + tk.W + tk.S)

    def _onEscape(self, event):
        self.master.quit()

    def set(self, onenter):
        self.textin.setOnEnter(onenter)

    def output(self, text):
        self.textout.put(text)


if __name__ == '__main__':
    root = tk.Tk()
    gui = MainWindow(root)

    gui.set(lambda text: gui.output(text))

    gui.mainloop()
