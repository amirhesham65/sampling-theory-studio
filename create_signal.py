import os
import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg
from numpy import sin, cos, pi
import numpy as np
import math

from models.signal import Signal

mainwindow_ui_file_path = os.path.join(os.path.dirname(__file__), 'views', 'create_signal_window.ui')
uiclass, baseclass = pg.Qt.loadUiType(mainwindow_ui_file_path)

# TODO: Change this later
MAX_F_SAMPLING = 500

class CreateSignalWindow(uiclass, baseclass):
    signal_saved = pyqtSignal(Signal)
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Composer - Create Signal")

        self.cosine_frequency = 1
        self.x = [i/100 for i in range(0,math.ceil(1000/(2*self.cosine_frequency)) * 100)]
        self.y = []

        self.cosine_amplitude = 1
        self.cosine_amplitude_unit = 1

        self.cosine_phase = 0;

        # Connecting UI controls to events
        self._initialize_signals_slots()

        self.cosine_amplitude_comboBox.addItem('m')
        self.cosine_amplitude_comboBox.addItem('mm')
        self.cosine_amplitude_comboBox.addItem('µm')


        self.cosine_frequency_slider.setMinimum(1)
        self.cosine_frequency_slider.setMaximum(1000)

        self.cosine_amplitude_slider.setMinimum(1)
        self.cosine_amplitude_slider.setMaximum(1000)

        self.cosine_phase_slider.setMinimum(-180)
        self.cosine_phase_slider.setMaximum(180)

        self.signal_graph.setXRange(0,10)
        self.signal_graph.setYRange(-1,1)
        self._update_plot()


    def _initialize_signals_slots(self):
       self.cosine_frequency_slider.valueChanged.connect(self._on_cosine_freq_slider_change)
       self.cosine_amplitude_slider.valueChanged.connect(self._on_cosine_amp_slider_change)
       self.cosine_phase_slider.valueChanged.connect(self._on_cosine_phase_slider_change)

       self.cosine_amplitude_comboBox.currentTextChanged.connect(self._on_cosine_amp_combobox_change)

       self.save_signal_button.clicked.connect(self.save_signal)
       

  
    def _on_cosine_freq_slider_change(self, value):
        self.cosine_frequency = value
        self.cosine_frequency_value.setText(str(value) + ' Hz')
        self._update_plot()

    def _on_cosine_amp_slider_change(self, value):
        self.cosine_amplitude = value
        self.cosine_amplitude_value.setText(str(value) + ' '+ self.cosine_amplitude_comboBox.currentText())
        self._update_plot()

    def _on_cosine_phase_slider_change(self, value):
        self.cosine_phase = value
        self.cosine_phase_value.setText(str(value) + '°')
        self._update_plot()

    def _on_cosine_amp_combobox_change(self, value):
        if value == 'µm':
            self.cosine_amplitude_unit = 10**(-6)
        elif value == 'mm':
            self.cosine_amplitude_unit = 10**(-3)
        elif value == 'm':
            self.cosine_amplitude_unit = 1
        self.cosine_amplitude_value.setText(str(self.cosine_amplitude) + ' '+ value)  
        self._update_plot()

    def _update_plot(self):
        self._generate_list()
        self.signal_graph.clear()
        self.signal_graph.plot(self.x,self.y)   

    def _generate_list(self):
        self.x = np.linspace(0, math.ceil(1000 / (2 * self.cosine_frequency)), 1000)
        self.y = self.cosine_amplitude * self.cosine_amplitude_unit * cos(self.cosine_frequency *(self.x - self.cosine_phase) * (2*pi))



    def save_signal(self):
        # Create a Signal object from the input data
        t = self.x
        y = self.y
        signal = Signal(t, y)
        
        # Emit the signal_saved signal with the Signal object as the argument
        self.signal_saved.emit(signal)
        
        self.window_closed.emit()
        
def main():
    app = QApplication(sys.argv)
    window = CreateSignalWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
