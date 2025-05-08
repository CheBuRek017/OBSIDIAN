import math

class OrbitalCalculator:
    def __init__(self, mu: float):
        self.mu = mu  # m³/s²
        
    def vel_orbital(self, r: float, a: float) -> float:
        return math.sqrt(self.mu * (2/r - 1/a))
    
    def hohmann_transfer(self, r1: float, r2: float) -> tuple:
        a_trans = (r1 + r2) / 2
        dv1 = self.vel_orbital(r1, a_trans) - self.vel_orbital(r1, r1)
        dv2 = self.vel_orbital(r2, r2) - self.vel_orbital(r2, a_trans)
        return (dv1, dv2)
    
    def circularize_burn(self, a: float, e: float, r_target: float) -> tuple:
        h = math.sqrt(self.mu * a * (1 - e**2))
        cos_theta = ((a * (1 - e**2) / r_target) - 1) / e
        theta = math.arccos(cos_theta)
        vr = (self.mu * e * math.sin(theta)) / h
        vt = (self.mu * (1 + e * math.cos(theta))) / h
        return (vr, vt)