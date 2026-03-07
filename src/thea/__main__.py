from thea.sounds import play_morse_pattern
from thea.network.video_stream import VideoController
from thea.utils import identify_coordinates_hsv


play_morse_pattern(".-.-.")

vc = VideoController(identify_coordinates_hsv)
vc.start()
