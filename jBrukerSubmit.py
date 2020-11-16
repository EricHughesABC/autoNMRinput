"""
Program derived from examples by Greg Moore.
https://wiki.python.org/jython/SwingExamples#JTextField
"""


import os
import csv
# import json
import platform
import readcsv243A

from javax.swing import JTable, JButton, JFrame, JPanel,  JTextField, JLabel,  JList, JScrollPane, JOptionPane, JSeparator
from javax.swing.table import DefaultTableModel
from java.awt import  BorderLayout,Dimension, FlowLayout, Color

def checkExperimentsWillRun(expt_list):
    """
    test whether all pulse sequences will run on current spectrometer.

    Parameters
    ----------
    expt_list : List of Dictionaries
        List of dictionaries read in from a csv file that has experiment
        information  such as solvent, pulse sequence, title

    Returns
    -------
    ok : Bool
    
    pulseSequence : String
        pulse sequence name that cannot run on sprectrometer 
        or "" if everything okay

    """
    for rw in expt_list:
        if  rw['Experiment'] == "High Field":
            continue
        if rw['Experiment'] not in readcsv243A.experiments[readcsv243A.spec_name].keys():
            return False, rw['Experiment']
        
        return True, ""
    

def returnJTableData( expt_list, carouselNumber):
    """
    return a list of lists (dataTable) containing experiment data for use 
    by a JTable widget.
    The dataTable will be sorted based on block/sample number.
    A carousel number will be inserted into the table for each different 
    sample, if the sample is destinned for low field and a zero will be added
    if sample is fron high field spectrometers
    The file name will be given a unique seconds number if it is a different sample
    starting from 61

    Parameters
    ----------
    expt_list : List
        List of dictionaries read in from csv file originating from excel sheet 
    carouselNumber : integer
        Starting position number in carousel where samples will be put

    Returns
    -------
    tableData : List
        2-D list of lists that has been sorted on sample/block number

    """

    # sort csv file based on block number
    # assume students may have not started from beginning of block and 
    # not added tubes sequentially.
    
    tableData = [] # list of lists to be used by jTable
    block_number = [] # list of list to hold sample number and index into list
    
    for i,r in enumerate(expt_list):
        block_number.append([int(r['sample #']),i])
    
    # sort block number list based on block number min to max based on type being integers   
    block_number.sort()
    
    # copy sorted dict data into a simple list of lists
    for jj,ii in block_number:
         r = expt_list[ii]
    
         tableData.append([int(r['sample #']),
                            r['Name'],
                            r['Experiment'],
                            r['Solvent'],
                            r['Group'],
                            r['Member'],
                            r['Sample Name']])
                            
    # Alter file name so that they are unique for each sample
    i=61
    oldblockNumber = int(tableData[0][0])
    for rw in tableData:
        currentBlockNumber = int(rw[0])
        if oldblockNumber != currentBlockNumber:
            i = i+1
            
        if len(rw[1]) == 5:
            rw[1] = "0" + str(rw[1])
        rw[1] = str(rw[1]) + str(i)
        print "update file name", i, rw[1]
        oldblockNumber = currentBlockNumber
    
    # insert holder number based on experiment performed on low field
    # if sample for high field analysis set holder number to 0
    # only increment holder/carousel number if new sample
    
    sampleNumberOld = int(tableData[0][0])
    
    for i,r in enumerate(tableData):
        sampleNumber = int(r[0])
        lowField = True
        if r[2] == 'High Field':
            lowField = False
        # lowField = r[2] != 'High Field'

        # if new sample and low field experiment
        # increment carousel Number
        if sampleNumber > sampleNumberOld and lowField:
            carouselNumber += 1
        
        # insert carousel number into table if lowfield experiment
        # else insert a Zero
        if lowField:
            r.insert(1, carouselNumber)
        else:
            r.insert(1,0)
        
        # update old sample number
        sampleNumberOld = sampleNumber

    return tableData


class JBrukerSubmit:

    colHeads = ('block/sample #',
                'Holder',
                'Name',
                'Experiment',
                'Solvent',
                'Group',
                'Member',
                'Sample Name')
                
    if platform.node() == 'DM-CHEM-200':
        basedir = r"W:\downloads\Eric\jython"
    elif platform.node() == 'ERIC-PC':
        basedir =  r"C:\Users\ERIC\Dropbox\projects\programming\2020\python\autoNMRinput"
    else:
        # running from Bruker spectrometers
        basedir = "/data/downloads/Eric"
    
    
    def listSubmit(self, event):
        """Submit highlighted to csv file to automation folder of spectrometer
        """
        
        # Ask for starting carousel position and submit experimets to topspin
        # obtain file name of CSV file
        selected = self.list.selectedIndex
        csvName = self.data[selected]
        
        # if no selected file and table is empty just return
        if self.label.text == "Selected File":
            return
        
        # Create check dialog before submitting data to automation
        self.dataTableModel.dataVector
#        submitString = "submit " + csvName + " starting at carousel position " + self.carouselStartingPosition.text 
        submitString = "submit " + csvName + " starting at carousel position " + str((self.dataTableModel.dataVector)[0][1]) 
        result = JOptionPane.showConfirmDialog(self.frame, submitString )
        
        # if submission confirmed 
        if result == 0:
            # submit csv file to automation
            ret = readcsv243A.submitNMRexpts( [self.dataTableModel.dataVector, csvName, self.carouselStartingPosition.text] )
            # if successful or not update status string
            if ret == 0:
                self.statusLabel.text = "File " + csvName + " Submitted to TOPSPIN  Starting at Carousel Position " + str((self.dataTableModel.dataVector)[0][1])         
                self.panelStatusLabel.setBackground(Color.GREEN)
            elif ret == 1:
                self.statusLabel.text = "Carousel Position not a number"
                self.panelStatusLabel.setBackground(Color.RED)
            elif ret == 2:
                self.statusLabel.text = "Incompatible experiment chosen for spectrometer"
                self.panelStatusLabel.setBackground(Color.RED)        
            elif ret == 3:
                self.statusLabel.text = "A holder starting position is not between 1 and 60 inclusive"
                self.panelStatusLabel.setBackground(Color.RED)
            elif ret == 4:
                self.statusLabel.text = "Too many samples for starting position chosen"
                self.panelStatusLabel.setBackground(Color.RED)
            
            # if an error occured display error message also in a warning dialog too.            
            if ret in [1,2,3,4]:
                JOptionPane.showMessageDialog(self.frame, self.statusLabel.text);
        
        
    def listSelect(self,event):
        """When a new csv file is selected from the list
        read in the file and display its contents in the table.
        Unordered csv files will be ordered based on the block/sample number.
        A holder column will be added to the CSV data based on the carousel 
        starting position.
        """
        
        # Process the events from the list box and update the label
        # get the index from the list and then the filename 
        selected = self.list.selectedIndex
        if selected >= 0:
        
            # update file label and set background colour to normal
            csvName = self.data[selected]
            self.label.text = csvName
            self.panelLabel.setBackground(self.standardBackgroundColor)
            
            # reset status label
            self.statusLabel.text = "Status"
            self.panelStatusLabel.setBackground(self.standardBackgroundColor)
            #
            # update table by reading in csv file
            # read in csv file and store as a list of dictionaries
            # one dictionary for each line   
            fn = csvName
            self.expt_list = []
            f = open(os.path.join(JBrukerSubmit.basedir, fn), 'r')
            reader = csv.DictReader(f)
            for row in reader:		
                self.expt_list.append(row)
            f.close()

            
            # get carousel starting position, if the value cannot be converted
            # to an integer reset it to 1 and reset the GUI to 1
            try:
                self.cnumber = int(self.carouselStartingPosition.text)
            except:
                self.cnumber = 1
                self.self.carouselStartingPosition.text = "1"
            
            # get the csv data into a list of lists form ready for displaying
            self.tableData = returnJTableData( self.expt_list, self.cnumber)

            # display csv table in table view
            colNames = JBrukerSubmit.colHeads
            # transfer the data over to the table model
            self.dataTableModel.setDataVector(self.tableData, colNames)
            # display the table in the GUI
            self.scrollPaneTable.getViewport().setView((self.table))
            
            # check to see if experiments will run on the spectometer
            ok, pulseSequence =  checkExperimentsWillRun(self.expt_list)
                
            if not ok:
                # display warning dialog
                warningText = pulseSequence + " cannot be run on this spectrometer"
                JOptionPane.showMessageDialog(self.frame, warningText);
                

            
    def returnCSVlist(self, hiddenFiles):
        """ read in csv files ommitting any that are created after 
        auto submission and return as list of strings.
        Miss out any that have been hidden"""
        csvlist = [ f for f in os.listdir(JBrukerSubmit.basedir) if (f.endswith(".csv")) and (f[-6] not in ['A', 'B', 'N'])]
        csvlist = [ f for f in csvlist if f not in self.hiddenFiles]
        return csvlist
        
    def listUpdate(self, event):
        """ when update button clicked renew csv list """
        self.data = self.returnCSVlist(self.hiddenFiles)
        self.list.setListData(self.data)


    def checkCarouselNumber(self, event):
        """ check that carousel field is an integer change background to white
        if okay, red if not."""
        
    	self.cnumber = self.carouselStartingPosition.text
    	try:
            self.cnumber = int(self.cnumber)
            self.carouselStartingPosition.background = Color.WHITE
            self.listSelect(event)
    	except:
    		self.carouselStartingPosition.background = Color.RED


    def tableMouseClicked(self, event):
        """Prior to editing the user will click the holder number cell
        more often than not. This function saves the cell row and column and
        the value in the cell prior to editing."""

        
        tble = event.getSource()
        self.rw = tble.getSelectedRow()
        self.cl = tble.getSelectedColumn()
        self.oldHolderValue = tble.getValueAt(self.rw, self.cl)
#        print "table mouse clicked", self.rw, self.cl
        
    def tableChangedCB(self,event):
        """Function is called when a cell is being edited. After the user 
        presses return the data is updated.
        Should only work if Holder column is being edited"""
        
        print "Table Changed"
        tble = event.getSource()
        if (event.keyChar == "\n") and (self.cl != 1):
            tble.setValueAt(self.oldHolderValue, self.rw, self.cl )
            
        elif (event.keyChar == "\n") and (self.cl == 1):
            print "RETURN"
            vlue = tble.getValueAt(self.rw, self.cl)
            print "row", self.rw, "col", self.cl, "value", vlue
            #
            # check to see if new holder number is used by another sample
            # get block number of sample changed
            blckNumber = tble.getValueAt(self.rw, 0)
            #
            # get values in table
            holderAlreadyOccupied = False
            tableValues = self.dataTableModel.dataVector
            for i, rw in enumerate(tableValues):
                print i
                if (int(rw[1]) == int(vlue))  and (int(blckNumber) != int(rw[0])):
                    tble.setValueAt(int(self.oldHolderValue), self.rw, 1 )
                    holderAlreadyOccupied = True
                    warningText = "Holder " + str(vlue) + " already used for sample " + str(rw[0])
                    JOptionPane.showMessageDialog(self.frame, warningText);

                    break  
            #
            # check to see if any other rows with same sample number need to be updated
            if not holderAlreadyOccupied:
                for i, rw in enumerate(tableValues):
                    if int(blckNumber) == int(rw[0]):
                        tble.setValueAt(int(vlue), i, 1 )
                
        
    # def tableKeyPressedCB(self, event):
    #     print "tableKeyPressedCB"
    #     tble = event.getSource()
    #     if event.keyChar == "\n":
    #         print "RETURN"
    #         vlue = tble.getValueAt(self.rw, self.cl)
    #         print "row", self.rw, "col", self.cl, "value", vlue

    #     elif (event.keyChar).isdigit():
    #         print "event.keyChar", event.keyChar
            
    #         self.rw = tble.getSelectedRow()
    #         self.cl = tble.getSelectedColumn()
        
    def listShowAllFiles(self,event):
        fp = open("hiddenFiles.txt", 'w')
        fp.write('zzz\n')
        fp.close()
        self.hiddenFiles = ['zzz']
        self.listUpdate(event)
        
    def listHideFile( self, event):
    
        # find highlighted csv file name
        selected = self.list.selectedIndex
        csvName = self.data[selected]
        # add csv file name to hidden csv files list
        self.hiddenFiles.append(csvName)
        # update label above table view
        self.label.text = "Selected File"
        self.panelLabel.setBackground(self.standardBackgroundColor)
        # display csv table in table view

        # set table to blanks
        self.tableData = []
        for i in range(18):
            self.tableData.append(["",] * len(JBrukerSubmit.colHeads))

        self.dataTableModel.setDataVector(self.tableData, JBrukerSubmit.colHeads)
        self.listUpdate(event)
        
        # save hiddenFiles file
        fp = open("hiddenFiles.txt", 'w')
        for f in self.hiddenFiles:
            fp.write(f+'\n')
        fp.close()
        

        
    def __init__(self):
        
        self.rw = 0 # table row
        self.cl = 0 # table column
        
        # load hidden files list
        
        self.hiddenFiles = ["zzz"]
        
        if os.path.exists("hiddenFiles.txt"):       
            fp = open("hiddenFiles.txt", "r")
            self.hiddenFiles = fp.readlines()
            fp.close()
        
        self.hiddenFiles = [f.strip() for f in self.hiddenFiles]
        print self.hiddenFiles

        # These lines setup the basic frame, size and layout
        # the setDefaultCloseOperation so that only the window closes and not TOPSPIN
        self.frame = JFrame("Submit NMR Experimets")
        self.frame.setSize(1200, 440)
        self.frame.setLayout(BorderLayout())
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

        # set up the list and the contents of the list
        # the python tuple get converted to a Java vector
        self.data = self.returnCSVlist(self.hiddenFiles)
        self.list = JList(self.data, valueChanged = self.listSelect)
        self.spane = JScrollPane()
        self.spane.setPreferredSize(Dimension(145,150))
        self.spane.getViewport().setView((self.list))
        panel = JPanel()
        panel.add(self.spane)

        # define buttons
        bpanel = JPanel()
        btnS = JButton('Submit File',actionPerformed=self.listSubmit)
        btnU = JButton('Update List',actionPerformed=self.listUpdate)
        btnHideFile = JButton('Hide File', actionPerformed=self.listHideFile)
        btnShowAllFiles  = JButton( 'Show All Files', actionPerformed=self.listShowAllFiles )

        # label displaying CSV file selected
        self.label = JLabel('Selected File', JLabel.CENTER)
        
        # label to display warnings and confirm expriments submitted
        self.statusLabel = JLabel('Status', JLabel.CENTER)
        
        # Create table to display csv file
        self.tableData = []
        
        for r in range(18):
            self.tableData.append(["",]*len(JBrukerSubmit.colHeads))

        colNames = JBrukerSubmit.colHeads
        self.dataTableModel = DefaultTableModel(self.tableData, colNames)
        self.table = JTable(self.dataTableModel, 
                            keyTyped=self.tableChangedCB,
                            mouseClicked=self.tableMouseClicked)
                            
        # set all columns to uneditable except Holder column
        # print dir(self.table)
        # self.table.getColumn(0).setEditable(False)
        # self.table.getColumn(2).setEditable(False)
        # self.table.getColumn(3).setEditable(False)
        # self.table.getColumn(4).setEditable(False)
        # self.table.getColumn(5).setEditable(False)
        # self.table.getColumn(6).setEditable(False)
        
        # self.table = JTable(self.dataTableModel, 
        #                     keyPressed=self.tableKeyPressedCB)
               
        self.scrollPaneTable = JScrollPane()
        self.scrollPaneTable.setPreferredSize(Dimension(900,300))
        
        self.scrollPaneTable.getViewport().setView((self.table))

        panelTable = JPanel()
        panelTable.add(self.scrollPaneTable)
        
        # create text field to get carousel starting position
        self.carouselLabel = JLabel( "Carousel Position", JLabel.CENTER)
        self.carouselStartingPosition = JTextField('1',13, keyPressed = self.checkCarouselNumber)
        
        # add widgets to do with manupulating csv list in FlowLayout Mode
        panelList = JPanel()
        panelList.setLayout(FlowLayout())
        panelList.setPreferredSize(Dimension(170,200))
        
        # set preferred size of buttons
        btnU.setPreferredSize(Dimension(140,20))
        btnS.setPreferredSize(Dimension(140,20))
        btnHideFile.setPreferredSize(Dimension(140,20))
        btnShowAllFiles.setPreferredSize(Dimension(140,20))
        
        
        self.carouselLabel.setPreferredSize(Dimension(140,20))
        self.carouselStartingPosition.setPreferredSize(Dimension(170,20))
        
        panelList.add(btnU)
        panelList.add(panel)
        panelList.add(btnHideFile)
        panelList.add(btnShowAllFiles)
        panelList.add(JSeparator(JSeparator.HORIZONTAL),BorderLayout.LINE_START)
        panelList.add(self.carouselLabel)
        panelList.add(self.carouselStartingPosition)
        panelList.add(btnS)
        
        self.panelLabel = JPanel()
        self.panelLabel.add( self.label)
        self.standardBackgroundColor = self.panelLabel.getBackground()
        
        # put status label in a panel so that background color can be changed
        self.panelStatusLabel = JPanel()
        self.panelStatusLabel.add( self.statusLabel)
        
        # add widgets to frame
        self.frame.add(self.panelLabel, BorderLayout.NORTH)
        self.frame.add(panelList, BorderLayout.WEST)        
        self.frame.add(panelTable, BorderLayout.CENTER)        
        self.frame.add(self.panelStatusLabel, BorderLayout.SOUTH)
                
        self.frame.setVisible(True)

if __name__ == '__main__':
        #start things off.        
        JBrukerSubmit()