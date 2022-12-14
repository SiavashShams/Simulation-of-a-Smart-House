# Simulation-of-a-Smart-House
About
-----
In this project, we will simulate a smart house equipped with IoT devices to control and monitor the lights, open and close a door, and regulate the home's temperature. A user interface dashboard is created in the ThingsBoard IoT platform in order to simulate the smart house. The data transferring is done via MQTT protocols.

Below is a sample of a designed dashboard in ThingsBoard.
![This is a](/Images/Dashboard.png)


Installation
------------
```sh
pip3 install -r requierments.txt
```
User's guide
------------
Follow the instructions and make your dashboard; then, in the control.py, enter your access token and run the code. You can switch the lights on and off or close and open the door by pressing the corresponding buttons while running the control.py.
Users who want to see the simulations in real-time can visit my public-designed dashboard via the [link](https://demo.thingsboard.io/dashboard/5f822670-0a71-11ec-a86d-6b65d9a2866e?publicId=0cc6e910-0a95-11ec-8e0e-d5779c4f3ddd) and just run the main.exe file. The file is designed to illustrate the data transfer between the server and the IoT dashboard temperature will fluctuate, the door will continue to close and open randomly, and the lights will turn on and off randomly.

Below is the app log after running the main.exe

![This is an image](/Images/App_log.png)



