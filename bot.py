# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    MapProxy,
    Vector,
    WeatherForecast,
    config,
)
from vendeeglobe.utils import distance_on_surface
from vendeeglobe import config

CREATOR = "🦑 ☠☠𝕂ℝÄ𝕂Ëℕ☠☠ 🐙"  # This is your team name


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """
    print(config.checkpoints[0])
    print(config.checkpoints[1])

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.avatar = "../../afonsos_bot/kraken.png"  # Optional attribute
        self.course = [
            Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),
            Checkpoint(longitude=-29.908577, latitude=17.999811, radius=50),
            Checkpoint(latitude=11.639738, longitude=-52.786058, radius=10),
            Checkpoint(latitude=11.820852, longitude=-60.555078, radius=10),
            Checkpoint(latitude=11.706513, longitude=-62.714800, radius=5),
            Checkpoint(latitude=14.950796, longitude=-73.025302, radius=15),
            Checkpoint(latitude=10.184482, longitude=-79.971065, radius=5),
            Checkpoint(latitude=9.477217, longitude=-79.951065, radius=5),
            Checkpoint(latitude=9.193906, longitude=-80.009630, radius=5),
            Checkpoint(latitude=8.869758, longitude=-79.461705, radius=5),
            Checkpoint(latitude=4.202637, longitude=-78.753701, radius=5),
            Checkpoint(latitude=3.802786, longitude=-87.740018, radius=5),
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1950),
            Checkpoint(latitude=-5.600926, longitude=-153.607253, radius=5),
            Checkpoint(latitude=-14.600926, longitude=-160.607253, radius=5),
            Checkpoint(latitude=-16.861951, longitude=-169.998368, radius=5),
            Checkpoint(latitude=-20.444844, longitude=-172.330914, radius=5),
            Checkpoint(latitude=-41.289193, longitude=-176.327763, radius=5),
            Checkpoint(latitude=-44.648524, longitude=174.505348, radius=5),
            Checkpoint(latitude=-49.497799, longitude=169.788539, radius=5),
            Checkpoint(latitude=-40.079012, longitude=110.808236, radius=5),
            Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190),
            Checkpoint(latitude=-37.071050, longitude=20.809699, radius=5),
            Checkpoint(latitude=-14.836600, longitude=-26.123895, radius=5),
            Checkpoint(latitude=16.538295, longitude=-20.081214, radius=5),
            Checkpoint(latitude=43.249473, longitude=-21.292899, radius=5),
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: WeatherForecast,
        world_map: MapProxy,
    ):
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            The weather forecast for the next 5 days.
        world_map:
            The map of the world: 1 for sea, 0 for land.
        """
        instructions = Instructions()
        for ch in self.course:
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
