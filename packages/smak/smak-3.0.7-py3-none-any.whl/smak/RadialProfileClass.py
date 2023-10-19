import tkinter
from tkinter.ttk import Button

#third party
import Pmw
import numpy as np

#local
import globalfuncs
import MyGraph

class RadialProfileParams:
    def __init__(self,maindisp, root, datachan):
        self.maindisp = maindisp
        self.root = root
        self.datachan = datachan

class RadialProfile():
    def __init__(self, imgwin, mapdata, ps):
                #get center coordinate... (use dialog)
        self.ps = ps
        self.imgwin = imgwin
        self.mapdata = mapdata
        
        self.radprofDialog=Pmw.Dialog(self.imgwin,title="Radial Profile",buttons=('OK','Cancel'),defaultbutton='OK',
                                     command=self.enterRadDialog)
        h=self.radprofDialog.interior()
        h.configure(background='#d4d0c8')
        #two entries and get pos button
        self.radxcentpos=Pmw.EntryField(h,labelpos='w',label_text='x:',entry_width=7,validate='real',hull_background='#d4d0c8',label_background='#d4d0c8')
        self.radycentpos=Pmw.EntryField(h,labelpos='w',label_text='y:',entry_width=7,validate='real',hull_background='#d4d0c8',label_background='#d4d0c8')
        self.radxcentpos.pack(side=tkinter.LEFT,padx=2,pady=2)
        self.radycentpos.pack(side=tkinter.LEFT,padx=2,pady=2)
        #get position button        
        b=Button(h,text='Get Pos',command=self.getradcentpos,style='ORANGE.TButton',width=7)
        b.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.radprofDialog.show()

        self.radprofDialog.userdeletefunc(func=self.kill)

    def kill(self):
        self.radprofDialog.withdraw()



    def getradcentpos(self):
        self.ps.maindisp.main.show()
        self.ps.maindisp.PMlock.acquire()
        self.ps.maindisp.startPMgetpos()
        self.putradcentpos()

    def putradcentpos(self):
        if self.ps.maindisp.PMlock.locked():
            self.ps.root.after(250,self.putradcentpos)
        else:
            self.radxcentpos.setvalue(self.ps.maindisp.markerexport[0])
            self.radycentpos.setvalue(self.ps.maindisp.markerexport[1])            
        
    def enterRadDialog(self,result):
        #check result
        if result=='Cancel':
            #close too
            self.radprofDialog.destroy()
            return
        #verify
        if not self.radxcentpos.valid() or not self.radycentpos.valid():
            print('need center values')
            return
        #get image data
        if self.ps.datachan.get()==():
            print('select data channel')
            return
        datind=self.mapdata.labels.index(self.ps.datachan.getvalue()[0])+2
        #get search indices
        if self.ps.maindisp.zmxyi[0:4]!=[0,0,-1,-1]:            
            dindices=self.ps.maindisp.zmxyi
        else:
            dindices=[0,0,self.mapdata.data.shape[0],self.mapdata.data.shape[1]]

        print(dindices)
        #do calc
        x0=float(self.radxcentpos.getvalue())
        y0=float(self.radycentpos.getvalue())
        #get pixels from data
        x0i=globalfuncs.indexme(self.mapdata.xvals,x0)
        y0i=globalfuncs.indexme(self.mapdata.yvals,y0)
        rad=max(self.mapdata.data.get(0).shape) #NEED TO CALC in pixels
        
        gridX=self.mapdata.data.get(0)[dindices[1]:dindices[3],dindices[0]:dindices[2]]-x0
        gridY=self.mapdata.data.get(1)[dindices[1]:dindices[3],dindices[0]:dindices[2]]-y0
        R=np.sqrt(gridX**2 + gridY**2)
        pz=abs(gridX[0,0]-gridX[0,1])
        print (pz)
        R=np.rint(R/(pz)).astype(int)

        gd=self.mapdata.data.get(datind)[dindices[1]:dindices[3],dindices[0]:dindices[2]]
        ints=np.bincount(R.ravel(),weights=gd.ravel())
        print (ints)
        dist=np.arange(len(ints))*pz
        
        if not self.ps.maindisp.linegraph2present:
            self.ps.maindisp.linegraph2present=1
            self.ps.maindisp.newlineplot2=Pmw.MegaToplevel(self.ps.maindisp.master)
            self.ps.maindisp.newlineplot2.title('Radial Plot View')
            self.ps.maindisp.newlineplot2.userdeletefunc(func=self.ps.maindisp.killlineplot2)           
            h=self.ps.maindisp.newlineplot2.interior()
            self.ps.maindisp.graphx2=MyGraph.MyGraph(h,whsize=(4.5,4),side=tkinter.LEFT,padx=2,graphpos=[[.15,.1],[.9,.9]])

        else:
            #clear old
            self.ps.maindisp.newlineplot2.title('Radial Plot View')
            self.ps.maindisp.graphx2.cleargraphs()
      
        self.ps.maindisp.graphx2.plot(tuple(dist),tuple(ints),text='XV',color='green')        
        self.ps.maindisp.graphx2.draw()
        self.ps.maindisp.newlineplot2.show()