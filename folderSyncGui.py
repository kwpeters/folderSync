#! /usr/bin/env python32
import wx

class FolderSyncFrame(wx.Frame):
    r'''This is the appliation's main frame window.'''

    def __init__(self):
        r'''Constructor'''

        # Chain to the base class.
        wx.Frame.__init__(self, None, title="FolderSync", size=(600, 400))

        # Setup the GUI.



class App(wx.App):
    r'''The application object.
    '''
    def OnInit(self):
        self.frame = FolderSyncFrame()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
