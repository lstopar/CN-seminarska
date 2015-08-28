from users import PeriodicUser, SecondaryUser, MarkovianUser
import matplotlib.pyplot as plt

PRINT_INTERVAL = 1
DELTA_TIME = 1   # millisecond
TIME_UNIT = 1000  # 1 second

TOTAL_TIME = 100*TIME_UNIT

N_CHANNELS = 1
channels = [0] * N_CHANNELS

primary_users = [MarkovianUser(TIME_UNIT, 0, 1, 5)]
secondary_users = [SecondaryUser(TIME_UNIT, TIME_UNIT)]
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
    
    occupied_states = []
    times = []
    
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
        
        occupied_states.append(channels[0])
        times.append(curr_tm)
            
        if curr_tm % PRINT_INTERVAL == 0:
            print 'Iteration:', curr_tm, 'channels:', channels
 
        # increase time
        curr_tm += DELTA_TIME
        
    # calculate the effectiveness measures
    estimated = secondary_users[0].channel_availability
    
    existing_availability = 0
    estimated_availability = 0
    ratios = []
    for i, available in enumerate(occupied_states):
        existing_availability += available != 1
        estimated_availability += estimated[i] == 1
        ratios.append(float(estimated_availability) / existing_availability if existing_availability > 0 else 0)
        
    plt.plot(times, ratios)
    plt.axis([0, TOTAL_TIME, 0, 1])
    plt.show()

if __name__ == "__main__":
    main()
    print 'Printing the learned intensities ...'
    for user in secondary_users:
        print str(user.Q)