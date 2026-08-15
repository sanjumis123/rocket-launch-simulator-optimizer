from math import pi

nose_cones = {
    "conical": {
        "nose_drag": 0.08,
        "complexity": 1.0,

        "volume": lambda r, l: (1/3) * pi * r**2 * l,

        # measured from nose tip
        "cg": lambda l: (3/4) * l,
        "cp": lambda l: (2/3) * l
    },

    "ogive": {
        "nose_drag": 0.035,
        "complexity": 1.2,

        "volume": lambda r, l: 0.52 * pi * r**2 * l,

        "cg": lambda l: 0.45 * l,
        "cp": lambda l: 0.466 * l
    },

    "elliptical": {
        "nose_drag": 0.025,
        "complexity": 1.3,

        "volume": lambda r, l: (2/3) * pi * r**2 * l,

        "cg": lambda l: (3/8) * l,
        "cp": lambda l: 0.333 * l
    },

    "parabolic": {
        "nose_drag": 0.028,
        "complexity": 1.4,

        "volume": lambda r, l: (8/15) * pi * r**2 * l,

        "cg": lambda l: 0.5 * l,
        "cp": lambda l: 0.5 * l
    }
}

fin_shapes = {
    "rectangular": {
        "drag_factor": 1.0,
        "complexity": 1.0,
        "taper_ratio": 1.0,
         "area": lambda cr, ct, h: cr * h,
         "cg": lambda cr, ct, m: cr/2,
         "cp": lambda fl, tc, m: fl/2,
         "sweep_angle": 0


    },

    "trapezoidal": {
        "drag_factor": 0.85,
        "complexity": 1.1,
        "taper_ratio": 0.5,
        "area": lambda cr, ct, h: ((cr + ct) / 2) * h,
        "cg": lambda cr, ct, m: m*(cr+2*ct)/(3*(cr+ct)) + (cr**2 + cr*ct + ct**2) / (3*(cr+ct)),
        "cp": lambda cr, ct, m: m*(cr+2*ct)/(3*(cr+ct)) + (1/6)*(cr + ct - (cr*ct)/(cr+ct)),
        "sweep_angle": 10
    },

    "swept": {
        "drag_factor": 0.75,
        "complexity": 1.3,
        "taper_ratio": 0.5,
        "area": lambda cr, ct, h: ((cr + ct) / 2) * h,
        "cg": lambda cr, ct, m: m*(cr+2*ct)/(3*(cr+ct)) + (cr**2 + cr*ct + ct**2) / (3*(cr+ct)),
        "cp": lambda cr, ct, m: m*(cr+2*ct)/(3*(cr+ct)) + (1/6)*(cr + ct - (cr*ct)/(cr+ct)),
        "sweep_angle": 45
    },

    "elliptical": {
        "drag_factor": 0.65,
        "complexity": 1.5,
        "taper_ratio": 0.0, 
        "area": lambda cr, ct, h: (pi / 4) * cr * h,
        "cg": lambda cr, ct, m: 0.42*cr,
        "cp": lambda fl, tc, m: 0.25*fl,
        "sweep_angle": 0
    }
}

materials = {
    "foam": {
        "density": 62,
        "surface_multiplier": 1.15,
        "cost_per_kg": 31
    },

    "plastic": {
        "density": 1240,
        "surface_multiplier": 1.01,
        "cost_per_kg": 23
    },

    "cardboard": {
        "density": 700,
        "surface_multiplier": 1.08,
        "cost_per_kg": 21
    },

    "pool noodle": {
        "density": 28,
        "surface_multiplier": 1.20,
        "cost_per_kg": 95

    }
}

snugness = {
    "loose": 1.0,
    "snug": 4.0,
    "tight": 7.0
}

snugness_airleakage = {
    "loose": 0.60,
    "snug": 0.90,
    "tight": 0.99
}