from abc import ABCMeta, abstractmethod
import random as rand

#================================================================================
# PRIMARY USERS
#================================================================================

class PrimaryUser:
    __metaclass__ = ABCMeta
    
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.is_active = False
        
    @abstractmethod
    def update(self, tm):
        pass
        
    def write(self, channels):
        if self.is_active:
            channels[self.channel_id] += 1
            
class PeriodicUser(PrimaryUser):
    
    def __init__(self, channel_id, period, active_tm):
        super(PeriodicUser, self).__init__(channel_id)
        self.PERIOD = period
        self.ACTIVE_TM = active_tm
        self.START_TIME = rand.randint(0, period-1)
        
    def update(self, tm):
        self.is_active = (tm - self.START_TIME) % self.PERIOD < self.ACTIVE_TM
        
class RandomUser(PrimaryUser):
    
    def __init__(self, channel_id, active_prob):
        super(RandomUser, self).__init__(channel_id)
        self.ACTIVE_PROB = active_prob
        
    def update(self, tm):
        self.is_active = rand.random() < self.ACTIVE_PROB
        
#================================================================================
# SECONDARY USERS
#================================================================================

class SecondaryUser:
    
    def __init__(self):
        self.curr_channel_id = 0
        pass
    
    def update(self, curr_tm, channels):
        self.can_write = channels[self.curr_channel_id] == 0
    
    def write(self, channels):
        
        if self.can_write:
            # write to the channel
            channels[self.curr_channel_id] += 3