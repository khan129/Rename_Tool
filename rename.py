
import sys
import os
import platform
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as apiUI

from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton


class renameSelected(QDialog):
    def getMainWindowPtr(): 
        mayaMainWindowPtr = maya.OpenMayaUI.MQtUtil.mainWindow() 
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWid.QWidget) 
        print mayaMainWindow 
        return mayaMainWindow 
    def __init__(self, parent=None):
        super(renameSelected, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle("renameSelected")
        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        
        #add widget
        self.charname_label = QtWidgets.QLabel("Enter Character Name")
        self.charname_input = QtWidgets.QLineEdit("dragon")
        self.side_label = QtWidgets.QLabel("Select Side")
        self.r_side = QtWidgets.QCheckBox("Right")
        self.l_side = QtWidgets.QCheckBox("Left")
        self.c_side = QtWidgets.QCheckBox("Center")
        self.anatomy_label = QtWidgets.QLabel("Enter Anatomy Part")
        self.anatomy_input = QtWidgets.QLineEdit("leg")
        self.rename_btn = QtWidgets.QPushButton("Rename")

        #sdd layout
        self.layout.addWidget(self.charname_label)
        self.layout.addWidget(self.charname_input)
        self.layout.addWidget(self.side_label)
        self.layout.addWidget(self.r_side)
        self.layout.addWidget(self.l_side)
        self.layout.addWidget(self.c_side)
        self.layout.addWidget(self.anatomy_label)
        self.layout.addWidget(self.anatomy_input)
        self.layout.addWidget(self.rename_btn)

        
        #add connections
        self.rename_btn.clicked.connect(self.get_inputs)



        # Layout Widgets
    def get_inputs(self):

        jntchain = cmds.listRelatives(allDescendents=True, type='joint')
        for jnt in reversed(jntchain):
            cmds.select(jnt,add=True)
        jj = cmds.ls(orderedSelection = True)


        charname = self.charname_input.text()
        anatomy= self.anatomy_input.text()
        if self.l_side.isChecked():
            side = 'l'
        elif self.r_side.isChecked():
            side = 'r'
        elif self.c_side.isChecked():
            side = 'c'
        else:
            side = 'HAHAHA'
        type_ = 'bn'


        version = 0
        lastjnt = jj[len(jj)-1]
        print lastjnt
        for jnt in jj:
            version = version + 1 
            if jnt == lastjnt:
                type_='be'
            v = '%02d' % version
            name = "{}_{}_{}{}_{}".format(charname, side, anatomy, v, type_)
            cmds.rename(jnt,name)
        cmds.select(all=False)





if __name__ == '__main__':
    w = renameSelected(parent=getMainWindowPtr())
    w.show()

