import sys
import os
from PySide2.QtWidgets import (QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QFileDialog)
from PySide2.QtCore import QProcess


class Form(QDialog):
    def run_process(self, command):
        process = QProcess()
        process.start(command)
        process.waitForFinished()
        std_output = process.readAllStandardOutput().data().decode('utf-8')
        return std_output

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLabel("BlaBla")
        self.button = QPushButton("Select Directory")
        self.button = QPushButton("Process files")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        filename = QFileDialog.getExistingDirectory(self, "Select folder for processing", "/")
        self.edit.setText(filename)
        for (dirpath, dirnames, filenames) in os.walk(filename):
            for filename in filenames:
                filepath = dirpath + "/" + filename
                command_result = self.run_process("md5sum " + "\"" + filepath + "\"")


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
