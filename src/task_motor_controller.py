'''!    @file    task_motor_controller.py
        @brief   Runs the motor and controller tasks together.  
        @details Implements closed-loop position control on a motor
                 using a task defined as a generator.
        @author  Cade Liberty
        @author  Juan Luna
        @author  Marcus Monroe
        @date    March 10, 2022
'''
import controller
import motor

class Task_Motor_Controller:
    '''! @brief     Task motor controller class.
    '''
    def __init__(self, encoder_share, gain_share, set_point_share, next_flag, ENA_pin, In1_pin, In2_pin, Timer):
        '''! @brief    Instantiates objects of the Task_Motor_Controller class.
             @param  encoder_share  Passes the present value from the encoder
             @param  gain_share    Share variable for proportional gain value.
             @param  set_point_share   Share variable for setpoint value.
             @param  next_flag  Share variable to indicate that the motor has reached its setpoint.
             @param  ENA_pin            Enable pin object for the motor.
             @param  In1_pin       Control pin 1 associated with motor.
             @param  In2_pin       Control pin 2 associated with motor.
             @param  Timer          Timer object for motor.
        '''
        # Define shares for motor and encoder 1

        ## Passes the present value from the encoder
        self.encoder_share = encoder_share
        ## Share variable for proportional gain value.
        self.gain_share = gain_share
        ## Share variable for setpoint value.
        self.set_point_share = set_point_share
        ## Share variable to say when the motor has reached its setpoint
        self.next_flag = next_flag
        
        # Define motor-related pin objects

        ## Enable pin object for the motor.
        self.ENA = ENA_pin
        ## Control pin 1 associated with motor.
        self.IN1A_pin = In1_pin
        ## Control pin 2 associated with motor.
        self.IN2A_pin = In2_pin
        ## Timer object for motor.
        self.tim_MOT_A = Timer
        
        ## Motor object
        self.motor = motor.MotorDriver(self.ENA, self.IN1A_pin, self.IN2A_pin, self.tim_MOT_A)
        
    def run(self):
         '''! @brief Runs the controller task and sets new duty cycle 
         '''
         ## Controller object
         self.controller = controller.controller(self.set_point_share, self.gain_share.get())
         while True:
             
             print(self.set_point_share.get())    
             
             ## Encoder position reading
             true_position = int(self.encoder_share.get())
             print('Encoder value: ', true_position)
             ## Difference between measured and setpoint values 
             self.controller.set_point(self.set_point_share.get())
             self.calc_error = self.controller.run(true_position)
             self.motor.set_duty_cycle(float(self.calc_error))
             
             if  self.set_point_share.get() - self.set_point_share.get()*.05 <= true_position <= self.set_point_share.get() + self.set_point_share.get()*.05:
                 self.next_flag.put(1)
                 self.motor.set_duty_cycle(0)
             yield (0)
             
             