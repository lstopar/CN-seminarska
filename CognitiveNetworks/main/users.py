from abc import ABCMeta, abstractmethod
import random as rand
import numpy as np

#================================================================================
# PRIMARY USERS
#================================================================================

class PrimaryUser:
    __metaclass__ = ABCMeta
    
    def __init__(self, time_unit, channel_id):
        self.TIME_UNIT = time_unit
        self.channel_id = channel_id
        self.is_active = False
        
    @abstractmethod
    def update(self, tm):
        pass
        
    def write(self, channels):
        if self.is_active:
            channels[self.channel_id] += 1
            
class PeriodicUser(PrimaryUser):
    
    def __init__(self, time_unit, channel_id, active_tm, inactive_tm):
        super(PeriodicUser, self).__init__(time_unit, channel_id)
        self.ACTIVE_TM = active_tm
        self.INACTIVE_TM = inactive_tm
        self.START_TIME = rand.randint(0, inactive_tm*time_unit)
        
    def update(self, tm):
        self.is_active = (tm - self.START_TIME) % (self.ACTIVE_TM + self.INACTIVE_TM) < self.INACTIVE_TM
        
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
    
    STATE_PRIM_INACTIVE = 0
    STATE_PRIM_ACTIVE = 1
    
    def __init__(self, time_unit):
        self.TIME_UNIT = time_unit
        self.curr_channel_id = 0
        self.jump_counts = [0, 0]
        # it doesn't matter what we initialize the transition rate matrix to
        # the only problematic intensity is zero
        self.Q = np.array([[-1.0,1.0],[1.0,-1.0]])
        # helper variables
        self.last_update_tm = None
        self.last_change_tm = None
        
    
    def update(self, curr_tm, channels):
        can_write = channels[self.curr_channel_id] == 0
        
        #  check if we can update the model
        if self.last_update_tm is not None and \
                can_write != self.can_write:
            if can_write:
                # the primary user just went from being inactive to being active
                # when the primary user is inactive we only sample the channel
                # every once in a while. This means that we know exactly when the
                # primary user became inactive (since we always sample before we 
                # send), but the time they became active is sometime between our
                # previous sampling and now. To minimize the error set the end 
                # time to the average of the two.
                end_time = float(curr_tm + self.last_update_tm) / 2
                if self.last_change_tm is not None:
                    duration = (end_time - self.last_change_tm) / self.TIME_UNIT
                    self._update_intensity(SecondaryUser.STATE_PRIM_INACTIVE, SecondaryUser.STATE_PRIM_ACTIVE, duration)
                
                self.last_change_tm = end_time
            elif self.last_change_tm is not None:  # check if we are initialized
                duration = (curr_tm - self.last_change_tm) / self.TIME_UNIT
                self._update_intensity(SecondaryUser.STATE_PRIM_ACTIVE, SecondaryUser.STATE_PRIM_INACTIVE, duration)            
                self.last_change_tm = curr_tm
        
        self.can_write = can_write
        self.last_update_tm = curr_tm
    
    def write(self, channels):
        if self.can_write:
            # write to the channel
            channels[self.curr_channel_id] += 2
            
    def _update_intensity(self, curr_state, next_state, jump_tm):
        _lambda = self.Q[curr_state][next_state]
        n = self.jump_counts[curr_state]
        # update
        self.Q[curr_state][next_state] = _lambda*(n + 1) / (n + _lambda*jump_tm)
        self.Q[curr_state][curr_state] = -self.Q[curr_state][next_state]
        self.jump_counts[curr_state] += 1