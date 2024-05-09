from utils.helpers import percent_to_value



class PWMChannelForMotor:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.channel.duty_cycle = 0
    
    
    def _percent_of_power_to_hex(self, percent_of_power: float):
        return percent_to_value(percent_of_power)
    
    
    def run_at(self, percent_of_power: float):
        self.channel.duty_cycle = self._percent_of_power_to_hex(percent_of_power)
        
        
    def stop(self):
        self.channel.duty_cycle = 0