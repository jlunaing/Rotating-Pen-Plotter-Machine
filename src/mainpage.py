'''!
@file       mainpage.py
@brief      Term Project Progress Check-in   
@date       February 24, 2022

@mainpage

This is an overview of the software and hardware design for the term project
of the Mechatronics course at Cal Poly.

@section    software     Software Design
                    
Our automatic pin-glass pen drawer device will have two motors and a solenoid
facilitating the motion of the pen/marker needed to draw a picture on the 
surface of the pint glass. This will be captured in the form of five tasks.
There will be two motor controller tasks for each of the two motors. Each 
of these tasks received the position of the motor from their respective encoders.
Each encoder will have an associated task.

One of the controller tasks will communicate with a "solenoid" task that controls
the extension/contraction motion of the solenoid. 

In addition, a user task will be implemented to initiate the program and 
send image data in the form of coordinates to the controller task. As expected 
from this, the image to be drawed is first pre-processed to get actual 
numerical information. This data will be saved in an array and sent to the 
controller task in x-y pairs.

The task diagram for the overall project is shown below. It is worth noting that 
while "x" is used to represent one of the axis, it can also be thought of as a 
"theta" axis, due to the rotating base creating the motion.

\htmlonly <style> div.image img[src = "term_proj_task_diagram.png"]{width:700px}
                </style>
    \endhtmlonly
    
    \image  html    term_proj_task_diagram.png "Term Project Task Diagram"


@subsection sec_fsm     State-Transition Diagram

@subsubsection sec_usr  User Task

The user task is responsible for starting the program. The task sends 
pre-processed image data in the form of coordinates to the motor controller
task for appropriate closed-loop control action to accomplish the goal of 
the project.

\htmlonly <style> div.image img[src = "user_task_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    user_task_fsm.png "User Task State-Transition Diagram"

@subsubsection sec_enc  Encoder Task

The encoder task is responsible for getting the encoder readings to be sent
to the controller task. The encoder reading is the angular position of the motor.
The will be two objects representing each encoders.

\htmlonly <style> div.image img[src = "encoder_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    encoder_fsm.png "Encoder State-Transition Diagram"

@subsubsection sec_mot_ctrl  Motor-Controller Task

The motor controller task is responsible for setting the duty cycle needed 
for the motor to get to the appropriate position on the surface of the pint
glass. The will be two objects representing each motors. One of the controllers
will be responsible for sharing data with the solenoid task so that motion of
the pen/marker is accomplished.

\htmlonly <style> div.image img[src = "motor_controller_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    motor_controller_fsm.png "Motor-Controller State-Transition Diagram"

@subsubsection sec_sol Solenoid Task

The solenoid task is responsible for actuating the extension/contraction 
motion of the solenoid. 

\htmlonly <style> div.image img[src = "solenoid_fsm.png"]{width:500px}
                </style>
    \endhtmlonly
    
    \image  html    solenoid_fsm.png "Solenoid State-Transition Diagram"

@section    hardware     Hardware Design

The basic hardware setup of our automatic pint-glass pen drawer has a rotating
base that is made from a pottery turntable. This will have a 28-tooth, 5-in 
pitch diameter (approximately) gear attached on top and meshed with a gear of
similar properties. The meshing gear is rotated by one of the motors. This 
motor is attached to a 3D-printed support base that holds the entire y-axis
assembly.

Structurally, the y-axis is comprised of the mentioned 3D-printed support base
and a support structure made out of wood and mounted atop of the 3D-printed based.
The wooden support has lead screw which is attached to the second motor. 
The lead screw has a 3D-printed support that holds the marker and the solenoid 
that actuates the in/out motion of the marker. The marker (labeled as pen in
the drawing) is held perpendicular to the lead screw. The y-axis support base
will likely include a feature that allows us to manually set the angle of the
y-axis with respect to a vertical reference axis. 

Finally, the pint glass on which we will draw the picture will be held in place
by glue or some other similar method.

A visual representation of the physical setup is shown below.

\htmlonly <style> div.image img[src = "assembly.png"]{width:800px}
                </style>
    \endhtmlonly
    
    \image  html    assembly.png "CAD model of the project"

'''