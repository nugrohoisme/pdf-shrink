import pdfShrink
import wx

class MainWindow(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)

        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        
        self.InitInput()
        self.InitUI()
        self.Centre()

        self.SetSize(600, 315)

        # Load ghostscript path from config
        gs_path = pdfShrink.get_gs_path()
        if gs_path is not None:
            self.txtGsPath.SetValue(gs_path)

    def InitUI(self):
        # Layout
        box = wx.BoxSizer(wx.VERTICAL)

        # Ghostscript path
        t = wx.StaticText(self, label="Ghostscript Path",style=wx.ALIGN_LEFT)
        t.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        box.Add(t, 0, wx.TOP|wx.ALIGN_LEFT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.txtGsPath, 1, wx.EXPAND)
        hbox.Add(self.btnGsFind, 0, wx.EXPAND)
        box.Add(hbox, 0, wx.EXPAND)

        # Input path
        t = wx.StaticText(self, label="Input File",style=wx.ALIGN_LEFT)
        t.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        box.Add(t, 0, wx.TOP|wx.ALIGN_LEFT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.txtInput, 1, wx.EXPAND)
        hbox.Add(self.btnInputFind, 0, wx.EXPAND)
        box.Add(hbox, 0, wx.EXPAND)

        # Output path
        t = wx.StaticText(self, label="Output File",style=wx.ALIGN_LEFT)
        t.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        box.Add(t, 0, wx.TOP|wx.ALIGN_LEFT, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.txtOutput, 1, wx.EXPAND)
        hbox.Add(self.btnOutputFind, 0, wx.EXPAND)
        box.Add(hbox, 0, wx.EXPAND)

        # Quality
        t = wx.StaticText(self, label="Quality (best to less)",style=wx.ALIGN_LEFT)
        t.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        box.Add(t, 0, wx.TOP|wx.ALIGN_LEFT, 10)
        box.Add(self.rbBox, 0, wx.EXPAND)

        # Process
        box.Add(self.btnProcess, 0, wx.TOP|wx.ALIGN_RIGHT,10)

        self.SetSizer(box)

    def InitInput(self):
        # Define input
        self.txtGsPath = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.txtInput = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.txtOutput = wx.TextCtrl(self)
        self.btnGsFind = wx.Button(self, label="Find")
        self.btnInputFind = wx.Button(self, label="Find")
        self.btnOutputFind = wx.Button(self, label="Find")
        self.rbBox = wx.RadioBox(self, choices=['printer', 'ebook', 'screen'])
        self.btnProcess = wx.Button(self, label="Shrink")

        # Bind events
        self.btnGsFind.Bind(wx.EVT_BUTTON, self.btnGsFind_Clicked)
        self.btnInputFind.Bind(wx.EVT_BUTTON, self.btnInputFind_Clicked)
        self.btnOutputFind.Bind(wx.EVT_BUTTON, self.btnOutputFind_Clicked)
        self.btnProcess.Bind(wx.EVT_BUTTON, self.btnProcess_Clicked)

    def btnGsFind_Clicked(self, e):
        ofd = wx.FileDialog(self, "Open", "", "", "", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        ofd.ShowModal()
        
        # Show & save to config
        if len(ofd.GetPath()) > 0:
            self.txtGsPath.SetValue(ofd.GetPath())
            pdfShrink.set_gs_path(self.txtGsPath.GetValue())

        ofd.Destroy()

    def btnInputFind_Clicked(self, e):
        ofd = wx.FileDialog(self, "Open", "", "", "PDF files (*.pdf)|*.pdf", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        ofd.ShowModal()
        self.txtInput.SetValue(ofd.GetPath())
        ofd.Destroy()

    def btnOutputFind_Clicked(self, e):
        ofd = wx.FileDialog(self, "Open", "", "", "PDF files (*.pdf)|*.pdf", wx.FD_OPEN)
        ofd.ShowModal()
        self.txtOutput.SetValue(ofd.GetPath())
        ofd.Destroy()

    def btnProcess_Clicked(self, e):
        if len(self.txtGsPath.GetValue()) == 0:
            d = wx.MessageDialog(None, 'Please select ghostscript executable or binary', "Sorry", wx.OK | wx.ICON_EXCLAMATION)
            d.ShowModal()
            d.Destroy()
            return

        if len(self.txtInput.GetValue()) == 0:
            d = wx.MessageDialog(None, 'Please select input file', "Sorry", wx.OK | wx.ICON_EXCLAMATION)
            d.ShowModal()
            d.Destroy()
            return

        if len(self.txtOutput.GetValue()) == 0:
            d = wx.MessageDialog(None, 'Please select/insert output file', "Sorry", wx.OK | wx.ICON_EXCLAMATION)
            d.ShowModal()
            d.Destroy()
            return

        self.btnProcess.Disable()
        self.btnProcess.SetLabel('Processing...')

        pdfShrink.doShrink(self.txtGsPath.GetValue(), self.txtInput.GetValue(), self.txtOutput.GetValue(), self.rbBox.GetStringSelection())

        d = wx.MessageDialog(None, 'Shrink SUCCESS', "Success!", wx.OK | wx.ICON_INFORMATION)
        d.ShowModal()
        d.Destroy()

        self.btnProcess.Enable()    
        self.btnProcess.SetLabel('Shrink')

if __name__ == '__main__':
    app = wx.App()
    
    window = MainWindow("PDF Shrinker")
    window.Show(True)

    app.MainLoop()