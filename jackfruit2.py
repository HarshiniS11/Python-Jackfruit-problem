import wx

tasks = []              
completed_tasks = []    


class CompletedTasksFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Completed Tasks", size=(350, 400))
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#f3e5f5")

        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Completed Tasks")
        title.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour("#4a148c")
        vbox.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        if not completed_tasks:
            msg = wx.StaticText(panel, label="No tasks completed yet.")
            msg.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                 wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            vbox.Add(msg, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        else:
            for task in completed_tasks:
                lbl = wx.StaticText(panel, label="• " + task)
                lbl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                vbox.Add(lbl, 0, wx.ALL, 5)

        panel.SetSizer(vbox)
        self.Show()


class TodoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="To-Do List with Checkboxes", size=(420, 550))
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#e8f4fc")

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="My To-Do List")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        # Entry box
        self.entry = wx.TextCtrl(panel)
        self.entry.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(self.entry, 0, wx.ALL | wx.EXPAND, 15)

        # Buttons
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

        # Task list panel
        self.task_panel = wx.Panel(panel)
        self.task_panel.SetBackgroundColour("#e8f4fc")
        self.task_sizer = wx.BoxSizer(wx.VERTICAL)
        self.task_panel.SetSizer(self.task_sizer)

        vbox.Add(self.task_panel, 1, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(vbox)
        self.Show()

    def add_task(self, event):
        text = self.entry.GetValue().strip()
        if not text:
            return

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        checkbox = wx.CheckBox(self.task_panel, label=text)
        checkbox.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        hbox.Add(checkbox, 0, wx.ALL, 5)

        self.task_sizer.Add(hbox, 0, wx.EXPAND)
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
        self.task_panel.Layout()

    def show_completed(self, event):
        CompletedTasksFrame(self)


# Run App
app = wx.App(False)
TodoFrame()
app.MainLoop()