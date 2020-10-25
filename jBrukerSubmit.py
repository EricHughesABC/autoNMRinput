"""
Program derived from examples by Greg Moore.
https://wiki.python.org/jython/SwingExamples#JTextField
"""


import os
import csv
import json
import platform
import readcsv243A

from javax.swing import JTable, JButton, JFrame, JPanel,  JTextField, JLabel,  JList, JScrollPane, JOptionPane
from javax.swing.table import DefaultTableModel
from java.awt import  BorderLayout,Dimension, FlowLayout, Color


class JBrukerSubmit:

    colHeads = ('sample #',
                'Name',
                'Experiment',
                'Solvent',
                'Group',
                'Member',
                'Sample Name')
                    
    basedir = r"c:\Bruker\Topspin4.0.8\exp\stan\nmr\py\user"

    def listSubmit(self, event):
        # Ask for starting carousel position and submit experimets to topspin
        # obtain file name of CSV file
        selected = self.list.selectedIndex
        csvName = self.data[selected]
        
        # Create check dialog before submitting data to auromation
        submitString = "submit " + csvName + " starting at carousel position " + self.carouselStartingPosition.text
        result = JOptionPane.showConfirmDialog(self.frame, submitString )
        
        # if submission confirmed 
        if result == 0:
            # submit csv file to automation
            ret = readcsv243A.submitNMRexpts( ["dummyProgName", csvName, self.carouselStartingPosition.text] )
            # if successful or not update status string
            if ret == 0:
                self.statusLabel.text = "File " + csvName + " Submitted to TOPSPIN  Starting at Carousel Position " + self.carouselStartingPosition.text        
                self.panelStatusLabel.setBackground(Color.GREEN)
            elif ret == 1:
                self.statusLabel.text = "Carousel Position not a number"
                self.panelStatusLabel.setBackground(Color.RED)
            elif ret == 2:
                self.statusLabel.text = "Incompatible experiment chosen for spectrometer"
                self.panelStatusLabel.setBackground(Color.RED)        
            elif ret == 3:
                self.statusLabel.text = "Holder starting position is not between 1 and 60 inclusive"
                self.panelStatusLabel.setBackground(Color.RED)
            elif ret == 4:
                self.statusLabel.text = "Too many samples for starting position chosen"
                self.panelStatusLabel.setBackground(Color.RED)
            
            # if an error occured display error message also in a warning dialog too.            
            if ret in [1,2,3,4]:
                JOptionPane.showMessageDialog(self.frame, self.statusLabel.text);
        
        
    def listSelect(self,event):
        # Process the events from the list box and update the label
        selected = self.list.selectedIndex
        if selected >= 0:
        
            # update file label
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

            # convert dictionary items to a list to display in table
            self.tableData = []
            for r in self.expt_list:
                self.tableData.append([r['sample #'],
                                       r['Name'],
                                       r['Experiment'],
                                       r['Solvent'],
                                       r['Group'],
                                       r['Member'],
                                       r['Sample Name']])

            # display csv table in table view
            colNames = JBrukerSubmit.colHeads
            dataModel = DefaultTableModel(self.tableData, colNames)
            self.table = JTable(dataModel) 
            self.scrollPaneTable.getViewport().setView((self.table))

            
    def returnCSVlist(self):
        # read in csv files ommitting any that are created after auto submission and return as list of strings
        csvlist = [ f for f in os.listdir(JBrukerSubmit.basedir) if (f.endswith(".csv")) and (f[-5] != '4')]      
        return csvlist
        
    def listUpdate(self, event):
        # when update button clicked renew csv list
        self.data = self.returnCSVlist()
        self.list.setListData(self.data)


    def checkCarouselNumber(self, event):
        # check that carousel field is an integer change background to white if okay
        # red if not.
    	self.cnumber = self.carouselStartingPosition.text
    	try:
    		self.cnumber = int(self.cnumber)
    		self.carouselStartingPosition.background = Color.WHITE
    	except:
    		self.carouselStartingPosition.background = Color.RED


    def __init__(self):

        # These lines setup the basic frame, size and layout
        # the setDefaultCloseOperation so that only the window closes and not TOPSPIN
        self.frame = JFrame("Submit NMR Experimets")
        self.frame.setSize(1000, 390)
        self.frame.setLayout(BorderLayout())
        self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

        # set up the list and the contents of the list
        # the python tuple get converted to a Java vector
        self.data = self.returnCSVlist()
        self.list = JList(self.data, valueChanged = self.listSelect)
        self.spane = JScrollPane()
        self.spane.setPreferredSize(Dimension(125,150))
        self.spane.getViewport().setView((self.list))
        panel = JPanel()
        panel.add(self.spane)

        # define buttons
        bpanel = JPanel()
        btnS = JButton('Submit File',actionPerformed=self.listSubmit)
        btnU = JButton('Update List',actionPerformed=self.listUpdate)

        # label displaying CSV file selected
        self.label = JLabel('Selected File', JLabel.CENTER)
        
        # label to display warnings and confirm expriments submitted
        self.statusLabel = JLabel('Status', JLabel.CENTER)
        
        # Create table to display csv file
        self.tableData = []
        
        for r in range(10):
            self.tableData.append(["",]*len(JBrukerSubmit.colHeads))

        colNames = JBrukerSubmit.colHeads
        dataModel = DefaultTableModel(self.tableData, colNames)
        self.table = JTable(dataModel)
               
        self.scrollPaneTable = JScrollPane()
        self.scrollPaneTable.setPreferredSize(Dimension(700,200))
        
        self.scrollPaneTable.getViewport().setView((self.table))

        panelTable = JPanel()
        panelTable.add(self.scrollPaneTable)
        
        # create text field to get carousel starting position
        self.carouselLabel = JLabel( "Carousel Position")
        self.carouselStartingPosition = JTextField('1',10, keyPressed = self.checkCarouselNumber)
        
        # add widgets to do with manupulating csv list in FlowLayout Mode
        panelList = JPanel()
        panelList.setLayout(FlowLayout())
        panelList.setPreferredSize(Dimension(170,200))
               
        panelList.add(btnU)
        panelList.add(panel)
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