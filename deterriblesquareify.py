#!/usr/bin/env python2.7

import wx

class Square(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Deterriblesquareify')

        # add a panel so it looks nice
        self.panel = wx.Panel(self, wx.ID_ANY)

        # define the maximum displayed image size in pixels
        self.maxImgSize = 1200
        self.imgSize = 400
        # initially the path to an image is not set
        self.imagePath = ''

        # set the minimum and maximum window sizes
        self.SetSizeHints(400,300,1200,800)

        # create buttons
        q1u1 = wx.Button(self.panel, wx.ID_ANY, '+1')
        q1d1 = wx.Button(self.panel, wx.ID_ANY, '-1')
        q2u1 = wx.Button(self.panel, wx.ID_ANY, '+1')
        q2d1 = wx.Button(self.panel, wx.ID_ANY, '-1')
        q3u1 = wx.Button(self.panel, wx.ID_ANY, '+1')
        q3d1 = wx.Button(self.panel, wx.ID_ANY, '-1')
        q4u1 = wx.Button(self.panel, wx.ID_ANY, '+1')
        q4d1 = wx.Button(self.panel, wx.ID_ANY, '-1')
        q1u10 = wx.Button(self.panel, wx.ID_ANY, '+10')
        q1d10 = wx.Button(self.panel, wx.ID_ANY, '-10')
        q2u10 = wx.Button(self.panel, wx.ID_ANY, '+10')
        q2d10 = wx.Button(self.panel, wx.ID_ANY, '-10')
        q3u10 = wx.Button(self.panel, wx.ID_ANY, '+10')
        q3d10 = wx.Button(self.panel, wx.ID_ANY, '-10')
        q4u10 = wx.Button(self.panel, wx.ID_ANY, '+10')
        q4d10 = wx.Button(self.panel, wx.ID_ANY, '-10')

        loadBtn = wx.Button(self.panel, wx.ID_ANY, 'Load Image')
        saveBtn = wx.Button(self.panel, wx.ID_ANY, 'Save Image')
        resetBtn = wx.Button(self.panel, wx.ID_ANY, 'Reset Image')
        autoBtn = wx.Button(self.panel, wx.ID_ANY, 'Autotune Image')

        # bind buttons  
        self.Bind(wx.EVT_BUTTON, self.onQ1u1, q1u1)
        self.Bind(wx.EVT_BUTTON, self.onQ1d1, q1d1)
        self.Bind(wx.EVT_BUTTON, self.onQ2u1, q2u1)
        self.Bind(wx.EVT_BUTTON, self.onQ2d1, q2d1)
        self.Bind(wx.EVT_BUTTON, self.onQ3u1, q3u1)
        self.Bind(wx.EVT_BUTTON, self.onQ3d1, q3d1)
        self.Bind(wx.EVT_BUTTON, self.onQ4u1, q4u1)
        self.Bind(wx.EVT_BUTTON, self.onQ4d1, q4d1)
        self.Bind(wx.EVT_BUTTON, self.onQ1u10, q1u10)
        self.Bind(wx.EVT_BUTTON, self.onQ1d10, q1d10)
        self.Bind(wx.EVT_BUTTON, self.onQ2u10, q2u10)
        self.Bind(wx.EVT_BUTTON, self.onQ2d10, q2d10)
        self.Bind(wx.EVT_BUTTON, self.onQ3u10, q3u10)
        self.Bind(wx.EVT_BUTTON, self.onQ3d10, q3d10)
        self.Bind(wx.EVT_BUTTON, self.onQ4u10, q4u10)
        self.Bind(wx.EVT_BUTTON, self.onQ4d10, q4d10)

        self.Bind(wx.EVT_BUTTON, self.onLoad, loadBtn)
        self.Bind(wx.EVT_BUTTON, self.onSave, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.onReset, resetBtn)
        self.Bind(wx.EVT_BUTTON, self.onAuto, autoBtn)

        self.Bind(wx.EVT_SIZE, self.onSize)

        # create image object
        #img = wx.Image('test2.tif')
        #img = wx.Image('test2.tif', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.myImg = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        #wx.StaticBitmap(self, -1, img, (10,5), (img.GetWidth(), img.GetHeight()))
        self.currentImg = wx.EmptyImage(self.imgSize, self.imgSize)
        self.myImg = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(self.currentImg))
        # clicking the blank image brings up the file loading dialog
        self.myImg.Bind(wx.EVT_LEFT_DOWN, self.onLoad)

        # create sizers to hold objects
        topSizer = wx.BoxSizer(wx.VERTICAL)
        # sizer for load/save buttons
        loadSaveSizer = wx.BoxSizer(wx.HORIZONTAL)
        # sizer for reset/auto buttons
        resetAutoSizer = wx.BoxSizer(wx.HORIZONTAL)
        # sizer for image and manipulation buttons
        self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
        # sizer for Q2, Q3 buttons
        LBtnSizer = wx.GridSizer(rows=4,cols=2, hgap=0, vgap=0)
        LBtnSizer.SetMinSize((100,100))
        # sizer for Q1, Q4 buttons
        RBtnSizer = wx.GridSizer(rows=4,cols=2, hgap=0, vgap=0)
        RBtnSizer.SetMinSize((100,100))

        # add objects to sizers
        loadSaveSizer.Add(loadBtn, 1, wx.EXPAND, 0)
        loadSaveSizer.Add(saveBtn, 1, wx.EXPAND, 0)

        resetAutoSizer.Add(resetBtn, 1, wx.EXPAND, 0)
        resetAutoSizer.Add(autoBtn, 1, wx.EXPAND, 0)

        LBtnSizer.Add(q2u10, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q2u1, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q2d10, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q2d1, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q3u10, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q3u1, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q3d10, 1, wx.EXPAND, 0)
        LBtnSizer.Add(q3d1, 1, wx.EXPAND, 0)

        RBtnSizer.Add(q1u1, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q1u10, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q1d1, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q1d10, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q4u1, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q4u10, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q4d1, 1, wx.EXPAND, 0)
        RBtnSizer.Add(q4d10, 1, wx.EXPAND, 0)

        self.imgSizer.Add(LBtnSizer, 1, wx.EXPAND)
        #self.imgSizer.Add((1,1), 1)
        #self.imgSizer.Add(self.myImg, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        #self.imgSizer.Add(self.myImg, 0, wx.ALL, border=10)
        self.imgSizer.Add(self.myImg, 0, wx.EXPAND)
        #self.imgSizer.Add((1,1), 1)
        self.imgSizer.Add(RBtnSizer, 1, wx.EXPAND)

        topSizer.Add(loadSaveSizer, 0, wx.EXPAND)
        topSizer.Add(self.imgSizer, 1, wx.EXPAND)
        topSizer.Add(resetAutoSizer, 0, wx.EXPAND)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        #self.panel.SetSizer(self.imgSizer)
        #self.imgSizer.Fit(self)

        self.panel.Layout()

        print 'size of imgSizer is '+str(self.imgSizer.GetMinSize()[1])

    def onQ1u1(self, event):
        print 'Adding 1 to pixels in Q1'

    def onQ1d1(self, event):
        print 'Subtracting 1 from pixels in Q1'

    def onQ2u1(self, event):
        print 'Adding 1 to pixels in Q2'

    def onQ2d1(self, event):
        print 'Subtracting 1 from pixels in Q2'

    def onQ3u1(self, event):
        print 'Adding 1 to pixels in Q3'

    def onQ3d1(self, event):
        print 'Subtracting 1 from pixels in Q3'

    def onQ4u1(self, event):
        print 'Adding 1 to pixels in Q4'

    def onQ4d1(self, event):
        print 'Subtracting 1 from pixels in Q4'

    def onQ1u10(self, event):
        print 'Adding 10 to pixels in Q1'

    def onQ1d10(self, event):
        print 'Subtracting 10 from pixels in Q1'

    def onQ2u10(self, event):
        print 'Adding 10 to pixels in Q2'

    def onQ2d10(self, event):
        print 'Subtracting 10 from pixels in Q2'

    def onQ3u10(self, event):
        print 'Adding 10 to pixels in Q3'

    def onQ3d10(self, event):
        print 'Subtracting 10 from pixels in Q3'

    def onQ4u10(self, event):
        print 'Adding 10 to pixels in Q4'

    def onQ4d10(self, event):
        print 'Subtracting 10 from pixels in Q4'

    def onLoad(self, e=None):
        '''
        Load an image file.
        '''

        print 'Loading...'

        # self.dirname provides a persistent memory of the last directory visited
        if 'self.dirname' not in locals():
            self.dirname = '.'

        wildcards = "TIF files (*.tif)|*.tif|PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg"
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", wildcards, wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.imagePath = dlg.GetPath()
            self.currentImg = wx.Image(self.imagePath)
            self.displayImg = self.currentImg.Scale(self.imgSize, self.imgSize)
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()

    def onSave(self, e=None):
        print 'Saving...'

    def onReset(self, e=None):
        '''
        Reset the currently loaded image to its original state.
        '''

        # only reset if a file has previously been loaded
        if self.imagePath != '':
            print 'Resetting image...'
            self.currentImg = wx.Image(self.imagePath)
            self.displayImg = self.currentImg.Scale(self.imgSize, self.imgSize)
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()

    def onAuto(self, e=None):
        print 'Autotuning...'

    def onSize(self, e=None):
        self.imgSize = self.imgSizer.GetSize()[1]
        print 'Height of image sizer is '+str(self.imgSize)
        self.displayImg = self.currentImg.Scale(self.imgSize, self.imgSize)
        self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
        self.panel.Refresh()
        e.Skip()


# Run the program
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Square().Show()
    app.MainLoop()
