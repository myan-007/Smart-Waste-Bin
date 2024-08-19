% Component Required
- Raspberry Pi 5 : Acts as the brain of the system, processing inputs from the sensors and controlling the mechanical actions of the system.
- Raspberry Pi Camera Module 2: Captures images of waste for classification using computer vision algorithms.
- Servo Motors (2x SG90): Used to control sorting mechanisms that direct waste into the appropriate bins.
- Ultrasonic Distance Sensor (HC-SR04): Detects the presence of objects and helps determine when waste is present to trigger sorting.
- Inductive Proximity Sensor (LJ12A3-4-Z/BX): Identifies metallic objects by detecting changes in inductance.
- Additional components: Jumper wires, breadboard, power supply, etc.

% Describe the software environment, including libraries and custom algorithms.
  Software Components
- Raspberry Pi OS: The operating system running on the Raspberry Pi.
- OpenCV Library: Used for image processing and object classification.
- Custom Python Scripts: Handle the logic of the system, sensor data acquisition, classification, and motor control.

% Install the Library
- Check the requirement.txt file add all those Libraries to virtual environment
- Run the individual file from the Code Folder for testing the each sensor individually
- Then run Usage.py under CV model folder hollistic model
