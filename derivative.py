import numpy as np
from elevator import sim_run

# Simulator Options
options = {}
options['FIG_SIZE'] = [8, 8] 
options['PID_DEBUG'] = False

# Physics Options
options['GRAVITY'] = True
options['FRICTION'] = True
options['ELEVATOR_MASS'] = 1000
options['COUNTERWEIGHT_MASS'] = 1000
options['PEOPLE_MASS'] = 100

# Controller Options
options['CONTROLLER'] = True
options['START_LOC'] = 3.0
options['SET_POINT'] = 27.0
options['OUTPUT_GAIN'] = 2000


class PDController:
    def __init__(self, reference):
        self.r = reference
        self.prev_time = 0
        self.prev_error = None
        self.output = 0
        # Part of PID DEBUG
        self.output_data = np.array([[0, 0, 0, 0]])

    def run(self, x, t):
        kp = 0.2
        kd = 0.75

        # Controller run time.
        if t - self.prev_time < 0.05:
            return self.output
        else:
            dt = t - self.prev_time
            self.prev_time = t

            # error.
            e = self.r - x

            # Calculate proportional control output.
            P_out = e * kp

            # Calculate derivative control output.
            if self.prev_error != None:
                D_out = (e - self.prev_error)/dt * kd
                self.prev_error = e
            else:
                D_out = 0
                self.prev_error = e

            # Calculate final output.
            self.output = P_out + D_out

            I_out = 0
            self.output_data = np.concatenate((self.output_data, \
                np.array([[t, P_out, I_out, D_out]])))

            return self.output

sim_run(options, PDController)
