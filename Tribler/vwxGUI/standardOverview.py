import wx, os, sys, os.path
import wx.xrc as xrc
from Tribler.vwxGUI.GuiUtility import GUIUtility


class standardOverview(wx.Panel):
    """
    Panel that shows one of the overview panels
    """
    def __init__(self, *args):
        if len(args) == 0:
            pre = wx.PrePanel()
            # the Create step is done by XRC.
            self.PostCreate(pre)
            self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        else:
            wx.Panel.__init__(self, args[0], args[1], args[2], args[3])
            self._PostInit()
        
    def OnCreate(self, event):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        wx.CallAfter(self._PostInit)
        event.Skip()
        return True
    
    def _PostInit(self):
        # Do all init here
        self.mode = 'torrentMode'
        self.addComponents()
        self.panel = None
        self.refreshMode()
        self.Refresh()
        self.guiUtility = GUIUtility.getInstance()
        self.guiUtility.report(self)
        
        
    def addComponents(self):
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.hSizer)
        self.SetAutoLayout(1)
        self.Layout()
        
    def setMode(self, mode):
        self.mode = mode
        self.refreshMode()
            
    def refreshMode(self):
        # load xrc
        self.oldpanel = self.panel
        self.Show(False)
        if self.mode == 'torrentMode':
            xrcResource = os.path.join('Tribler','vwxGUI', 'torrentOverview.xrc')
            panelName = 'torrentOverview'
        elif self.mode == 'personsMode':
            xrcResource = os.path.join('Tribler','vwxGUI', 'personsOverview.xrc')
            panelName = 'personsOverview'
        
        else:
            print 'Mode unknown'
            return
        self.res = xrc.XmlResource(xrcResource)
        # create panel
        self.panel = self.res.LoadPanel(self, panelName)
        
        if self.oldpanel:
            self.hSizer.Detach(self.oldpanel)
            self.oldpanel.Destroy()
        
        self.hSizer.Add(self.panel, 1, wx.ALL|wx.EXPAND, 0)
        
        self.hSizer.Layout()
        self.panel.Refresh()
        self.Show(True)