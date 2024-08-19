from picamera2 import Picamera2, Preview
from time import sleep

def capture_image():
    # Initialize the Picamera2 object
    picam2 = Picamera2()
    try:
        # Configure the camera resolution
        config = picam2.create_still_configuration(main={"size": (1024, 768)})
        picam2.configure(config)

        # Start the camera
        picam2.start_preview(Preview.QTGL)

        picam2.start()

        sleep(4)  # Allow the camera to warm up

        # Capture the image to a memory stream
        image_array = picam2.capture_array()
        image = Image.fromarray(image_array)
        datetime.now()
    finally:
      picam2.close()
    return image
capture_image()

