'''! @file      controller.py
     @brief     A driver implementing proportional closed-loop control.
     @details   Computes the actuation value by multiplying the signal by the
                proportional controller gain, Kp. The error is found by
                calculating the difference between the setpoint (desired) value
                and measured value.
     @author    Cade Liberty
     @author    Juan Luna
     @author    Marcus Monroe
     @date      February 10, 2022
'''

class controller:
    '''! @brief     Driver class implementing proportional control.
        @details    Methods of this class set up attributes and methods
                    responsible for calculating the actuation value to be
                    sent to the motor for closed-loop control.
    '''
    def __init__(self, set_point_share, gain_share):
        '''! @brief  Initializes objects of the EncoderDriver class.
             @param  set_point_share  Share variable for the setpoint value
             @param  gain_share    Share variable for the Kp gain value
        '''
        ## Chosen motor position value
        self.setpoint = set_point_share.get()
        ## Share variable for the Kp gain value
        
        self.gain_share = gain_share
        print('The gain is ', self.gain_share)
    
    def run(self, measured):
        '''! @brief Runs closed loop control calculation
             @param measured  measured position value from encoder
        '''
        ## Difference between the setpoint and measured
        print('the setpoint used is:',self.setpoint)
        self.error = float(self.setpoint) - float(measured)
        ## Proportional gain value 
        self.gain = float(self.gain_share)
        
        return (self.error*self.gain)
    
    def set_point(self, setpoint):        
        '''! @brief  Establishes new reference value
             @param setpoint  reference value selected by user
        '''
        self.setpoint = setpoint
        
    def set_gain(self, gain):
        '''! @brief Establishes new Kp value
             @param gain  Kp value, the proportional gain
        '''
        self.gain = gain