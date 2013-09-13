import wx
import glob
import snapext
import time
import xml.etree.ElementTree as et
modules = sorted([x.replace('.py', '') for x in glob.glob('*.py') if x != 'launcher.py']) #replace py with epk
status = {}
combine = []
"""def CombineXML():
    global combine
    roots = []
    blocks = []
    for i in range(0, len(combine)):
        combine[i] = et.parse(combine[i] + '.xml')
        roots.append(combine[i].getroot())
    for root in roots:
        for child in root:
            blocks.append(child)
    wrapper = et.Element('blocks')
    wrapper.attrib = {'app':'Snap! Module Combiner 1.0', 'version':'0.1'}
    for i in range(0, len(blocks)):
        wrapper.append(blocks[i])
    @snapext.SnapHandler.route('/Extensions.xml')
    def combine():
        et.tostring(wrapper)"""
class SnapFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self,parent, title=title, size=size)
class SnapPanel(wx.Panel):
    frame = None
    def __init__(self, parent):
        global frame
        frame = parent
        wx.Panel.__init__(self, parent)
        y = 0
        for i in modules:
            self.cb = wx.CheckBox(self, label=i, pos=(0,y))
            self.Bind(wx.EVT_CHECKBOX, self.Status, self.cb)
            y += 20
        self.run = wx.Button(self, label="Run!", pos=(200, (len(modules) * 20 / 2) - 10))
        self.Bind(wx.EVT_BUTTON, self.Run, self.run)
    
    def Status(self, event):
        status[event.GetEventObject().GetLabel().encode('ascii', 'ignore')] = event.Checked()
    print status
    def Run(self, event):
        frame.Close()
app = wx.App(False)
frame = SnapFrame(None, title="Snap! Launchpad", size=(400, len(modules) * 20 + 10))
panel = SnapPanel(frame)
frame.Show()
app.MainLoop()
for i in status.iteritems():
    if i[1] == True:
        __import__(i[0])
        combine.append(i[0])
#CombineXML()
snapext.main(snapext.SnapHandler, 1337)
