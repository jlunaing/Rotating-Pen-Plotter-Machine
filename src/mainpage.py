'''!
@file       mainpage.py
@brief      Term Project Progress Check-in   

@mainpage

This is an overview of the software design of the term project for the
Mechatronics course at California Polytechnic State University.

The student self-funded project consists of a two and one-half axis machine that draws
a image on the surface of a pint glass. One axis is a rotating base, a second 
axis a vertical up/down motion, and the third, half axis is the in/out motion 
of the marker/pen that plots the image.

@section    software     Software Design
                    
Four tasks allow our system, called "pen plotter" for brevity, to achieve its
desired functionality. Two of these tasks are provided by the instructor and 
accomplish cooperative multitasking and data sharing. The other two, are an
encoder tasks to read the position of the motor and a motor-controller task that sets
the motor percent duty cycle that corresponds to the setpoint or desired value
of position. Because there are two motors for each full axis, there are two
motor controller tasks, each with an associated encoder task. Thus, a total of 
six tasks. However, excluding the ones related to cooperative multitasking and
data sharing for purposes of defining a task diagram, we have four tasks in total.

The task diagram for the overall project is shown below. It is worth noting that 
while "x" is used to represent one of the axis, it can also be thought of as a 
"theta" axis, due to the rotating base creating the motion.

\htmlonly <style> div.image img[src = "term_proj_task_diagram.png"]{width:700px}
                </style>
    \endhtmlonly
    
    \image  html    term_proj_task_diagram.png "Term Project Task Diagram"

For simplicity, there is no user task. The main script for the program is
responsible for providing the controller with the image data. The position
coordinates of the image were acquired in a pre-processing step. This involved
generating an image using the Inkspace software and exporting the results in 
HPGL format. The file was changed to a CSV file and our main file was responsible
for extracting x and y coordinates from this file.

@subsection sec_fsm     State-Transition Diagrams

@subsubsection sec_enc  Encoder Task

The encoder task is responsible for getting the encoder readings to be sent
to the controller task. This is accomplished by writing the encoder value into 
a share variable accessible to all pertaining tasks. 

The encoder reading represents the angular position of the motor.
The are two objects representing the encoders.

\htmlonly <style> div.image img[src = "encoder_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    encoder_fsm.png "Encoder State-Transition Diagram"

@subsubsection sec_mot_ctrl  Motor-Controller Task

The motor controller task is responsible for setting the duty cycle needed 
for the motor to get to the appropriate position on the surface of the pint
glass. The will be two objects representing each motor.

The percent duty cycle is the actuation value sent from the controller. The 
controller calculates the actuation signal from the error value, computed from
the desired value (setpoint) and the measured value (encoder reading). The setpoint
is accessible in the motor-controller task as a shared variable. 

The motor controller updates every time the measured value is within 5% of 
the setpoint. This allowed some tolerance needed due to the limited resolution
of the encoders.

\htmlonly <style> div.image img[src = "motor_controller_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    motor_controller_fsm.png "Motor-Controller State-Transition Diagram"

In addition, we have the in/out motion of the solenoid. After every setpoint 
was reached, the solenoid object was set low (active-low configuration) and a 
dot was "plotted" on the surface of the glass. This is not included in the controller
state-transition diagram because this is handled on the main file.

@date       Created: February 24, 2022
@date       Modified: March 15, 2022
@author     Juan D. Luna

'''