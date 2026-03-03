from thea.network.video_stream import VideoController
from thea.network.processing import calculate_average, identify_coordinates

vc = VideoController(identify_coordinates)
vc.start()