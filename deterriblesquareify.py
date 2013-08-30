#!/usr/bin/env python2.7

import wx
import numpy as np
from scipy.misc import imsave

debug = False

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

        # bind image resize event
        self.Bind(wx.EVT_SIZE, self.onSize)

        # create image object
        self.imgArray = np.zeros((1,1,3), dtype='uint8')
        self.myImg = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(self.numpyToWxImage(self.imgArray)))

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
            self.fileName = dlg.GetFilename()

            # disable logging (.tif[f]s with funny tags cause a pop-up error)
            noLog = wx.LogNull()

            # save the original for resetting
            self.originalImg = wx.Image(self.imagePath)

            # reenable logging
            del noLog

            # goof around with formats
            self.imgArray = self.wxImageToNumpy(self.originalImg)

            # scale the original for display (saves a step for the first display)
            self.displayImg = self.originalImg.Scale(self.imgSize, self.imgSize)
            #self.displayImg = self.numpyToWxImage(self.imgArray).Scale(self.imgSize, self.imgSize)

            # display the loaded image
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()
        dlg.Destroy()

    def onImageClick(self, e=None):
        '''
        When the blank image is clicked when the program first loads, it brings
        up a file dialog.  The click binding is then removed'
        '''
        
        # load an image
        self.onLoad()

        # unbind clicking on the image
        self.myImg.Unbind(wx.EVT_LEFT_DOWN)

    def onSave(self, e=None):
        '''
        Saves the image in an arbitrary format.
        '''
        print 'Saving...'
        dlg = wx.FileDialog(self, "Choose a file name", self.dirname, 'CORRECTED_'+str(self.fileName), "*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.saveFileName = dlg.GetFilename()
            self.saveDirName = dlg.GetDirectory()
            self.newImagePath = dlg.GetPath()
            imsave(self.newImagePath, self.imgArray)
        dlg.Destroy()

    def onReset(self, e=None):
        '''
        Reset the currently loaded image to its original state.
        '''

        # only reset if a file has previously been loaded
        if self.imagePath != '':
            print 'Resetting image...'
            # reset array which is manipulated
            self.imgArray = self.wxImageToNumpy(self.originalImg)
            # reset display image
            self.displayImg = self.originalImg.Scale(self.imgSize, self.imgSize)
            self.myImg.SetBitmap(wx.BitmapFromImage(self.displayImg))
            self.panel.Refresh()

    def onAuto(self, e=None):
        '''
        Automatically finds the broken quadrant and adjusts it to match its neighbors.
        '''

        print 'Autotuning...'

        # TODO maybe switch the 0 and 1
        xDim = self.imgArray.shape[0]
        yDim = self.imgArray.shape[1]

        ## construct vectors of grayscale values on adjacent quadrant edges
        #TODO read grayscale values as matrix

        # bottom of Q1 and top of Q4
        q1b = self.imgArray[(xDim/2 - 1), (yDim/2):yDim, 1]
        q4t = self.imgArray[(xDim/2), (yDim/2):yDim, 1]

        # left of Q1 and right of Q2
        q1l = self.imgArray[0:(xDim/2), yDim/2, 1]
        q2r = self.imgArray[0:(xDim/2), yDim/2 - 1, 1]

        # bottom of Q2 and top of Q3
        q2b = self.imgArray[(xDim/2 - 1), 0:(yDim/2), 1]
        q3t = self.imgArray[(xDim/2), 0:(yDim/2), 1]

        # right of Q3 and left of Q4
        q3r = self.imgArray[(xDim/2):xDim, (yDim/2 - 1), 1]
        q4l = self.imgArray[(xDim/2):xDim, (yDim/2), 1]

        ## find which quadrant is most likely to be the maladjusted one
        # calculate rms difference for each edge
        rmsRight = self.rms(q1b, q4t)
        rmsTop = self.rms(q1l, q2r)
        rmsLeft = self.rms(q2b, q3t)
        rmsBottom = self.rms(q3r, q4l)

        # each quadrant has two edges
        rmsQ1 = rmsTop + rmsRight
        rmsQ2 = rmsTop + rmsLeft
        rmsQ3 = rmsLeft + rmsBottom
        rmsQ4 = rmsBottom + rmsRight

        # find the largest
        if (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ1):
            q = 1
            insideEdge = np.append(q1l, q1b)
            outsideEdge = np.append(q2r, q4t)
            print 'Q1 will be adjusted'
        elif (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ2):
            q = 2
            insideEdge = np.append(q2r, q2b)
            outsideEdge = np.append(q1l, q3t)
            print 'Q2 will be adjusted'
        elif (max(rmsQ1, rmsQ2, rmsQ3, rmsQ4) == rmsQ3):
            q = 3
            insideEdge = np.append(q3r, q3t)
            outsideEdge = np.append(q4l, q2b)
            print 'Q3 will be adjusted'
        else:
            q = 4
            insideEdge = np.append(q4l, q4t)
            outsideEdge = np.append(q3r, q1b)
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
            if (debug):
                print 'n is %s' % n
            # find new adjusted RMS value
            newRMSValue = self.rmsAdjust(insideEdge, outsideEdge, n)
            iter += 1
            if (debug):
                print 'oldRMSValue is %s' % oldRMSValue
                print 'newRMSValue is %s' % newRMSValue

        ## adjust the quadrant
        if (debug):
            print 'Adjusting Q%d by %d grayscale values' % (q, (n - nSign))
        self.adjustQuadrant(q, n - nSign)
        print 'FINISHED AUTOTUNE'

    def adjustQuadrant(self, q, n, e=None):
        '''
        Quadrant q is 1, 2, 3, or 4.  n is the adjustment to the RGB values.
        '''

        # the origin is at the top left of the image
        # TODO maybe switch the 0 and 1 in the shape array accesses
        if (q == 1):    # top right quadrant
            minx = self.imgArray.shape[0]/2 + 0
            maxx = self.imgArray.shape[0]
            miny = 0
            maxy = self.imgArray.shape[1]/2
        elif (q == 2):    # top left quadrant
            minx = 0
            maxx = self.imgArray.shape[0]/2
            miny = 0
            maxy = self.imgArray.shape[1]/2
        elif (q == 3):    # bottom left quadrant
            minx = 0
            maxx = self.imgArray.shape[0]/2
            miny = self.imgArray.shape[1]/2 + 0
            maxy = self.imgArray.shape[1]
        elif (q == 4):    # bottom right quadrant
            minx = self.imgArray.shape[0]/2 + 0
            maxx = self.imgArray.shape[0]
            miny = self.imgArray.shape[1]/2 + 0
            maxy = self.imgArray.shape[1]
        else:
            raise ValueError, 'Invalid quadrant specified.'

        # convert to signed 32-bit int
        imgArrayCopy = np.int32(self.imgArray)

        # shift the RGB values in each pixel
        imgArrayCopy[miny:maxy,minx:maxx,:] += n

        # clip values to account for wrapping of RGB values
        imgArrayCopy = np.clip(imgArrayCopy, 0, 255)

        # convert back to signed 8-bit int
        self.imgArray = np.uint8(imgArrayCopy)

        # display altered image
        self.displayImg = self.numpyToWxImage(self.imgArray).Scale(self.imgSize, self.imgSize)
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

        # make array manipulable
        a.flags.writeable = True

        return a

    def numpyToWxImage(self, a):
        '''
        Converts a numpy array to a wx.Image.
        '''

        # note the use of the ascontiguousarray method, otherwise it may break for big arrays
        return wx.ImageFromBuffer(a.shape[0], a.shape[1], np.ascontiguousarray(a))
        
    def rms(self, v1, v2):
        '''
        Gives the RMS difference between vectors v1 and v2
        '''
        return self.rmsAdjust(v1, v2, 0.0)

    def rmsAdjust(self, v1, v2, n):
        '''
        Finds the RMS difference between two vectors, with the values in the
        first vector adjusted by n.
        '''

        # important to convert to float, otherwise RMS wraps and is not correct
        newV1 = np.array(v1, dtype=float)
        newV2 = np.array(v2, dtype=float)

        return np.sqrt(np.mean((newV1 + n - newV2)**2))

    def onSize(self, e=None):
        # scale image to height of sizer
        self.imgSize = self.imgSizer.GetSize()[1]
        self.myImg.SetBitmap(wx.BitmapFromImage(self.numpyToWxImage(self.imgArray).Scale(self.imgSize, self.imgSize)))
        self.panel.Refresh()
        e.Skip()

# Run the program
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Square().Show()
    app.MainLoop()
