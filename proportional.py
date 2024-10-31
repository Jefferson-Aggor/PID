import numpy as np
from elevator import sim_run

# Simulator Options
options = {}
options['FIG_SIZE'] = [8, 8]
options['PID_DEBUG'] = False

# Physics Options
options['GRAVITY'] = True
options['FRICTION'] = True
options['ELEVATOR_MASS'] = 500
options['COUNTERWEIGHT_MASS'] = 500
options['PEOPLE_MASS'] = 0

# Controller Options
options['CONTROLLER'] = True
options['START_LOC'] = 0.0
options['SET_POINT'] = 6.0
options['OUTPUT_GAIN'] = 1000


class Controller:
    def __init__(self, reference):
        self.r = reference
        self.prev_time = 0
        self.output = 0

    def run(self, x, t):
        if t - self.prev_time < 0.05:
            return self.output
        else:
            self.prev_time = t
            # Proportional control (P)
            kp = 1
            e = self.r - x
            self.output = kp * e

            return self.output

sim_run(options, Controller)
