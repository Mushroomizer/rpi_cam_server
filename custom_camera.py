from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from streaming_server import StreamingOutput


class Cam:
    def __init__(self) -> None:
        self.tuning = Picamera2.load_tuning_file("camera_noir.json","./config")
        self.tuning["rpi.agc"]["exposure_modes"]["normal"] = {"shutter": [100, 66666], "gain": [1.0, 8.0]}
        self.picam2 = Picamera2(tuning=self.tuning)
        self.picam2.configure(self.picam2.create_video_configuration(main={"size": (640, 480)}))
    
    def jpeg_streaming_output(self) -> StreamingOutput:
        output = StreamingOutput()
        self.picam2.start_recording(JpegEncoder(), FileOutput(output))
        return output

    def __del__(self):
        self.picam2.stop_recording()

