from thea.network.video_stream import VideoController
from thea.processing.color.tuning import tune
from thea.utils import identify_coordinates_hsv


vc = VideoController(identify_coordinates_hsv)
vc.start()
