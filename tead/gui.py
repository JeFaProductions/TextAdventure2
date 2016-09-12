import tkinter as tk
import os.path

# Global "theme" for all widgets.
conf = dict(
    bg="black", fg="white", selectbackground="grey", insertbackground="white",
    borderwidth=5, font="Courier 8 bold", highlightthickness=0, highlightbackground="yellow",
    inactiveselectbackground="grey")


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

    def putln(self, text):
        self.put(text + self.lb)


class TextOutput(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)


class Inventory(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)

        self.selectedrow = 1

        self.putln("inventory item 1")
        self.putln("inventory item 2")
        self.putln("inventory item 3")

        self.text.bind("<Down>", self._onDown)
        self.text.bind("<Up>", self._onUp)
        self.text.bind("<Right>", lambda e: "break")
        self.text.bind("<Left>", lambda e: "break")
        self.text.bind("<Button-1>", lambda e: "break")
        self.text.bind("<Double-Button-1>", lambda e: "break")
        self.text.bind("<B1-Motion>", lambda e: "break")

        # self.text.tag_add("sel", "1.0", "1.end")

        self._rowmark()

    def _getrowrange(self, row):
        """
        Returns the from and to index for the desired row.

        :param row: String with the desired row.
        :return: List with from and to index.
        """
        fromindex = row + ".0"
        toindex = row + ".end"
        return [fromindex, toindex]

    def _rowmark(self, row=1):
        """
        Sets the new row mark.

        :param row: New row number as integer.
        """
        old = self._getrowrange(str(self.selectedrow))
        new = self._getrowrange(str(row))

        self.text.tag_remove("sel", old[0], old[1])
        self.text.tag_add("sel", new[0], new[1])

        self.selectedrow = row

    def _onUp(self, event):
        if self.selectedrow != 1:
            self._rowmark(self.selectedrow - 1)
        return "break"

    def _onDown(self, event):
        end = int(float(self.text.index("end"))) - 2
        if self.selectedrow < end:
            self._rowmark(self.selectedrow + 1)
        return "break"

    def focus(self):
        """
        Sets the focus to the text field.
        """
        self.text.focus()


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

    def focus(self):
        """
        Sets the focus to the text input field.
        """
        self.text.focus()


class Prompt(tk.Text):
    DEFAULT_PROMPT = ">"

    def __init__(self, master=None):
        super().__init__(master)

        self.setPrompt(self.DEFAULT_PROMPT)

        self.config(width=2, height=1, state="disabled")
        self.config(**conf)

    def setPrompt(self, prompt):
        if len(prompt) is 1:
            self.config(state="normal")
            self.delete("1.0", "1.end")
            self.insert("1.0", prompt)
            self.config(state="disabled")


class InfoBar(tk.Frame):
    bgcolor = "grey"

    def __init__(self, master=None):
        super().__init__(master)

        self.config(height=20, bg=self.bgcolor)

        self.infoleft = tk.Label(self)
        self.infoleft.config(bg=self.bgcolor, font=conf["font"])
        self.infoleft.grid(row=0, column=0, sticky=tk.W)

        self.infocenter = tk.Label(self)
        self.infocenter.config(bg=self.bgcolor, font=conf["font"])
        self.infocenter.grid(row=0, column=1)

        self.inforight = tk.Label(self)
        self.inforight.config(bg=self.bgcolor, font=conf["font"])
        self.inforight.grid(row=0, column=2, sticky=tk.E)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.outleft("https://github.com/JeFaProductions/TextAdventure2")
        self.outcenter("Text Adventure 2")
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

    def outcenter(self, text):
        self.infocenter.config(text=text)

    def outright(self, text):
        self.inforight.config(text=text)


class MainWindow(tk.Frame):
    # TODO: Make accessible from root directory
    ICON_FILE = "res/icon.ico"

    def __init__(self, master=None):
        super().__init__(master)

        self.config(bg="black")

        self.master.title("TEAD")
        self.master.iconbitmap(os.path.normpath(self.ICON_FILE))
        self.master.geometry('{}x{}'.format(800, 600))

        self.infobar = None
        self.textout = None
        self.inventory = None
        self.textprompt = None
        self.textin = None

        self.setupframes()
        self.setupevents()

        self.textin.focus()

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

    def setupevents(self):
        self.master.bind("<Escape>", self._onEscape)
        self.textin.text.bind("<Tab>", self._onTab)
        self.textin.text.bind("<FocusIn>", self._onTextinFocus)
        self.inventory.text.bind("<FocusIn>", self._onInventoryFocus)

    def _onEscape(self, event):
        self.master.quit()

    def _onTab(self, event):
        if self.textin.text.focus_get():
            self.inventory.focus()
        return "break"

    def _onTextinFocus(self, event):
        self.textprompt.setPrompt(">")

    def _onInventoryFocus(self, event):
        self.textprompt.setPrompt("#")

    def set(self, onenter, welcome_text):
        self.textin.setOnEnter(onenter)
        self.textout.put(welcome_text)

    def output(self, text):
        self.textout.put(text)


def loadwelcome(file):
    with open(file) as f:
        text = f.read()
    return text

