from users import PeriodicUser, SecondaryUser

PRINT_INTERVAL = 1
DELTA_TIME = 1   # millisecond
TIME_UNIT = 10.0  # TODO minute

TOTAL_TIME = 100*TIME_UNIT

N_CHANNELS = 1
channels = [0] * N_CHANNELS

primary_users = [PeriodicUser(TIME_UNIT, 0, 5*TIME_UNIT, 2*TIME_UNIT)]
secondary_users = [SecondaryUser(TIME_UNIT)]
# primary_users = [RandomUser(0, .1)]
            

#================================================================================
# HELPER METHODS
#================================================================================

def reset_channels():
    for i in range(N_CHANNELS):
        channels[i] = 0
    
def update_primaries(curr_tm):
    for user in primary_users:
        user.update(curr_tm)
        
def update_secondaries(curr_tm):
    for user in secondary_users:
        user.update(curr_tm, channels)
        
def write_primaries():
    for user in primary_users:
        user.write(channels)
        
def write_secondaries():
    for user in secondary_users:
        user.write(channels)

#================================================================================
# SIMULATION
#================================================================================

def main():
    print 'Running the simulation ...'
    
    curr_tm = 0
    while curr_tm < TOTAL_TIME:
        # reset channels and update the users
        reset_channels()
        update_primaries(curr_tm)
        write_primaries()
        
        # LISTEN-before-TALK policy - all the secondary users must check for
        # reappearance of the primary user before writing the next byte
        update_secondaries(curr_tm)
        write_secondaries()
            
        if curr_tm % PRINT_INTERVAL == 0:
            print 'Iteration:', curr_tm, 'channels:', channels
 
        # increase time
        curr_tm += DELTA_TIME

if __name__ == "__main__":
    main()
    print 'Printing the learned intensities ...'
    for user in secondary_users:
        print str(user.Q)