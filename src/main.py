"""!
@file main.py
    This file contains the main script for our Term Project.

    The original structure of the code was developed by JR Ridgely, 
    Mechatronics lab instructor.
    
@date   March 10, 2022
    
@author Cade Liberty
@author Juan Luna
@author Marcus Monroe

"""

import gc
import pyb
import utime
import cotask
import task_share
import task_encoder
import task_motor_controller

if __name__ == "__main__":

    # Define encoder pin objects -------------------------------
    
    # ENCODER 1

    ## First pin object for encoder channel.
    ENC1A_pin_1 = pyb.Pin.cpu.C6
    ## Second pin object for encoder channel.
    ENC1B_pin_1 = pyb.Pin.cpu.C7
    ## Timer object for encoder.
    tim_ENC_A_1 = pyb.Timer(8, prescaler = 0, period = 2**16 - 1)
    
    # ENCODER 2

    ## First pin object for encoder channel.
    ENC1A_pin_2 = pyb.Pin.cpu.B6
    ## Second pin object for encoder channel.
    ENC1B_pin_2 = pyb.Pin.cpu.B7
    ## Timer object for encoder.
    tim_ENC_A_2 = pyb.Timer(4, prescaler = 0, period = 2**16 - 1)
    
    # Define motor pin objects ---------------------------------
    
    # First motor

    ## Enable pin object
    ENA_pin_1 = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    ## First control pin of motor
    In1_pin_1 = pyb.Pin.cpu.B4
    ## Second control pin of motor
    In2_pin_1 = pyb.Pin.cpu.B5
    ## Timer object for motor with 20-kHz frequency
    Timer_1   = pyb.Timer(3, freq = 20000)
  
    # second motor

    ## Enable pin object
    ENA_pin_2 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    ## First control pin of motor
    In1_pin_2 = pyb.Pin.cpu.A0
    ## Second control pin of motor
    In2_pin_2 = pyb.Pin.cpu.A1
    ## Timer object for motor with 20-kHz frequency
    Timer_2   = pyb.Timer(5, freq = 20000)

    # Solenoid pin definition
    
    ## Solenoid pin object, set as output pin
    solenoid = pyb.Pin(pyb.Pin.cpu.C4, pyb.Pin.OUT_PP)
    # Start with setting pin low
    solenoid.low()
    
    # Lists containing setpoint coordinates (G code) of the image to be drawn.
    

    with open('x_y_data.csv', 'r') as f:
        ## List to hold data from cvs file
        csv_data = []
        ## Counter variable
        ticker = 0
        ## Counter variable for indices
        num = 0
        ## List of x-coordinate values
        x = []
        ## List of y-coordinate values
        y = []
        for line in f.readlines():
            csv_data.append(line.split(','))
        while ticker < len(csv_data):
            while len(csv_data[ticker]) > 2:
                csv_data[ticker].pop(-1)
            ticker += 1
        while num < len(csv_data):
            try:
                x.append(float(csv_data[num][0]))
                y.append(float(csv_data[num][1]))
            except:
                if len(x) > len(y):
                    x.pop(-1)
                pass
            num += 1

    ## List of theta-1 values  
    theta1 = []
    ## List of theta-2 values
    theta2 = []
    
    # Convert G code to encoder ticks
    for i in range(len(y)):
        theta2.append((y[i]/.0622)*16384+100)
        theta1.append((2*x[i]/(4.852*y[i] + 2.315))*16384/6.28318+100)
    
    # Create shared variables

    ## Encoder share variable for encoder 1
    encoder_share_1   = task_share.Share ('f', thread_protect = False,name = "Encoder_Share_1")
    ## Gain share variable for motor 1
    gain_share_1      = task_share.Share ('f', thread_protect = False, name = "Gain_Share_1")
    ## Setpoint variable for motor 1
    set_point_share_1 = task_share.Share ('f', thread_protect = False, name = "Set _Point _Share_1")
    ## Encoder share variable for encoder 2
    encoder_share_2   = task_share.Share ('f', thread_protect = False, name = "Encoder_Share_2")
    ## Gain share variable for motor 2
    gain_share_2      = task_share.Share ('f', thread_protect = False, name = "Gain_Share_2")
    ## Setpoint variable for motor 2
    set_point_share_2 = task_share.Share ('f', thread_protect = False, name = "Set_Point_Share_2")
    ## Flag signalling that motor 1 has reached its setpoint
    next_flag1 = task_share.Share ('f', thread_protect = False, name = "next_flag1")
    ## Flag signalling that motor 2 has reached its setpoint
    next_flag2 = task_share.Share ('f', thread_protect = False, name = "next_flag2")
    
    # Define task objects

    ## Encoder 1 task object
    task_encoder1 = task_encoder.Task_Encoder(encoder_share_1, ENC1A_pin_1, ENC1B_pin_1, tim_ENC_A_1)
    ## Encoder 2 task object
    task_encoder2 = task_encoder.Task_Encoder(encoder_share_2, ENC1A_pin_2, ENC1B_pin_2, tim_ENC_A_2) 
    ## Motor Controller 1 task object
    task_motor_controller1 = task_motor_controller.Task_Motor_Controller(encoder_share_1, gain_share_1, set_point_share_1, next_flag1, ENA_pin_1, In1_pin_1, In2_pin_1, Timer_1)
    ## Motor Controller 2 task object
    task_motor_controller2 = task_motor_controller.Task_Motor_Controller(encoder_share_2, gain_share_2, set_point_share_2, next_flag2, ENA_pin_2, In1_pin_2, In2_pin_2, Timer_2)    

    ## Encoder 1 task object from cotask module     
    task_enc1 = cotask.Task (task_encoder1.run, name = 'Task_Encoder', priority = 2, 
                        period = 1, profile = True, trace = False)
    ## Encoder 2 task object from cotask module 
    task_enc2 = cotask.Task (task_encoder2.run, name = 'Task_Encoder', priority = 2, 
                        period = 1, profile = True, trace = False)
    ## Motor 1 task object from cotask module 
    task_mot1 = cotask.Task (task_motor_controller1.run, name = 'Task_Controller', priority = 2, 
                        period = 5, profile = True, trace = False)
    ## Motor 2 task object from cotask module 
    task_mot2 = cotask.Task (task_motor_controller2.run, name = 'Task_Controller', priority = 2, 
                        period = 5, profile = True, trace = False)
    
    cotask.task_list.append(task_enc1)
    cotask.task_list.append(task_enc2)
    cotask.task_list.append(task_mot1)
    cotask.task_list.append(task_mot2)

    # Tracking values for debugging

    ## Counter variable
    count = 1

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # State 0, initialization
    gain_share_1.put(.6)
    gain_share_2.put(1.0)
    task_encoder1.zero()
    task_encoder2.zero()
    task_motor_controller1.motor.set_duty_cycle(0)
    task_motor_controller2.motor.set_duty_cycle(0)
    set_point_share_1.put(theta1[0])
    set_point_share_2.put(theta2[0])
    
    while True:
        cotask.task_list.pri_sched()
        
        if next_flag1.get() == 1:
            if next_flag2.get() == 1:
                try:
                    print('Getting to setpoint...')
                    solenoid.high()
                    utime.sleep_ms(250)
                    solenoid.low()
                    set_point_share_1.put(theta1[count])
                    set_point_share_2.put(theta2[count])
                except KeyboardInterrupt:
                    task_motor_controller1.motor.set_duty_cycle(0)
                    task_motor_controller2.motor.set_duty_cycle(0)
                    print('Program terminated...')
                except IndexError:
                    solenoid.low()
                    task_encoder1.zero()
                    task_encoder2.zero()
                    task_motor_controller1.motor.set_duty_cycle(0)
                    task_motor_controller2.motor.set_duty_cycle(0)
                    print('Completed Design')
                    break
                else:
                    #set solenoid value to high
                    #set solenoid value to low
                    
                    print('Else statement')
                finally:
                    print('finally did finally run')
                    count += 1
                    next_flag1.put(0)
                    next_flag2.put(0)