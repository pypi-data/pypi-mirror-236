import napari
import napari.layers
from napari.qt import thread_worker
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from qtpy.QtWidgets import (
    QSpinBox,
    QWidget, 
    QComboBox, 
    QSizePolicy, 
    QLabel, 
    QGridLayout, 
)
import cv2
import numpy as np
import matplotlib as mpl

mpl.rc("axes", edgecolor="white")
mpl.rc("axes", facecolor="#262930")
mpl.rc("axes", labelcolor="white")
mpl.rc("savefig", facecolor="#262930")
mpl.rc("text", color="white")
mpl.rc("xtick", color="white")
mpl.rc("ytick", color="white")

class HistogramWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer

        self.video_layer = None
        self.busy = False  # Are we busy rendering the figure?
        
        # Layout
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignTop)
        self.setLayout(grid_layout)

        # Image
        self.cb_image = QComboBox()
        self.cb_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cb_image.currentTextChanged.connect(self._connect_video_layer)
        grid_layout.addWidget(QLabel("Image", self), 0, 0)
        grid_layout.addWidget(self.cb_image, 0, 1)

        # Bins selector
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setMinimum(10)
        self.bins_spinbox.setMaximum(100)
        self.bins_spinbox.setSingleStep(5)
        self.bins_spinbox.setValue(50)
        self.bins_spinbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.bins_spinbox.valueChanged.connect(self.drawing_handler)
        grid_layout.addWidget(QLabel("Bins", self), 1, 0)
        grid_layout.addWidget(self.bins_spinbox, 1, 1)

        # Histogram plot
        self.canvas = FigureCanvas()
        self.canvas.figure.set_tight_layout(True)
        self.canvas.figure.patch.set_facecolor("#262930")
        self.axes = self.canvas.figure.subplots()
        self.axes.cla()
        self.axes.set_xlabel('Gray level')
        self.axes.set_ylabel('Frequency')
        self.axes.set_xlim(0, 1)
        self.axes.set_yticks([])
        self.canvas.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.canvas.setMinimumSize(300, 300)
        grid_layout.addWidget(self.canvas, 2, 0, 1, 2)

        self.threaded_draw = thread_worker(self.draw, connect={'returned': self._set_busy_false})

        # Setup layer callbacks
        self.viewer.layers.events.inserted.connect(
            lambda e: e.value.events.name.connect(self._on_layer_change)
        )
        self.viewer.layers.events.inserted.connect(self._on_layer_change)
        self.viewer.layers.events.removed.connect(self._on_layer_change)
        self._on_layer_change(None)
        
    def _on_layer_change(self, e):
        self.cb_image.clear()
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image) & (x.rgb is False):
                self.cb_image.addItem(x.name, x.data)

    @property
    def bins(self):
        return self.bins_spinbox.value()

    def _connect_video_layer(self, e):
        if e == '':
            return
        try:
            self.video_layer = self.viewer.layers[e]
        except KeyError:
            print(f'{e} not in layers.')
            return
        
        for x in self.viewer.layers:
            if isinstance(x, napari.layers.Image):
                x.events.set_data.disconnect(self.drawing_handler)
        
        self.video_layer.events.set_data.connect(self.drawing_handler)

        self.drawing_handler()

    def drawing_handler(self):
        if (not self.busy) & (self.video_layer is not None):
            self.threaded_draw()

    def _set_busy_false(self):
        self.busy = False    

    def draw(self):
        self.busy = True
        frame = self.video_layer.data
        ndim = self.video_layer.ndim
        frame_max = np.max(frame)
        self.axes.cla()
        self.axes.set_xlabel('Gray level')
        self.axes.set_ylabel('Frequency')
        self.axes.set_yticks([])
        histogram = cv2.calcHist([frame], [0], None, [self.bins], [0, frame_max]) / np.prod(frame.shape[:ndim])
        histogram = np.squeeze(histogram)
        try:
            self.axes.fill_between(
                np.linspace(0, frame_max, self.bins), 
                histogram, 
                interpolate=False, 
                color='#a6b5d4'
            )
        except ValueError:
            print('Caught value error.')
        try:
            self.canvas.draw()
        except IndexError:
            print('Caught index error.')