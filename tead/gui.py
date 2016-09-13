import tkinter as tk
import os

# Global configuration parameters to easily change the style.
config = dict(
    # Global "theme" for all widgets.
    theme=dict(
        bg="black",
        fg="white",
        selectbackground="grey",
        insertbackground="white",
        borderwidth=3,
        font="Courier 9 bold",
        highlightthickness=0,
        highlightbackground="yellow",
        inactiveselectbackground="grey",
    ),
    # File path, text, etc.
    files=dict(
        icon_file_win="res/icon.ico",
        icon_file_linux="res/icon.xbm",
        welcome_text_file="res/welcome_text",
        title="TEAD",
        default_width=800,
        default_height=600,
        default_infoleft="https://github.com/JeFaProductions/TextAdventure2",
        default_infocenter="Text Adventure 2",
        default_inforight="GUI prototype",
        default_prompt=">"
    )
)


class ReadonlyText(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)

        self.text.config(state="disabled", wrap=tk.WORD)
        self.text.config(**config["theme"])

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

    def delete(self, indexfrom, indexto):
        """
        Deletes text in the output field.

        :param indexfrom: Tkinter index
        :param indexto:  Tkinter index
        """
        self.text.config(state="normal")
        self.text.delete(indexfrom, indexto)
        self.text.config(state="disabled")

    def put(self, text):
        self.text.config(state="normal")
        self.text.insert("end", text)
        self.text.config(state="disabled")

    def putln(self, text):
        """
        Adds a linebreak to the text and prints it on the output field.

        :param text: String
        """
        self.put(text + os.linesep)


class TextOutput(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)


class Inventory(ReadonlyText):
    def __init__(self, master=None):
        super().__init__(master)

        self.selectedrow = 1

        self.addItem("inventory item 1")
        self.addItem("inventory item 2")
        self.addItem("inventory item 3")
        self.deleteItem("inventory item 2")

        self.text.bind("<Down>", self._onDown)
        self.text.bind("<Up>", self._onUp)
        self.text.bind("<Right>", lambda e: "break")
        self.text.bind("<Left>", lambda e: "break")
        self.text.bind("<Button-1>", lambda e: "break")
        self.text.bind("<Double-Button-1>", lambda e: "break")
        self.text.bind("<B1-Motion>", lambda e: "break")

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

    def addItem(self, name):
        self.putln(name)

    def deleteItem(self, name):
        pos = self.text.search(name, "1.0", "end")
        if self.selectedrow == int(float(pos)):
            if self.selectedrow > 1:
                self._onUp()
            else:
                self._onDown()

        self.delete(pos, pos + "+1lines")


class TextInput(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.text = tk.Text(self)

        self.text.config(height=1, wrap="none")
        self.text.config(**config["theme"])

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.text.bind("<Return>", self._onReturn)

        self._onReturnCB = None

    def _onReturn(self, event):
        if self._onReturnCB is not None:
            self._onReturnCB(self.text.get(1.0, tk.END))
            self.text.delete(1.0, tk.END)
        return "break"

    def setOnReturn(self, cb):
        self._onReturnCB = cb

    def focus(self):
        """
        Sets the focus to the text input field.
        """
        self.text.focus()


class Prompt(tk.Text):
    def __init__(self, master=None):
        super().__init__(master)

        self.setPrompt(config["files"]["default_prompt"])

        self.config(width=2, height=1, state="disabled")
        self.config(**config["theme"])

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

        font = config["theme"]["font"]

        self.infoleft = tk.Label(self)
        self.infoleft.config(bg=self.bgcolor, font=font)
        self.infoleft.grid(row=0, column=0, sticky=tk.W)

        self.infocenter = tk.Label(self)
        self.infocenter.config(bg=self.bgcolor, font=font)
        self.infocenter.grid(row=0, column=1)

        self.inforight = tk.Label(self)
        self.inforight.config(bg=self.bgcolor, font=font)
        self.inforight.grid(row=0, column=2, sticky=tk.E)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.outleft(config["files"]["default_infoleft"])
        self.outcenter(config["files"]["default_infocenter"])
        self.outright(config["files"]["default_inforight"])

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
    def __init__(self, master=None):
        super().__init__(master)

        self.infobar = None
        self.textout = None
        self.inventory = None
        self.textprompt = None
        self.textin = None

        self._setupstyle()
        self._setupframes()
        self._setupevents()

        welcomefile = config["files"]["welcome_text_file"]
        with open(welcomefile) as f:
            text = f.read()
        self.output(text)

        self.textin.focus()

    def _setupstyle(self):
        self.config(bg="black")

        self.master.title(config["files"]["title"])

        if os.name == "nt":
            self.master.wm_iconbitmap(
                bitmap=os.path.normpath(config["files"]["icon_file_win"]))
        else:
            self.master.wm_iconbitmap(
                bitmap="@" + os.path.normpath(config["files"]["icon_file_linux"]))

        self.master.geometry('{}x{}'.format(
            config["files"]["default_width"],
            config["files"]["default_height"]))

    def _setupframes(self):
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

    def _setupevents(self):
        # GUI events
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

    def output(self, text):
        """
        Prints the the text on the output text field.

        :param text: String
        """
        self.textout.put(text)
