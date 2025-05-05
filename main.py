from user_interface.terminal_ui import Loader
from bodies.celestial import CelestialBody
from user_interface.terminal_ui import TerminalInterface
import sys

class OrbitalToolkit:
    def __init__(self):
        self.loader = Loader()
        self.body_manager = CelestialBody()
        self.interface = TerminalInterface()
        
    def initialize(self):
        self.loader.scan_directory("maneuvers")
        self.loader.scan_directory("bodies")
        self.interface.show_welcome()
        
    def run(self):
        body = self.interface.select_body(self.body_manager.bodies)
        maneuver = self.interface.select_maneuver(self.loader.modules)
        params = self.interface.get_parameters(maneuver)
        result = maneuver['module'].calculate(params | {'body': body})
        self.interface.show_results(result)

if __name__ == "__main__":
    toolkit = OrbitalToolkit()
    toolkit.initialize()
    
    try:
        toolkit.run()
    except KeyboardInterrupt:
        print("\n🚀 Session terminated by user. Safe travels!")
        sys.exit(0)