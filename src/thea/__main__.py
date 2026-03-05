from thea.network.video_stream import VideoController
from thea.processing.utils import identify_coordinates_hsv

vc = VideoController(identify_coordinates_hsv)
vc.start()