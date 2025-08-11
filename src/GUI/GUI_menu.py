import tkinter as tk


class GuiMenu(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        self.menubar = tk.Menu(parent)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open File",
            command=lambda: gui_main.open_file(),
            accelerator="Ctrl+O",
        )
        parent.bind_all("<Control-o>", lambda x: gui_main.open_file())

        self.filemenu.add_command(
            label="Save File As...",
            command=lambda: gui_main.save_file_as(),
            accelerator="Ctrl+S",
        )
        parent.bind_all("<Control-o>", lambda x: gui_main.open_file())

        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=lambda: gui_main.quit_program(), accelerator="Ctrl+Q")
        parent.bind_all("<Control-q>", lambda x: gui_main.quit_program())

        # options submenu
        self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="Export Font Image", command=lambda: gui_main.export_font_image())
        self.toolsmenu.add_command(label="Import Font Image", command=lambda: gui_main.import_font_image())

        # help submenu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=lambda: gui_main.show_about_window())

        # main menu
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        parent.config(menu=self.menubar)
