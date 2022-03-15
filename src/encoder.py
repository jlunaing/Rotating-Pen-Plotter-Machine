'''!    @file       encoder.py
        @brief      A driver for working with a quadrature incremental encoder.
        @details    Encapsulates functionality of encoder attached to the motor.
                    This class sets up pins to control the encoder and methods
                    to read and zero (reset) the angular position of the motor
                    in units of "ticks". Position reading is based on an 
                    algorithm that accounts for overflow and underflow.
 
        @author     Cade Liberty
        @author     Juan Luna
        @author     Marcus Monroe
        @date       March 10, 2022
'''

import pyb

class EncoderDriver:
    '''! @brief      Driver class for the quadrature incremental encoder.
         @details    Objects of this class can be used to instantiate encoder
                     objects to control two encoders, each attach to one motor.
    '''
    def __init__ (self, enc1_pin, enc2_pin, timer):
        '''! @brief      Initializes objects of the EncoderDriver class.
             @param  enc1_pin    Encoder pin object for first timer channel.
             @param  enc2_pin    Encoder pin object for second timer channel.
             @param  timer       Timer object for program timing.  
        '''     
        ## Encoder pin object for first timer channel.
        self.enc1_pin = enc1_pin
        ## Encoder pin object for second timer channel.
        self.enc2_pin = enc2_pin

        ## Timer object for program timing. 
        self.timer = timer

        # Encoder timer channel setup

        ## Channel object "1" for motor timer.
        self.tim_ch1 = timer.channel(1, mode = pyb.Timer.ENC_AB, pin = self.enc1_pin)
        ## Channel object "2" for motor timer.
        self.tim_ch2 = timer.channel(2, mode = pyb.Timer.ENC_AB, pin = self.enc2_pin)

        ## Timer period, defined as largets 16-bit number
        self.period     = 2**16 - 1

        #  Variables to be used in EncoderDriver class methods

        ## Difference between consecutive tick counts
        self.delta_val = 0
        ## Previous recorded encoder tick value
        self.last_tick = 0
        ## Latest recorded encoder tick value
        self.new_tick = 0
        ## Encoder position that accounts for overflow/underflow
        self.true_position = 0
        
    def read(self):
        '''! @brief      Reads current position of encoder.
             @details    Algorithm accounting for overflow and underflow is
                         implemented to return current encoder position.
        '''
        # Save last encoder reading
        self.last_tick = self.new_tick
        # Take a new encoder reading
        self.new_tick = self.timer.counter()
        # Calculate difference between last two readings
        self.delta_val = self.new_tick - self.last_tick
        
        # Accounting for overflow or underflow
        if (self.delta_val > 0.5*self.period):
            self.delta_val -= self.period

        elif (self.delta_val < -0.5*self.period):
            self.delta_val += self.period
          
        #self.rev_per_s = self.delta_var/(16384)

        self.true_position += self.delta_val
        return self.true_position

    def zero(self):
        '''! @brief      Resets (zeroes) the position of the encoder.
        '''
        self.true_position = 0
