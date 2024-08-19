import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image
import matplotlib.pyplot as plt
from time import sleep
from picamera2 import Picamera2
from gpiozero import AngularServo


# Initialize components once to avoid re-initialization overhead
model_load_path = '/home/teamuser/Documents/Project/CV model/model.pth'
model = models.resnet18(weights=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(model_load_path))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

image_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])

# Initialize Picamera2 once
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1024, 768)})
picam2.configure(config)

# Initialize servos once
servo1 = AngularServo(18, min_pulse_width=0.00075, max_pulse_width=0.00225)
servo2 = AngularServo(17, min_pulse_width=0.00075, max_pulse_width=0.00225)

def predict_image(image):
    image = image_transforms(image)
    image = image.unsqueeze(0)  # Add batch dimension
    image = image.to(device)
    
    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
    
    class_names = ['organic', 'recyclable']
    prediction = class_names[preds.item()]
    return prediction

def capture_image():
    # Start the camera and capture an image
    picam2.start()
    sleep(2)  # Allow the camera to warm up

    # Capture the image to a memory stream
    image_array = picam2.capture_array()
    image = Image.fromarray(image_array)

    picam2.stop()

    return image

def run_servo(prediction):
    if prediction == "organic":
        servo1.angle = 0
        print("servo1.angle = 0")
        sleep(1)
        servo1.angle = -45
        print("servo1.angle = -45")
        sleep(1)
        servo1.angle = 0
        print("servo1.angle = 0")
    else:
        servo1.angle = 0
        servo2.angle = 0
        sleep(1)
        servo1.angle = 45
        sleep(1)
        servo1.angle = -45
        sleep(1)
        servo2.angle = -45
        sleep(1)
        servo2.angle = 0
        sleep(1)
        servo1.angle = 0
        print("servo1.angle = 0")

if __name__ == "__main__":
    picam2.start_preview()  # Start preview once, if needed
    while True:
        captured_image = capture_image()

        plt.imshow(captured_image)
        plt.axis('off')
        plt.show()

        prediction = predict_image(captured_image)
        print(prediction)
        run_servo(prediction)

        # Ask the user if they want to capture another image
        user_input = input("Capture another image? (y/n): ")
    
        if user_input.lower() != 'y':
            break

    picam2.stop_preview()  # Stop preview when done
