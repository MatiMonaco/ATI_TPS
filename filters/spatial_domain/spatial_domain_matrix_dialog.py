from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets,QtCore

class SpatialDomainMatrixInputDialog(QtWidgets.QDialog):
    def __init__(self, mask, mask_size):
        super().__init__()
        self.mask_size = mask_size
        self.mask = mask
       
        self.setupUi()
        
        
     

    def setupUi(self):
        layout= QtWidgets.QVBoxLayout(self)
      
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok, self)

        #####
      
        self.maskWeights = QtWidgets.QTableWidget()
        self.maskWeights.setObjectName("maskWeights")

        self.generateMatrixTable()

        self.maskWeights.horizontalHeader().setVisible(False)
        self.maskWeights.verticalHeader().setVisible(False)
        self.maskWeights.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.maskWeights.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.maskWeights)
        
        #####

        buttonBox.accepted.connect(self.updateMask)
        buttonBox.rejected.connect(self.rejected)
        layout.addWidget(buttonBox)


        pixmapi = getattr(QtWidgets.QStyle, 'SP_DirOpenIcon')
        icon = self.style().standardIcon(pixmapi)
        self.setWindowIcon(icon)
        self.setWindowTitle("Enter Mask Weights")

     



       
    def updateMask(self):
        for i in range(self.mask_size):
            for j in range(self.mask_size):
                text = self.maskWeights.cellWidget(i, j).text()
             
                if text != '':
                    self.mask[i,j] = int(text)
        self.accept()

    def generateMatrixTable(self):
      
        self.maskWeights.setRowCount(self.mask_size)
        self.maskWeights.setColumnCount(self.mask_size)
        onlyDouble = QDoubleValidator()
        for i in range(self.mask_size):
            for j in range(self.mask_size):
                lineEdit = QtWidgets.QLineEdit()

                #item = QtWidgets.QTableWidgetItem()
                lineEdit.setAlignment(QtCore.Qt.AlignCenter)
                lineEdit.setText(str(self.mask[i, j]))
                lineEdit.setValidator(onlyDouble)
                self.maskWeights.setCellWidget(i,j,lineEdit)
                #self.maskWeights.setItem(i, j, item)

    def getMaskWeights(self):
        
        return self.mask

