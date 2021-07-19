from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QApplication
import constants
import sys
import json
import time

class SetupControls(QWidget):
    def __init__(self):
        super().__init__()

        # sets window size to constants set in constants.py
        self.setFixedSize(constants.setupResolutionWidth, constants.setupResolutionHeight)

        # creates instances of QLabels, QTextEdits and QPushButtons, as well as set locations
        self.titleLabel = QLabel(self)
        self.titleLabel.move(40,40)

        self.editableTextField = QTextEdit(self)
        self.editableTextField.move(40,80)

        self.cancelButton = QPushButton(self)
        self.cancelButton.move(40,360)
        self.cancelButton.setText('Cancel')
        self.cancelButton.pressed.connect(self.cancelButtonCallback)

        self.nextButton = QPushButton(self)
        self.nextButton.move(360,360)
        self.nextButton.setText('Next')
        self.nextButton.pressed.connect(self.nextButtonCallback)

        self.initialScreen()

        self.installationPageNum = 0
        self.dataObject = None

        self.show()

        return

    def initialScreen(self):
        self.titleLabel.setText('Corgi Inventory Software Setup')
        self.editableTextField.setText('Please use this installer to set up the location data is saved for Corgi Inventory. Any path entered will be created if not existent, or will be wiped and written with an empty configuration.')
        self.editableTextField.setReadOnly(True)

        return

    def touScreen(self):
        self.titleLabel.setText('Terms of Use')
        self.editableTextField.setText('No warranty is provided on this software')
        self.editableTextField.setReadOnly(True)

        return

    def pathScreen(self):
        self.titleLabel.setText('JSON Path')
        self.editableTextField.setText('partsData.json')
        self.editableTextField.setReadOnly(False)

        return


    def statusScreen(self):

        self.statusText = ""

        self.path = self.editableTextField.toPlainText()

        self.titleLabel.setText('Status')
        self.editableTextField.setText(self.statusText)
        self.editableTextField.setReadOnly(True)

        try:
            data = open(self.path, 'r+')
        except:
            newFile = open(self.path, 'w')
            newFile.close()
            self.statusText += 'New JSON file created\n'
            data = open(self.path, 'r+')

        self.emptyDictForParts = {}

        for category in ['Resistors', 'Capacitors']:
            self.emptyDictForParts[category] = {}
            self.statusText = self.statusText + " " + category + " category has been added\n"
            self.editableTextField.setText(self.statusText)

        json.dump(self.emptyDictForParts, data)
        data.close()

        return

    def allDone(self):
        self.statusText += "JSON file has been initialized!\n"
        self.editableTextField.setText(self.statusText)

        self.cancelButton.setText('Finish')

    # define callback functions for button

    def cancelButtonCallback(ev):
        sys.exit()

    def nextButtonCallback(self):
        if self.installationPageNum > 5:

            return

        self.installationPageNum += 1

        if self.installationPageNum == 1:
            self.initialScreen()
        elif self.installationPageNum == 2:
            self.touScreen()
        elif self.installationPageNum == 3:
            self.pathScreen()
        elif self.installationPageNum == 4:
            self.statusScreen()
        elif self.installationPageNum == 5:
            self.allDone()

        return

app = QApplication(sys.argv)

controls = SetupControls()

sys.exit(app.exec_())
