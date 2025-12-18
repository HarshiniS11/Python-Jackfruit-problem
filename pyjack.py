import wx

tasks = []
completed_tasks = []


class CompletedTasksFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Completed Tasks", size=(400, 450))

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#f3e5f5")

        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Completed Tasks")
        title.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour("#4a148c")
        vbox.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        # -------- SCROLLABLE COMPLETED TASK AREA -------- #
        scroll = wx.ScrolledWindow(panel, style=wx.HSCROLL | wx.VSCROLL)
        scroll.SetScrollRate(10, 10)
        scroll.SetBackgroundColour("#ffffff")

        scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        if not completed_tasks:
            msg = wx.StaticText(scroll, label="No tasks completed yet.")
            msg.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT,
                                 wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            scroll_sizer.Add(msg, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        else:
            for task in completed_tasks:
                lbl = wx.StaticText(scroll, label="• " + task)
                lbl.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,
                                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                scroll_sizer.Add(lbl, 0, wx.ALL | wx.ALIGN_CENTER, 8)

        scroll.SetSizer(scroll_sizer)
        scroll.FitInside()

        vbox.Add(scroll, 1, wx.ALL | wx.EXPAND, 15)

        panel.SetSizer(vbox)
        self.Show()


class TodoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="To-Do List with Checkboxes", size=(450, 600))

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#e8f4fc")

        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="My To-Do List")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        self.entry = wx.TextCtrl(panel)
        self.entry.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(self.entry, 0, wx.ALL | wx.EXPAND, 15)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)

        add_btn = wx.Button(panel, label="Add Task", size=(150, 40))
        add_btn.SetBackgroundColour("#1976d2")
        add_btn.SetForegroundColour("white")
        add_btn.Bind(wx.EVT_BUTTON, self.add_task)

        del_btn = wx.Button(panel, label="Delete Completed", size=(150, 40))
        del_btn.SetBackgroundColour("#d32f2f")
        del_btn.SetForegroundColour("white")
        del_btn.Bind(wx.EVT_BUTTON, self.delete_completed)

        btn_box.Add(add_btn, 0, wx.ALL, 5)
        btn_box.Add(del_btn, 0, wx.ALL, 5)

        vbox.Add(btn_box, 0, wx.ALIGN_CENTER)

        show_btn = wx.Button(panel, label="Show Completed", size=(320, 40))
        show_btn.SetBackgroundColour("#388e3c")
        show_btn.SetForegroundColour("white")
        show_btn.Bind(wx.EVT_BUTTON, self.show_completed)

        vbox.Add(show_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # -------- SCROLLABLE TASK AREA (H + V) -------- #
        self.task_panel = wx.ScrolledWindow(panel, style=wx.HSCROLL | wx.VSCROLL)
        self.task_panel.SetScrollRate(10, 10)
        self.task_panel.SetBackgroundColour("#f8bbd0")

        self.task_sizer = wx.BoxSizer(wx.VERTICAL)
        self.task_panel.SetSizer(self.task_sizer)

        vbox.Add(self.task_panel, 1, wx.ALL | wx.EXPAND, 15)

        panel.SetSizer(vbox)
        self.Show()

    def add_task(self, event):
        text = self.entry.GetValue().strip()
        if not text:
            return

        if text.lower() in [t[2].lower() for t in tasks]:
            wx.MessageBox(
                "TASK IS ALREADY PRESENT IN TO-DO LIST",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
            return

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        checkbox = wx.CheckBox(self.task_panel, label=text)
        checkbox.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        hbox.AddStretchSpacer(1)
        hbox.Add(checkbox, 0, wx.ALL | wx.ALIGN_CENTER, 8)
        hbox.AddStretchSpacer(1)

        self.task_sizer.Add(hbox, 0, wx.EXPAND)

        self.task_panel.FitInside()
        self.task_panel.Layout()

        tasks.append((checkbox, hbox, text))
        self.entry.SetValue("")

    def delete_completed(self, event):
        global tasks, completed_tasks
        new_tasks = []

        for checkbox, box, text in tasks:
            if checkbox.GetValue():
                completed_tasks.append(text)
                box.Clear(True)
            else:
                new_tasks.append((checkbox, box, text))

        tasks = new_tasks
        self.task_panel.FitInside()
        self.task_panel.Layout()

    def show_completed(self, event):
        CompletedTasksFrame(self)


# -------- RUN APP -------- #
app = wx.App(False)
TodoFrame()
app.MainLoop()
