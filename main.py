import sys
import os
from PySide2.QtWidgets import (QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QFileDialog, QMessageBox)
from PySide2.QtCore import QProcess, QThread, SIGNAL


def get_md5(command):
    process = QProcess()
    process.start(command)
    process.waitForFinished()
    std_output = process.readAllStandardOutput().data().decode('utf-8')
    return std_output


class MD5sumThread(QThread):
    def __init__(self, folder_path):
        super().__init__()
        self.dir_path = folder_path

    def run(self):
        self.get_md5_all_files()

    def get_md5_all_files(self):
        for (dir_path, dir_names, filenames) in os.walk(self.dir_path):
            for filename in filenames:
                filepath = dir_path + "/" + filename
                command_result = get_md5("md5sum " + "\"" + filepath + "\"")
                print(command_result)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.dir_path = ""
        self.get_thread = MD5sumThread("")

        self.label_dir = QLabel("Select a directory")
        self.button_select_dir = QPushButton("Select Directory")
        self.button_process_files = QPushButton("Process Files")
        self.button_cancel_process = QPushButton("Cancel Processing")

        self.define_layout()
        self.connect_listeners()

        self.set_widgets_select_dir()

    def define_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_dir)
        layout.addWidget(self.button_select_dir)
        layout.addWidget(self.button_process_files)
        layout.addWidget(self.button_cancel_process)
        self.setLayout(layout)

    def connect_listeners(self):
        self.button_select_dir.clicked.connect(self.show_select_folder_dialog)
        self.button_process_files.clicked.connect(self.process_files)
        self.button_cancel_process.clicked.connect(self.cancel_processing)

    def show_select_folder_dialog(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select folder for processing", "/")

        if os.path.exists(selected_dir):
            self.dir_path = selected_dir
            self.label_dir.setText(self.dir_path)
            self.set_widgets_start_processing()

    def set_widgets_select_dir(self):
        self.button_select_dir.setEnabled(True)
        self.button_process_files.setEnabled(False)
        self.button_cancel_process.setEnabled(False)

    def set_widgets_start_processing(self):
        self.button_select_dir.setEnabled(True)
        self.button_process_files.setEnabled(True)
        self.button_cancel_process.setEnabled(False)

    def set_widgets_processing(self):
        self.button_select_dir.setEnabled(False)
        self.button_process_files.setEnabled(False)
        self.button_cancel_process.setEnabled(True)

    def process_files(self):
        if os.path.exists(self.dir_path):
            self.set_widgets_processing()

            self.get_thread = MD5sumThread(self.dir_path)
            self.connect(self.get_thread, SIGNAL("finished()"), self.processing_done)
            self.get_thread.start()
        else:
            QMessageBox.critical(self, "No directory selected",
                                 "Please select a valid directory",
                                 QMessageBox.Ok)

    def cancel_processing(self):
        self.set_widgets_start_processing()

        if self.get_thread.isRunning():
            self.get_thread.terminate()
            self.get_thread.wait()

    def processing_done(self):
        self.set_widgets_start_processing()
        QMessageBox.information(self, "Done!", "Done processing files!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
