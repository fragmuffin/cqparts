import cadquery
from cadquery import BoxSelector
from math import pi, cos, sqrt

from .base import ScrewDrive, screw_drive

from ...params import *


class AcentricWedgesScrewDrive(ScrewDrive):
    count = IntRange(1, None, 4)
    width = PositiveFloat(0.5)
    acentric_radius = PositiveFloat(None)  # defaults to width / 2

    def initialize_parameters(self):
        super(AcentricWedgesScrewDrive, self).initialize_parameters()
        if self.acentric_radius is None:
            self.acentric_radius = self.width / 2

    def apply(self, workplane, offset=(0, 0, 0)):
        # Start with a cylindrical pin down the center
        tool = cadquery.Workplane("XY") \
            .circle(self.width / 2).extrude(-self.depth)

        # Create a single blade
        points = [
            (0, 0),
            (0, -self.depth),
            (-self.width / 2, -self.depth),
            (-self.diameter / 2, 0),
        ]
        blade = cadquery.Workplane("XZ").workplane(offset=self.acentric_radius - (self.width / 2)) \
            .moveTo(*points[0]).polyline(points[1:]).close() \
            .extrude(self.width)

        for i in range(self.count):
            angle = i * (360. / self.count)
            tool = tool.union(
                blade.translate((0, 0, 0)) \
                    .rotate((0, 0, 0), (0, 0, 1), angle)
            )

        return workplane.cut(tool.translate(offset))


@screw_drive('tri_point')
class TripointScrewDrive(AcentricWedgesScrewDrive):
    count = IntRange(1, None, 3)
    acentric_radius = PositiveFloat(0.0)  # yeah, not my best class design, but it works


@screw_drive('torq_set')
class TorqsetScrewDrive(AcentricWedgesScrewDrive):
    count = IntRange(1, None, 4)