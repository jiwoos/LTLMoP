#!/usr/bin/env python
# -*- coding: us-ascii -*-
# generated by wxGlade 0.6.3 on Tue Jan 26 00:44:24 2010

import wx, wx.lib.buttons
import sys, socket
import wx.lib.delayedresult as delayedresult
sys.path.append("lib")
import project
import mapRenderer

# begin wxGlade: extracode
# end wxGlade

# For IPC, we need to pass messages by stderr because stdout is buffered.
# But we still want to show errors, so we'll point stderr to stdout.
sys.stdout = sys.__stderr__
sys.stderr = sys.__stdout__

class SensorEditorFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SensorEditorFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.buttons = [] # This will later hold our buttons

        self.map_panels = {} # This will later hold our map panels
        self.map_bitmaps = {} # This will later hold our map panel bitmaps
        self.map_state = {} # This will later hold current region states
        self.map_scales = {}

        self.waitingForInput = False
        self.Bind(wx.EVT_IDLE, self.onIdle)
        
        self.host = 'localhost'
        self.port = 23459
        self.buf = 1024
        self.addr = (self.host,self.port)
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDPSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # Let everyone know we're ready
        #print "Hello!"
        self.UDPSock.sendto("Hello!\n",self.addr)
        #self.UDPSock.close()        

    def __set_properties(self):
        # begin wxGlade: SensorEditorFrame.__set_properties
        self.SetTitle("Dummy Sensor Handler")
        self.SetSize((272, 372))
        self.panel_1.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SensorEditorFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def sensorToggle(self, event): # wxGlade: SensorEditorFrame.<event_handler>
        btn = event.GetEventObject()

        self.UDPSock.sendto(btn.GetLabelText() + "=" + str(btn.GetValue()),self.addr)
        #print btn.GetLabelText() + "=" + str(btn.GetValue())

        # TODO: Button background colour doesn't show up very well
        if btn.GetValue():
            btn.SetBackgroundColour(wx.Colour(0, 255, 0)) 
        else:
            btn.SetBackgroundColour(wx.Colour(255, 0, 0)) 

        self.Refresh()

        event.Skip()

    def checkForInput(self):
        return sys.stdin.readline()

    def updateFromInput(self, text):
        """
        We decide what buttons to create based on messages via stdin
        """
        line = text.get().strip()

        if line == ":QUIT" or line == '': # EOF means Executor crashed
            wx.CallAfter(self.Close)
            return

        try: 
            # Read in the information
            [sensor_type, sensor_name, sensor_value] = line.split(",")
            
            if sensor_type.strip().lower() == "button":
                # Create the new button and add it to the sizer
                self.buttons.append(wx.lib.buttons.GenToggleButton(self.panel_1, -1, sensor_name))
                big_font = wx.Font(pointSize=24, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL)
                self.buttons[-1].SetFont(big_font)
                self.panel_1.GetSizer().Add(self.buttons[-1], 1, wx.EXPAND, 0)

                # Set the initial value as appropriate
                if sensor_value == "1":
                    self.buttons[-1].SetValue(True)
                    self.buttons[-1].SetBackgroundColour(wx.Colour(0, 255, 0)) 
                else:
                    self.buttons[-1].SetValue(False)
                    self.buttons[-1].SetBackgroundColour(wx.Colour(255, 0, 0)) 

                # Bind to event handler
                self.Bind(wx.EVT_BUTTON, self.sensorToggle, self.buttons[-1])
            elif sensor_type.strip().lower() == "region":
                if self.proj is None:
                    print "Error: region sensor cannot be created without a project loaded"
                else:
                    # initialize
                    self.map_state[sensor_name] = sensor_value

                    self.map_panels[sensor_name] = wx.Panel(self.panel_1)

                    self.Bind(wx.EVT_SIZE, self.onResize)
                    self.panel_1.GetSizer().Add(self.map_panels[sensor_name], 1, wx.EXPAND, 0)

                    self.map_panels[sensor_name].SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
                    self.map_panels[sensor_name].Bind(wx.EVT_PAINT, self.onMapPaint)
                    self.map_panels[sensor_name].Bind(wx.EVT_LEFT_DOWN, self.onMapClick)
            elif sensor_type.strip().lower() == "loadproj":
                self.proj =  project.Project()
                self.proj.loadProject(sensor_name)
                self.decomposedRFI = self.proj.loadRegionFile(decomposed=True)

            self.panel_1.Layout() # Update the frame
            self.onResize()
        except ValueError:
            print "(SENSOR) WARNING: Unexpected message received!"

        self.waitingForInput = False  # Make sure another listener gets started

    def onIdle(self, event):
        # TODO: Use plain threading like other parts of LTLMoP?
        if not self.waitingForInput:
            delayedresult.startWorker(self.updateFromInput, self.checkForInput)
            self.waitingForInput = True
        event.Skip()

    def onMapClick(self, event):
        panel = event.GetEventObject()
        panel_key = None
        for k,v in self.map_panels.iteritems():
            if v == panel:
                panel_key = k
                break

        x = event.GetX()/self.map_scales[panel_key]
        y = event.GetY()/self.map_scales[panel_key]
        for region in self.decomposedRFI.regions:
            if region.objectContainsPoint(x, y):
                if region.name != self.map_state[panel_key]:
                    self.map_state[panel_key] = region.name
                    self.UDPSock.sendto(panel_key + "=" + region.name, self.addr)
                break

        self.onResize() # Force map redraw
        event.Skip()

    def onResize(self, event=None):
        for k, p in self.map_panels.iteritems():
            size = p.GetSize()
            self.map_bitmaps[k] = wx.EmptyBitmap(size.x, size.y)
            self.map_scales[k] = mapRenderer.drawMap(self.map_bitmaps[k], self.decomposedRFI, scaleToFit=True, drawLabels=True, memory=True, highlightList=self.map_state[k])

        self.Refresh()
        self.Update()

        if event is not None:
            event.Skip()

    def onMapPaint(self, event):
        panel = event.GetEventObject()
        panel_key = None
        for k,v in self.map_panels.iteritems():
            if v == panel:
                panel_key = k
                break

        if panel_key not in self.map_bitmaps:
            return

        pdc = wx.AutoBufferedPaintDC(panel)
        try:
            dc = wx.GCDC(pdc)
        except:
            dc = pdc

        # dc.BeginDrawing()

        # Draw background
        dc.DrawBitmap(self.map_bitmaps[panel_key], 0, 0)

        # dc.EndDrawing()

        event.Skip()

# end of class SensorEditorFrame


class SensorHandlerApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = SensorEditorFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class SensorHandlerApp

if __name__ == "__main__":
    SensorHandler = SensorHandlerApp(0)
    SensorHandler.MainLoop()
