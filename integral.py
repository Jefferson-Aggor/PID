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
options['COUNTERWEIGHT_MASS'] = 2000
options['PEOPLE_MASS'] = 800
# Also try 200, 50, and -200.

# Controller Options
options['CONTROLLER'] = True
options['START_LOC'] = 3.0 
options['SET_POINT'] = 27.0
options['OUTPUT_GAIN'] = 2000


class PIDController:
    def __init__(self, reference):
        self.r = reference
        self.prev_time = 0
        self.prev_error = None
        self.integral = 0
        self.output = 0
        self.output_max = 2.5
        self.windup = 5
        # Part of PID DEBUG
        self.output_data = np.array([[0, 0, 0, 0]])

    def run(self, x, t):
        kp = 1.5
        ki = 0.25
        kd = 2.5

        # Controller run time.
        if t - self.prev_time < 0.05:
            return self.output
        else:
            dt = t - self.prev_time
            self.prev_time = t

            # Calculate error.
            e = self.r - x

            # Calculate proportional control output.
            P_out = kp * e

            # Calculate integral control output.
        
            self.integral += e * dt

            # Apply windup to prevent integral windup.
            if self.integral > self.windup:
                self.integral = self.windup
            elif self.integral < -self.windup:
                self.integral = -self.windup

            I_out = self.integral * ki

            # Calculate derivative control output.
            if self.prev_error != None:
                D_out = (e - self.prev_error)/(dt) * kd
                self.prev_error = e
            else:
                D_out = 0
                # Set this to error.
                self.prev_error = e

            # Calculate final output.
            self.output = P_out + I_out + D_out

            if self.output > self.output_max:
                self.output = self.output_max
            elif self.output < -self.output_max:
                self.output = -self.output_max

            self.output_data = np.concatenate((self.output_data, \
                np.array([[t, P_out, I_out, D_out]])))

            return self.output

sim_run(options, PIDController)
