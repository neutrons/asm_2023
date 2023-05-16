import ipywe.fileselector
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
from IPython.display import display

from ipywidgets import interactive
import ipywidgets as widgets



class Exercise1WithWidgets:

    def __init__(self):
        pass

    def input_load_and_visualize_data(self):
        data_folder = ipywe.fileselector.FileSelectorPanel(instruction="Select images",
                                                           filters={'TIFF': ['*.tiff', '*.tif']},
                                                           default_filter='TIFF',
                                                           multiple=True,
                                                           next=self.load_data)
        data_folder.show()

    def load_data(self, list_files):
        self.images = []

        pb = widgets.IntProgress(min=0, max=len(list_files) - 1, description="Loading")
        display(pb)

        for _index, _file in enumerate(list_files):
            _image = np.array(Image.open(_file))
            self.images.append(_image)
            pb.value = _index + 1
            time.sleep(0.15)  # slowing down the load to be able to see the progress bar in action

        pb.description = "Done!"

        self.visualize_data()

    def visualize_data(self):
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax_image = ax.imshow(self.images[0])
        self.cb = plt.colorbar(ax_image, ax=ax)
        plt.show()

        def plot(index):
            self.cb.remove()
            ax_image = ax.imshow(self.images[index])
            self.cb = plt.colorbar(ax_image, ax=ax)
            plt.show()

        v = interactive(plot,
                        index=widgets.IntSlider(min=0,
                                                max=len(self.images) - 1))
        display(v)

