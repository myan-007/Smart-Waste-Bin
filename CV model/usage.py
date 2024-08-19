import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image
import matplotlib.pyplot as plt
from time import sleep,time
from picamera2 import Picamera2
from gpiozero import AngularServo,DistanceSensor
from gpiozero import DigitalInputDevice
from datetime import datetime
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

def log_message(message):
    log_path = os.path.join(script_dir, "shutdown_log.txt")
    with open(log_path, "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

# Function to monitor system health
def monitor_system():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = float(temp.replace("temp=", "").replace("'C\n", ""))

    voltage = os.popen("vcgencmd measure_volts").readline()
    voltage = float(voltage.replace("volt=", "").replace("V\n", ""))

    throttled = os.popen("vcgencmd get_throttled").readline().strip()

    if temp > 80:  # Adjust threshold as needed
        log_message(f"High temperature warning: {temp}�C")

    if voltage < 4.8:  # Voltage drop threshold
        log_message(f"Low voltage warning: {voltage}V")

    if "0x50000" in throttled:
        log_message(f"Throttling detected: {throttled}")

 

model_load_path = '/home/teamuser/Documents/Project/CV model/model.pth'
model = models.resnet18(weights=True)
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
    # Initialize the Picamera2 object
    picam2 = Picamera2()

    try:
        # Configure the camera resolution
        config = picam2.create_still_configuration(main={"size": (1024, 768)})
        picam2.configure(config)

        # Start the camera
        picam2.start()
        sleep(2)  # Allow the camera to warm up

        # Capture the image to a memory stream
        image_array = picam2.capture_array()
        image = Image.fromarray(image_array)
        datetime.now()
    finally:
        # Ensure the camera is stopped
        picam2.stop()
        picam2.close()

    return image

 
def runServo(perdiction):
    servo2=None
    servo1 = AngularServo(17,min_pulse_width=0.00075, max_pulse_width=0.00225)
    sleep(2)
    servo1.angle = 0
    sleep(2)
    if(perdiction != "organic"):
     servo2 = AngularServo(18,min_pulse_width=0.00075, max_pulse_width=0.00225)
     sleep(2)
     servo2.angle = -10
     
     sleep(2)
    
    print("servos Initialized")

    while(True):
        if(perdiction == "organic"):
            sleep(3)
            servo1.angle = -35
            sleep(3)
            servo1.angle = -0
            sleep(3)
            servo1.detach()
            
        else:
            ind_sensor = DigitalInputDevice(27)
            print("Inductive Sensor Initialized")
            print(ind_sensor)
        
            servo1.angle = 15
            sleep(2)
            servo1.angle = 35
            sleep(2)
            servo1.angle = 0
            sleep(1)
            
            startTime = time()
            
            flag = 0
            while time() - startTime <= 5:
                if ind_sensor.value == 0:
                    print("Metal Detected")
                    servo2.angle = 35
                    sleep(3)
                    flag = 1
                    break
            if flag == 0:        
                servo2.angle = -35
                sleep(3)
            servo2.angle = -0
            sleep(3)
            
            servo1.detach()
            servo2.detach()
            print("Servos Detached")
            print("Ready to use again")
    break
 
if __name__ == "__main__":
    while True:

        monitor_system()
        distance_threshold = 35
        prox_sensor = DistanceSensor(echo=23,trigger=24)
        while(True):
            distance = prox_sensor.distance *100
            
            if distance < distance_threshold:
                prox_sensor.close()
                break
        captured_image = capture_image()
        print("camera captured")
        plt.imshow(captured_image)
        plt.axis('off')
        # plt.show()
        prediction = predict_image(captured_image)
        print("CV model : ",prediction)
        runServo(prediction)
        # Ask the user if they want to capture another image
        # user_input = input("Capture another image? (y/n): ")
        # if user_input.lower() != 'y':
        #     break

 



