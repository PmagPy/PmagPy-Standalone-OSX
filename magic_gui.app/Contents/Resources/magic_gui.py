#!/usr/bin/env pythonw
"""
doc string
"""

# pylint: disable=C0103,E402
print '-I- Importing MagIC GUI dependencies'
import matplotlib
if not matplotlib.get_backend() == 'WXAgg':
    matplotlib.use('WXAgg')
import wx
import wx.lib.buttons as buttons
import sys
import os
import pmagpy
from pmagpy import data_model3
from pmagpy import validate_upload3 as val_up3
from pmagpy import pmag
from pmagpy import ipmag

from dialogs import pmag_widgets as pw
from dialogs import magic_grid3 as magic_grid
from dialogs import pmag_menu_dialogs
from dialogs import grid_frame3 as grid_frame
from pmagpy import new_builder as nb


class MainFrame(wx.Frame):
    """
    MagIC GUI
    """

    def __init__(self, WD=None, name='Main Frame', dmodel=None):
        try:
            version = pmag.get_version()
        except:
            version = ""
        title = "MagIC GUI   version: %s" % version
        if sys.platform in ['win32', 'win64']:
            title += "  Powered by Enthought Canopy"
        wx.Frame.__init__(self, None, wx.ID_ANY, title, name=name)
        #
        self.grid_frame = None
        self.panel = wx.Panel(self, size=wx.GetDisplaySize(), name='main panel')
        print '-I- Fetching working directory'
        self.WD = os.path.realpath(WD) or os.getcwd()

        print '-I- Initializing magic data model'
        if dmodel is None:
            dmodel = data_model3.DataModel()
        self.data_model = dmodel

        self.edited = False
        self.validation_mode = False

        print '-I- Initializing interface'
        self.InitUI()

        print '-I- Completed interface'
        wx.CallAfter(self.get_wd_data)

    def get_wd_data(self):
        wait = wx.BusyInfo('Reading in data from current working directory, please wait...')
        wx.Yield()
        print '-I- Read in any available data from working directory'
        self.contribution = nb.Contribution(self.WD, dmodel=self.data_model)
        del wait


    def InitUI(self):
        """
        Make main user interface
        """
        bSizer0 = wx.StaticBoxSizer(
            wx.StaticBox(self.panel, wx.ID_ANY, "Choose MagIC project directory", name='bSizer0'), wx.HORIZONTAL
        )
        self.dir_path = wx.TextCtrl(self.panel, id=-1, size=(600, 25), style=wx.TE_READONLY)
        self.dir_path.SetValue(self.WD)
        self.change_dir_button = buttons.GenButton(
            self.panel, id=-1, label="change directory", size=(-1, -1), name='change_dir_btn'
        )
        self.change_dir_button.SetBackgroundColour("#F8F8FF")
        self.change_dir_button.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_change_dir_button, self.change_dir_button)
        bSizer0.Add(self.change_dir_button, wx.ALIGN_LEFT)
        bSizer0.AddSpacer(40)
        bSizer0.Add(self.dir_path, wx.ALIGN_CENTER_VERTICAL)

        self.bSizer_msg = wx.StaticBoxSizer(wx.StaticBox(
            self.panel, wx.ID_ANY, "Message", name='bsizer_msg'),
                                            wx.HORIZONTAL)
        self.message = wx.StaticText(self.panel, -1,
                                     label="Some text will be here",
                                     name='messages')
        self.bSizer_msg.Add(self.message)

        #---sizer 1 ----
        bSizer1 = wx.StaticBoxSizer(wx.StaticBox(
            self.panel, wx.ID_ANY, "Add information to the data model", name='bSizer1'),
                                    wx.HORIZONTAL)

        text = "1. add location data"
        self.btn1 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='locations_btn')
        self.btn1.SetBackgroundColour("#FDC68A")
        self.btn1.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn1)

        text = "2. add site data"
        self.btn2 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='sites_btn')
        self.btn2.SetBackgroundColour("#6ECFF6")
        self.btn2.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn2)


        text = "3. add sample data"
        self.btn3 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='samples_btn')
        self.btn3.SetBackgroundColour("#C4DF9B")
        self.btn3.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn3)


        text = "4. add specimen data"
        self.btn4 = buttons.GenButton(self.panel, id=-1,
                                      label=text, size=(300, 50), name='specimens_btn')
        self.btn4.SetBackgroundColour("#FDC68A")
        self.btn4.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn4)


        text = "5. add age data"
        self.btn5 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='ages_btn')
        self.btn5.SetBackgroundColour("#6ECFF6")
        self.btn5.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn5)

        #text = "6. add results data"
        #self.btn6 = buttons.GenButton(self.panel, id=-1, label=text,
        #                              size=(300, 50), name='result_btn')
        #self.btn6.SetBackgroundColour("#C4DF9B")
        #self.btn6.InitColours()
        #self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn6)

        bsizer1a = wx.BoxSizer(wx.VERTICAL)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn1, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn2, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn3, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)

        bSizer1.Add(bsizer1a, wx.ALIGN_CENTER, wx.EXPAND)
        bSizer1.AddSpacer(20)

        #bSizer1.Add(OR, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)
        bsizer1b = wx.BoxSizer(wx.VERTICAL)
        #__init__(self, parent, id, label, pos, size, style, validator, name
        bsizer1b.Add(self.btn4, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)
        bsizer1b.Add(self.btn5, 0, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)
        #bsizer1b.Add(self.btn6, 0, wx.ALIGN_CENTER, 0)
        bSizer1.Add(bsizer1b, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)

        #---sizer 2 ----

        bSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, "Upload to MagIC database", name='bSizer2'), wx.HORIZONTAL)

        text = "prepare upload txt file"
        self.btn_upload = buttons.GenButton(self.panel, id=-1, label=text,
                                            size=(300, 50), name='upload_btn')
        self.btn_upload.SetBackgroundColour("#C4DF9B")
        self.btn_upload.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_upload_file, self.btn_upload)

        bSizer2.AddSpacer(20)
        bSizer2.Add(self.btn_upload, 0, wx.ALIGN_CENTER, 0)
        bSizer2.AddSpacer(20)
        #self.Bind(wx.EVT_BUTTON, self.on_btn_upload, self.btn_upload)


        #---arrange sizers ----

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        #vbox.Add(self.logo,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(5)
        vbox.Add(bSizer0, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)
        #vbox.Add(bSizer0_1, 0, wx.ALIGN_CENTER, 0)
        #vbox.AddSpacer(10)
        vbox.Add(self.bSizer_msg, 0, wx.ALIGN_CENTER, 0)
        self.bSizer_msg.ShowItems(False)
        vbox.Add(bSizer1, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)
        vbox.AddSpacer(10)
        self.hbox.AddSpacer(10)
        vbox.Add(bSizer2, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)

        self.hbox.Add(vbox, 0, wx.ALIGN_CENTER, 0)
        self.hbox.AddSpacer(5)

        self.panel.SetSizer(self.hbox)
        self.hbox.Fit(self)

        # do menu
        print "-I- Initializing menu"
        menubar = MagICMenu(self)
        self.SetMenuBar(menubar)


    def on_change_dir_button(self, event):
        """
        create change directory frame
        """
        currentDirectory = self.WD #os.getcwd()
        change_dir_dialog = wx.DirDialog(self.panel,
                                         "Choose your working directory to create or edit a MagIC contribution:",
                                         defaultPath=currentDirectory,
                                         style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR)
        result = change_dir_dialog.ShowModal()
        if result == wx.ID_CANCEL:
            return
        if result == wx.ID_OK:
            self.WD = change_dir_dialog.GetPath()
            self.dir_path.SetValue(self.WD)
        change_dir_dialog.Destroy()
        wait = wx.BusyInfo('Initializing data object in new directory, please wait...')
        wx.Yield()
        print '-I- Initializing magic data object'
        # make new contribution object, but reuse old data_model
        self.contribution = nb.Contribution(self.WD, dmodel=self.data_model)
        self.edited = False
        print '-I- Read in any available data from working directory'
        print '-I- Initializing headers'
        del wait

    def on_open_grid_frame(self):
        self.Hide()

    def on_close_grid_frame(self, event=None):
        if self.grid_frame.grid.changes:
            self.edited = True
        self.grid_frame = None
        self.Show()
        if event:
            event.Skip()

    def make_grid_frame(self, event):
        """
        Create a GridFrame for data type of the button that was clicked
        """
        if self.grid_frame:
            print '-I- You already have a grid frame open'
            pw.simple_warning("You already have a grid open")
            return

        try:
            grid_type = event.GetButtonObj().Name[:-4] # remove '_btn'
        except AttributeError:
            grid_type = self.FindWindowById(event.Id).Name[:-4] # remove ('_btn')
        wait = wx.BusyInfo('Making {} grid, please wait...'.format(grid_type))
        wx.Yield()
        # hide mainframe
        self.on_open_grid_frame()
        # make grid frame
        self.grid_frame = grid_frame.GridFrame(self.contribution, self.WD, grid_type, grid_type, self.panel)
        row_string = ""
        # paint validations if appropriate
        if self.validation_mode:
            if grid_type in self.validation_mode:
                self.grid_frame.toggle_help(None, "open")
                row_problems = self.failing_items[grid_type]["rows"]
                missing_columns = self.failing_items[grid_type]["missing_columns"]
                missing_groups = self.failing_items[grid_type]["missing_groups"]
                #all_cols = row_problems.columns
                #col_nums = range(len(all_cols))
                #col_pos = dict(zip(all_cols, col_nums))
                if len(row_problems):
                    row_string = """Columns and rows with problem data have been highlighted in blue.
Cells with problem data are highlighted according to the type of problem.
Red: incorrect data
For full error messages, see {}.""".format(grid_type + "_errors.txt")
                    for row in row_problems['num']:
                        self.grid_frame.grid.paint_invalid_row(row)
                        mask = row_problems["num"] == row
                        items = row_problems[mask]
                        cols = items.dropna(how="all", axis=1).drop(["num", "issues"], axis=1)
                        for col in cols:
                            pre, col_name = val_up3.extract_col_name(col)
                            col_ind = self.grid_frame.grid.col_labels.index(col_name)
                            self.grid_frame.grid.paint_invalid_cell(row, col_ind)
                current_label = self.grid_frame.msg_text.GetLabel()
                if len(missing_columns):
                    col_string = "You are missing the following required columns: {}\n\n".format(", ".join(missing_columns))
                else:
                    col_string = ""
                if len(missing_groups):
                    group_string = "You must have at least one column from each of the following groups: {}\n\n".format(", ".join(missing_groups))
                else:
                    group_string = ""
                #
                add_text = """{}{}{}""".format(col_string, group_string, row_string)
                self.grid_frame.msg_text.SetLabel(add_text)
        #self.on_finish_change_dir(self.change_dir_dialog)
        self.grid_frame.do_fit(None)
        del wait


    def on_upload_file(self, event):
        wait = wx.BusyInfo('Validating data, please wait...')
        wx.Yield()
        res, error_message, has_problems, all_failing_items = ipmag.upload_magic3(dir_path=self.WD,
                                                                                  vocab=self.contribution.vocab)
        self.failing_items = all_failing_items
        if has_problems:
            self.validation_mode = set(has_problems)
            # highlighting doesn't work with Windows
            if sys.platform in ['win32', 'win62']:
                self.message.SetLabel('The following grid(s) have incorrect or incomplete data:\n{}'.format(', '.join(self.validation_mode)))
            # highlighting does work with OSX
            else:
                for dtype in ["specimens", "samples", "sites", "locations", "ages"]:
                    wind = self.FindWindowByName(dtype + '_btn')
                    if dtype not in has_problems:
                        wind.Unbind(wx.EVT_PAINT, handler=self.highlight_button)
                    else:
                        wind.Bind(wx.EVT_PAINT, self.highlight_button)
                self.Refresh()
                self.message.SetLabel('Highlighted grids have incorrect or incomplete data')
            self.bSizer_msg.ShowItems(True)
            self.hbox.Fit(self)
        if not has_problems:
            self.validation_mode = set()
            self.message.SetLabel('')
            self.bSizer_msg.ShowItems(False)
            self.hbox.Fit(self)
        del wait


    def highlight_button(self, event):
        """
        Draw a red highlight line around the event object
        """
        wind = event.GetEventObject()
        pos = wind.GetPosition()
        size = wind.GetSize()
        try:
            dc = wx.PaintDC(self)
        except wx._core.PyAssertionError:
            # if it's not a native paint event, we can't us wx.PaintDC
            dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen('red', 5, wx.SOLID))
        dc.DrawRectangle(pos[0], pos[1], size[0], size[1])
        event.Skip()


class MagICMenu(wx.MenuBar):
    """
    initialize menu bar for GUI
    """
    #pylint: disable=R0904
    #pylint: disable=R0914
    def __init__(self, parent):
        self.parent = parent
        super(MagICMenu, self).__init__()

        file_menu = wx.Menu()
        file_quit = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        file_clear = file_menu.Append(wx.ID_ANY, 'Clear directory', 'Delete all files from working directory')
        #file_help = file_menu.Append(wx.ID_ANY, 'Help', 'More information about creating a MagIC contribution')
        file_show = file_menu.Append(wx.ID_ANY, 'Show main window', 'Show main window')
        file_close_grid = file_menu.Append(wx.ID_ANY, 'Close current grid', 'Close current grid')
        parent.Bind(wx.EVT_MENU, self.on_quit, file_quit)
        parent.Bind(wx.EVT_MENU, self.on_clear, file_clear)
        #parent.Bind(wx.EVT_MENU, self.on_help, file_help)
        parent.Bind(wx.EVT_MENU, self.on_show_mainframe, file_show)
        parent.Bind(wx.EVT_MENU, self.on_close_grid, file_close_grid)
        self.Append(file_menu, 'File')

        help_menu = wx.Menu()
        help_cookbook = help_menu.Append(wx.ID_ANY, '&PmagPy Cookbook\tCtrl-Shift-H',
                                         'Access the online documentation')
        help_git = help_menu.Append(wx.ID_ANY, '&Github Page\tCtrl-Shift-G',
                                    'Access the PmagPy repository')
        parent.Bind(wx.EVT_MENU, pw.on_cookbook, help_cookbook)
        parent.Bind(wx.EVT_MENU, pw.on_git, help_git)
        if pw.get_output_frame():
            help_show = help_menu.Append(wx.ID_ANY, 'Show output', 'Show help')
            help_hide = help_menu.Append(wx.ID_ANY, 'Hide output', 'Hide output')
            parent.Bind(wx.EVT_MENU, pw.on_show_output, help_show)
            parent.Bind(wx.EVT_MENU, pw.on_hide_output, help_hide)
        self.Append(help_menu, 'Help ')

    def on_quit(self, event):
        """
        shut down application
        """
        if self.parent.grid_frame:
            if self.parent.grid_frame.grid.changes:
                dlg = wx.MessageDialog(self,caption="Message:", message="Are you sure you want to exit the program?\nYou have a grid open with unsaved changes.\n ", style=wx.OK|wx.CANCEL)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    dlg.Destroy()
                else:
                    dlg.Destroy()
                    return
        if self.parent.grid_frame:
            self.parent.grid_frame.Destroy()
        self.parent.Close()
        try:
            sys.exit()
        except TypeError:
            pass

    def on_clear(self, event):
        """
        initialize window to allow user to empty the working directory
        """
        dia = pmag_menu_dialogs.ClearWD(self.parent, self.parent.WD)
        clear = dia.do_clear()
        if clear:
            print '-I- Clear data object'
            self.contribution = nb.Contribution(self.WD, dmodel=self.data_model)
            self.edited = False



    #def on_help(self, event):
    #    """
    #    point user to Cookbook help
    #    """
    #    #for use on the command line
    #    path = find_pmag_dir.get_pmag_dir()
    #
    #    # for use with pyinstaller:
    #    #path = self.Parent.resource_dir
    #
    #    html_frame = pw.HtmlFrame(self, page=(os.path.join(path, "documentation", #"magic_gui.html")))
    #    html_frame.Center()
    #    html_frame.Show()

    def on_show_mainframe(self, event):
        """
        Show main magic_gui window
        """
        self.parent.Show()
        self.parent.Raise()

    def on_close_grid(self, event):
        """
        If there is an open grid, save its data and close it.
        """
        if self.parent.grid_frame:
            self.parent.grid_frame.onSave(None)
            self.parent.grid_frame.Destroy()

def main():
    if '-h' in sys.argv:
        print "See https://earthref.org/PmagPy/cookbook/#magic_gui.py for a complete tutorial"
        sys.exit()
    print '-I- Starting MagIC GUI - please be patient'

    # if redirect is true, wxpython makes its own output window for stdout/stderr
    app = wx.App(redirect=True)

    working_dir = pmag.get_named_arg_from_sys('-WD', '.')
    app.frame = MainFrame(working_dir)
    ## this causes an error with Canopy Python
    ## (it works with brew Python)
    ## need to use these lines for Py2app
    if working_dir == '.':
        app.frame.on_change_dir_button(None)

    app.frame.Show()
    app.frame.Center()
    ## use for debugging:
    #if '-i' in sys.argv:
    #    import wx.lib.inspection
    #    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()



if __name__ == "__main__":
    main()
