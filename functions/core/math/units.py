class UnitConverter:
    # Conversion factors
    KM_TO_M = 1000
    M_TO_FT = 3.28084
    KM_TO_NMI = 0.539957

    @classmethod
    def celestial_params(cls, data: dict) -> dict:
        return {
            "radius_m": data["radius_km"] * cls.KM_TO_M,
            "mu_m3_s2": data["mu_km3_s2"] * (cls.KM_TO_M**3)
        }

    @classmethod
    def format_velocity(cls, mps: float) -> str:
        return f"{mps:.3f} m/s | {mps * cls.M_TO_FT:.2f} fps | {mps * 3.6:.2f} km/h"

    @classmethod
    def format_altitude(cls, meters: float) -> str:
        km = meters / cls.KM_TO_M
        return (
            f"{km:.2f} km | "
            f"{meters * cls.M_TO_FT:,.0f} ft | "
            f"{km * cls.KM_TO_NMI:.2f} nmi"
        )