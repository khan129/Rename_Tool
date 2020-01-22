import maya.cmds as cmds
from PySide2 import QtWidgets
import maya.OpenMayaUI as apiUI
from shiboken2 import wrapInstance

class renameSelected(QtWidgets.QDialog):
    def get_main_window(): 
        """
        Gets main window in maya. 

        Args:
            None
        Returns:
            maya_main_window (Pyside.Widget)
        """
        main_window_parent = maya.OpenMayaUI.MQtUtil.mainWindow() 
        maya_main_window = wrapInstance(long(main_window_parent), QtWidgets.QWidget) 
        return maya_main_window 

    def __init__(self, parent=get_main_window()):
        """
        Runs gui set up. 

        Args:
            parent (Pyside.Widget)
        """
        super(renameSelected, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle("Rename Joints")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        
        # Add Widgets
        self.charname_label = QtWidgets.QLabel("Enter Character Name")
        self.charname_input = QtWidgets.QLineEdit("Bob")
        self.side_label = QtWidgets.QLabel("Select Side")
        self.r_side = QtWidgets.QCheckBox("Right")
        self.l_side = QtWidgets.QCheckBox("Left")
        self.c_side = QtWidgets.QCheckBox("Center")
        self.anatomy_label = QtWidgets.QLabel("Enter Anatomy Part")
        self.anatomy_input = QtWidgets.QLineEdit("leg")
        self.rename_btn = QtWidgets.QPushButton("Rename")

        # Add Layout
        self.layout.addWidget(self.charname_label)
        self.layout.addWidget(self.charname_input)
        self.layout.addWidget(self.side_label)
        self.layout.addWidget(self.r_side)
        self.layout.addWidget(self.l_side)
        self.layout.addWidget(self.c_side)
        self.layout.addWidget(self.anatomy_label)
        self.layout.addWidget(self.anatomy_input)
        self.layout.addWidget(self.rename_btn)

        # Add Connections
        self.rename_btn.clicked.connect(self.get_inputs)

    def get_inputs(self):
        """
        Gets inputs from gui
        """

        joint_chain = cmds.listRelatives(allDescendents=True, type='joint')
        for joint in reversed(joint_chain):
            cmds.select(joint,add=True)
        selected_joints = cmds.ls(orderedSelection = True)


        charname = self.charname_input.text()
        anatomy= self.anatomy_input.text()
        if self.l_side.isChecked():
            side = 'l'
        elif self.r_side.isChecked():
            side = 'r'
        elif self.c_side.isChecked():
            side = 'c'
        else:
            print "pick side please"
            
        # bn stands for bind
        type_ = 'bn'
        version = 0
        last_joint = selected_joints[len(selected_joints)-1]
        print last_joint
        for joint in selected_joints:
            version = version + 1 
            if joint == last_joint:
                # bind end joint
                type_='be'
            v = '%02d' % version
            name = "{}_{}_{}{}_{}".format(charname, side, anatomy, v, type_)
            cmds.rename(joint,name)
        cmds.select(all=False)

renameSelected().show()

