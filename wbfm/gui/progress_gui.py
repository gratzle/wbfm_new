# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/raw/progress_gui_raw.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import argparse
import os
import sys
from pathlib import Path

from napari import Viewer
from PyQt5 import QtCore, QtWidgets

from wbfm.gui.utils.utils_gui import add_fps_printer
from wbfm.gui.utils.file_dialog_widget import FileDialog
from wbfm.utils.projects.utils_project import safe_cd
from wbfm.utils.projects.utils_project_status import check_all_needed_data_for_step
from wbfm.utils.projects.finished_project_data import ProjectData


class UiMainWindow(object):

    def __init__(self, app=None):
        self.parent_qtapp = app

        # Unclear if this matters
        os.environ["NAPARI_ASYNC"] = "1"

        self.viewer = None

    def setupUi(self, MainWindow, project_path):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(491, 289)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 461, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Top
        self.loadProjectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadProjectButton.setObjectName("loadButton")
        self.loadProjectButton.clicked.connect(self.load_project_file)
        self.verticalLayout.addWidget(self.loadProjectButton)

        self.checkButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.checkButton.setObjectName("checkButton")
        self.checkButton.clicked.connect(self.check_project_status)
        self.verticalLayout.addWidget(self.checkButton)

        # Specific steps
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.segmentationProgress = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.segmentationProgress.setProperty("value", 0)
        self.segmentationProgress.setObjectName("segmentationProgress")
        self.gridLayout.addWidget(self.segmentationProgress, 1, 1, 1, 1)
        self.trainingProgress = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.trainingProgress.setProperty("value", 0)
        self.trainingProgress.setObjectName("trainingProgress")
        self.gridLayout.addWidget(self.trainingProgress, 2, 1, 1, 1)
        self.trackingProgress = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.trackingProgress.setProperty("value", 0)
        self.trackingProgress.setObjectName("trackingProgress")
        self.gridLayout.addWidget(self.trackingProgress, 3, 1, 1, 1)
        self.tracesProgress = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.tracesProgress.setProperty("value", 0)
        self.tracesProgress.setObjectName("tracesProgress")
        self.gridLayout.addWidget(self.tracesProgress, 4, 1, 1, 1)

        # Visualization buttons
        self.segVisButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.segVisButton.setObjectName("pushButton_2")
        self.segVisButton.clicked.connect(self.napari_for_masks)
        self.segVisButton.setToolTip('Visualize segmentation (untracked)')
        self.gridLayout.addWidget(self.segVisButton, 1, 2, 1, 1)
        self.trainingVisButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.trainingVisButton.setObjectName("trainingVisButton")
        self.trainingVisButton.clicked.connect(self.napari_for_masks_training)
        self.trainingVisButton.setToolTip('Visualize training data (segmentation overlaid on raw data)')
        self.gridLayout.addWidget(self.trainingVisButton, 2, 2, 1, 1)
        self.trackingVisButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.trackingVisButton.setObjectName("trackingVisButton")
        self.trackingVisButton.clicked.connect(self.napari_for_masks_tracking)
        self.trackingVisButton.setToolTip('Visualize tracked data (segmentation overlaid on raw data)')
        self.gridLayout.addWidget(self.trackingVisButton, 3, 2, 1, 1)
        self.tracesVisButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.tracesVisButton.setObjectName("pushButton_5")
        self.tracesVisButton.clicked.connect(self.open_traces_gui)
        self.tracesVisButton.setToolTip('For more info, see trace_explorer.py')
        self.gridLayout.addWidget(self.tracesVisButton, 4, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 491, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Load project path
        self.is_loaded = False
        self.project_dir = None
        self.project_file = project_path

        # Deactivate not working buttons
        self.trainingVisButton.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadProjectButton.setText(_translate("MainWindow", "Load Project"))
        self.checkButton.setText(_translate("MainWindow", "Update Project Status"))

        self.label_5.setText(_translate("MainWindow", "1. Segmentation"))
        self.label_6.setText(_translate("MainWindow", "2. Training data"))
        self.label_7.setText(_translate("MainWindow", "3. Tracking"))
        self.label_8.setText(_translate("MainWindow", "4. Traces"))

        self.label_3.setText(_translate("MainWindow", "Visualize"))
        self.label.setText(_translate("MainWindow", "Step"))
        self.label_2.setText(_translate("MainWindow", "Status"))

        self.segVisButton.setText(_translate("MainWindow", "SegmentationVis"))
        self.trainingVisButton.setText(_translate("MainWindow", "TrainingVis"))
        self.trackingVisButton.setText(_translate("MainWindow", "IntermediateTrackingVis"))
        self.tracesVisButton.setText(_translate("MainWindow", "FullTrackingVis"))

    def load_project_file(self):
        ex = FileDialog()
        self.project_file = ex.fileName

    @property
    def project_file(self):
        return self._project_file

    @project_file.setter
    def project_file(self, value):
        if value is None:
            return

        self.is_loaded = True
        self._project_file = value
        print(f"Loading project: {self.project_file}")
        self.project_dir = Path(value).parent
        with safe_cd(self.project_dir):
            self._load_config_files(value)
        self.check_project_status()


    def check_project_status(self):
        seg_status = check_all_needed_data_for_step(self.cfg, 1, raise_error=False)
        if seg_status:
            self.segmentationProgress.setValue(100)
        else:
            self.segmentationProgress.setValue(0)
        training_status = check_all_needed_data_for_step(self.cfg, 2,
                                                         training_data_required=False, raise_error=False)
        if training_status:
            self.trainingProgress.setValue(100)
        else:
            self.trainingProgress.setValue(0)
        tracking_status = check_all_needed_data_for_step(self.cfg, 3, raise_error=False)
        if tracking_status:
            self.trackingProgress.setValue(100)
        else:
            self.trackingProgress.setValue(0)
        traces_status = check_all_needed_data_for_step(self.cfg, 4, raise_error=False)
        if traces_status:
            self.tracesProgress.setValue(100)
        else:
            self.tracesProgress.setValue(0)

    def _load_config_files(self, project_path):
        self.project_data = ProjectData.load_final_project_data(project_path)
        self.cfg = self.project_data.project_config

    def napari_for_masks(self):
        """Open napari window for segmentation before tracking"""
        # self.viewer = Viewer(ndisplay=3)
        which_layers = ['Red data', 'Green data', 'Raw segmentation']
        self.viewer = self.project_data.add_layers_to_viewer(self.viewer, which_layers=which_layers)
        self.viewer.show()
        add_fps_printer(self.viewer)

    def napari_for_masks_tracking(self):
        """Open napari window for segmentation colored by tracking"""
        self.viewer = Viewer(ndisplay=3)
        which_layers = ['Red data', 'Green data', 'Raw segmentation', 'Intermediate global IDs']
        self.project_data.add_layers_to_viewer(self.viewer, which_layers=which_layers)
        self.viewer.show()

    def napari_for_masks_training(self):
        """Open napari window for segmentation and raw data"""
        self.viewer = Viewer(ndisplay=3)
        which_layers = ['Red data', 'Green data', 'Raw segmentation']
        self.project_data.add_layers_to_viewer(self.viewer, which_layers=which_layers)
        self.viewer.show()

    def open_traces_gui(self):
        self.viewer = Viewer(ndisplay=3)
        which_layers = ['Red data', 'Green data', 'Raw segmentation', 'Colored segmentation',
                        'Neuron IDs', 'Intermediate global IDs']
        self.project_data.add_layers_to_viewer(self.viewer, which_layers=which_layers)
        self.viewer.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build GUI with a project')
    parser.add_argument('--project_path', '-p', default=None,
                        help='path to config file')
    parser.add_argument('--DEBUG', default=False,
                        help='')
    args = parser.parse_args()

    # Basic setup
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(app)
    # Get project settings
    project_path = args.project_path
    # Actually build window
    ui.setupUi(MainWindow, project_path)
    MainWindow.show()
    sys.exit(app.exec_())
