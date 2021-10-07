# UltrasoundPhasedArray
 Ultrasound phased array for directional transmission: construction, embedded software and python implementation

## General specifications
A low-cost, narrowband ultrasound phased array system for narrowbeam transmission is presented. 

The design features wide bandwidth MEMS loudspeakers (UT-P 2019, USound) with very small dimensions (5 x 7 mm). Dense loudspeaker arrays with small interelement spacing can be constructed, enabling grating lobe free beam patterns at high frequency. The current prototype can support up to 64 MEMS speakers. The amplitude and phase of each loudspeaker stage can be controlled with high resolution, respectively with 10-bit and 12-bit. The array itself is constructed using a 3D printer. 

<p align="center">
  <img src="https://github.com/ChesneyBuyle/UltrasoundPhasedArray/blob/main/Photos/MEMS%20speaker%20array.jpg" width=50% height=50%>
</p>

## System overview

Block diagram of the prototype:

<p align="center">
 <img src="https://raw.githubusercontent.com/ChesneyBuyle/UltrasoundPhasedArray/main/Photos/system_overview_github.png" width=40% height=40%>
</p>

The loudspeaker array is controlled by an external computer. The phase delays and amplitudes of the loudspeaker stages are calculated according to the desired ultrasound beam pattern in Python. Next, these parameters are sent to a controller board, which consists of a NUCLEO-H743ZI2 microcontroller board and custom signal distribution PCB. 
* The microcontroller sends the transducer stage parameters to the corresponding DSP boards. The DSP boards contain the signal generation and amplifier hardware blocks of the loudspeaker stages. 
* The microcontroller uses the signal distribution board to distribute a common clock signal to the DSP boards (for phase coherence) and it ensures communication to the correct hardware blocks. 


## Folder structure
* The *3D prints* folder contains the necessary STL-files to print the array. The loudspeakers should first be placed inside the *holder part (part 1)*. Next, the *cover part (part 2)* can be attached to the back of the array (side with connections on the MEMS loudspeakers) using M2 bolts. This keeps the MEMS loudspeakers in place when soldering the signal wires. Hence, now you should be able to solder the signal wires to the loudspeaker elements. We used very thin 0.25mm coated copper wire, because the loudspeaker connections are very fragile. Finally, we placed a thin layer of acoustic foam on the back of array and kept it into place using the *wire cover part (part 3)*. It also ensures that the signal wires and thus MEMS loudspeakers do not move anymore. 

* The *Python* folder contains the Python scripts for control over the transducer stages (controller.py and main.py). Furthermore, the Python scripts for sampling of the microphone signal (daq.py), stepper motor control (stepper.py) and plotting (plotter.py) are also available. Note that some paths may need to updated before the code runs correctly.

* The *PCB design files* folder contains the schematic and board files of the custom signal distribution and DSP boards (DDS, VGA and power amplifier). These were designed in Eagle. 

* The *Controller board code* contains the embedded code for the NUCLEO-H743ZI2 microcontroller board. 
