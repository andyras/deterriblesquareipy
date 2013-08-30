#!/usr/bin/env python2.7

import wx
import numpy as np
from scipy.misc import imread

debug = True

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
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(1, 1), q1u1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(1, -1), q1d1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(2, 1), q2u1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(2, -1), q2d1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(3, 1), q3u1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(3, -1), q3d1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(4, 1), q4u1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(4, -1), q4d1)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(1, 10), q1u10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(1, -10), q1d10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(2, 10), q2u10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(2, -10), q2d10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(3, 10), q3u10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(3, -10), q3d10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(4, 10), q4u10)
        self.Bind(wx.EVT_BUTTON, lambda event: self.adjustQuadrant(4, -10), q4d10)

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
        self.currentImg = wx.EmptyImage(1,1)
        self.myImg = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(self.currentImg))
        # clicking the blank image brings up the file loading dialog
        self.myImg.Bind(wx.EVT_LEFT_DOWN, self.onImageClick)

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
        self.imgSizer.Add(self.myImg, 0, wx.EXPAND)
        self.imgSizer.Add(RBtnSizer, 1, wx.EXPAND)

        topSizer.Add(loadSaveSizer, 0, wx.EXPAND)
        topSizer.Add(self.imgSizer, 1, wx.EXPAND)
        topSizer.Add(resetAutoSizer, 0, wx.EXPAND)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

        self.panel.Layout()

    def mm(self, n):
        '''
        Sets the integer n to be between 0 and 255
        '''
        if (n < 0):
            return 0
        elif (n > 255):
            return 255
        return n

    def adjustQuadrant(self, q, n, e=None):
        '''
        Quadrant q is 1, 2, 3, or 4.  n is the adjustment to the RGB values.
        '''
        # the origin is at the top left of the image
        if (q == 1):    # top right quadrant
            minx = self.currentImg.GetSize()[0]/2 + 0
            maxx = self.currentImg.GetSize()[0]
            miny = 0
            maxy = self.currentImg.GetSize()[1]/2
        elif (q == 2):    # top left quadrant
            minx = 0
            maxx = self.currentImg.GetSize()[0]/2
            miny = 0
            maxy = self.currentImg.GetSize()[1]/2
        elif (q == 3):    # bottom left quadrant
            minx = 0
            maxx = self.currentImg.GetSize()[0]/2
            miny = self.currentImg.GetSize()[1]/2 + 0
            maxy = self.currentImg.GetSize()[1]
        elif (q == 4):    # bottom right quadrant
            minx = self.currentImg.GetSize()[0]/2 + 0
            maxx = self.currentImg.GetSize()[0]
            miny = self.currentImg.GetSize()[1]/2 + 0
            maxy = self.currentImg.GetSize()[1]
        else:
            raise ValueError, 'Invalid quadrant specified.'

        # adjust each pixel in the quadrant
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                r = self.currentImg.GetRed(x, y) + n
                g = self.currentImg.GetGreen(x, y) + n
                b = self.currentImg.GetBlue(x, y) + n
                self.currentImg.SetRGB(x, y, self.mm(r), self.mm(g), self.mm(b))

        self.displayImg = self.currentImg.Scale(self.imgSize, self.imgSize)
        self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
        self.panel.Refresh()

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

            # disable logging (.tif[f]s with funny tags cause a pop-up error)
            noLog = wx.LogNull()

            # save the original for resetting
            self.originalImg = wx.Image(self.imagePath)
            self.currentImg = wx.Image(self.imagePath)

            # reenable logging
            del noLog

            # goof around with formats
            self.imgArray = self.wxImageToNumpy(self.originalImg)
            self.currentImg = self.numpyToWxImage(self.imgArray)

            # scale the original for display (saves a step for the first display)
            self.displayImg = self.originalImg.Scale(self.imgSize, self.imgSize)
            #self.displayImg = self.numpyToWxImage(self.imgArray).Scale(self.imgSize, self.imgSize)

            # display the loaded image
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()

    def wxImageToNumpy(self, img):
        '''
        Converts a wx.Image to a numpy array.
        '''

        # datatype is important
        a = np.frombuffer(img.GetData(), dtype='uint8')
        # note that height is the first dimension in the np.array.
        # (x and y are switched)
        a.shape = (img.GetHeight(), img.GetWidth(), 3)

        return a

    def numpyToWxImage(self, a):
        '''
        Converts a numpy array to a wx.Image.
        '''

        # note the use of the ascontiguousarray method, otherwise it may break for big arrays
        return wx.ImageFromBuffer(a.shape[0], a.shape[1], np.ascontiguousarray(a))
        
    def onSave(self, e=None):
        print 'Saving...'

    def onReset(self, e=None):
        '''
        Reset the currently loaded image to its original state.
        '''

        # only reset if a file has previously been loaded
        if self.imagePath != '':
            print 'Resetting image...'
            self.displayImg = self.originalImg.Scale(self.imgSize, self.imgSize)
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()

    def onAuto(self, e=None):
        '''
        Automatically finds the broken quadrant and adjusts it to match its neighbors.
        '''

        print 'Autotuning...'

        xDim = self.currentImg.GetSize()[0]
        yDim = self.currentImg.GetSize()[1]

        if (debug):
            print 'xDim '+str(xDim)
            print 'yDim '+str(yDim)

        ## construct vectors of grayscale values on adjacent quadrant edges
        #TODO read grayscale values as matrix

        # bottom of Q1 and top of Q4
        q1b = []
        q4t = []
        for x in range(xDim/2, xDim):
            q1b.append(self.currentImg.GetRed(x, yDim/2 - 1))
            q4t.append(self.currentImg.GetRed(x, yDim/2))

        # left of Q1 and right of Q2
        q1l = []
        q2r = []
        for y in range(0, yDim/2):
            q1l.append(self.currentImg.GetRed(xDim/2, y))
            q2r.append(self.currentImg.GetRed(xDim/2 - 1, y))

        # bottom of Q2 and top of Q3
        q2b = []
        q3t = []
        for x in range(0, xDim/2):
            q2b.append(self.currentImg.GetRed(x, yDim/2 - 1))
            q3t.append(self.currentImg.GetRed(x, yDim/2))

        # right of Q3 and left of Q4
        q3r = []
        q4l = []
        for y in range(yDim/2, yDim):
            q3r.append(self.currentImg.GetRed(xDim/2 - 1, y))
            q4l.append(self.currentImg.GetRed(xDim/2, y))

        ## find which quadrant is most likely to be the maladjusted one
        # calculate rms difference for each edge
        rmsRight = self.rms(q1b, q4t)
        rmsTop = self.rms(q1l, q2r)
        rmsLeft = self.rms(q2b, q3t)
        rmsBottom = self.rms(q3r, q4l)

        # each quadrant has two edges
        print rmsTop
        rmsQ1 = rmsTop + rmsRight
        rmsQ2 = rmsTop + rmsLeft
        rmsQ3 = rmsLeft + rmsBottom
        rmsQ4 = rmsBottom + rmsRight

        # find the largest
        if (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ1):
            q = 1
            insideEdge = q1l + q1b
            outsideEdge = q2r + q4t
            print 'Q1 will be adjusted'
        elif (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ2):
            q = 2
            insideEdge = q2r + q2b
            outsideEdge = q1l + q3t
            print 'Q2 will be adjusted'
        elif (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ3):
            q = 3
            insideEdge = q3r + q3t
            outsideEdge = q4l + q2b
            print 'Q3 will be adjusted'
        else:
            q = 4
            insideEdge = q4l + q4t
            outsideEdge = q3r + q1b
            print 'Q4 will be adjusted'

        ## find n which minimizes the rms difference in grayscale intensity along edges of quadrant
        n = 0
        newRMSValue = self.rms(insideEdge, outsideEdge)

        nSign = -1
        # case where pixels in quadrant need to be adjusted up
        if (sum(insideEdge) < sum(outsideEdge)):
            nSign = 1

        iter = 0
        maxIter = 255
        oldRMSValue = 1e10
        print 'STARTING AUTOTUNE'
        while ((iter < maxIter) and (newRMSValue < oldRMSValue)):
            oldRMSValue = newRMSValue
            # increase the adjustment to the insideEdge pixels
            n += nSign
            print 'n is %s' % n
            # find new adjusted RMS value
            newRMSValue = self.rmsAdjust(insideEdge, outsideEdge, n)
            iter += 1
            print 'oldRMSValue is %s' % oldRMSValue
            print 'newRMSValue is %s' % newRMSValue

        ## adjust the quadrant
        print 'Adjusting Q%d by %d grayscale values' % (q, (n - nSign))
        self.adjustQuadrant(q, n - nSign)
        print 'FINISHED AUTOTUNE'

    def rms(self, v1, v2):
        return self.rmsAdjust(v1, v2, 0)

    def rmsAdjust(self, v1, v2, n):
        '''
        Finds the RMS difference between two vectors, with the values in the
        first vector adjusted by n.
        '''

        squareSum = 0.0
        for i in range(len(v1)):
            squareSum += (v1[i] + n - v2[i])**2

        print 'RMS is %s' % squareSum

        return (squareSum/len(v1))**0.5

    def onSize(self, e=None):
        self.imgSize = self.imgSizer.GetSize()[1]
        print 'Height of image sizer is '+str(self.imgSize)
        self.displayImg = self.currentImg.Scale(self.imgSize, self.imgSize)
        self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
        self.panel.Refresh()
        e.Skip()

    def onImageClick(self, e=None):
        '''
        When the blank image is clicked when the program first loads, it brings
        up a file dialog.  The click binding is then removed'
        '''
        self.onLoad()
        self.myImg.Unbind(wx.EVT_LEFT_DOWN)


# Run the program
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Square().Show()
    app.MainLoop()
