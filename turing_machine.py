class TuringMachine:
    def __init__(self, config):
        self.states = config['states']
        self.initial_state = config['initial_state']
        self.accept_state = config['accept_state']
        try:
            self.reject_state = config['reject_state']
        except Exception:
            self.reject_state = None

        self.transitions = config['transitions']

        try:
            self.positions = config['positions']
        except Exception:
            self.positions = None