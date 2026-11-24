"""Smallest template Forge model: one parameterized native Box."""


class SimpleBox:
    length = 40.0
    width = 30.0
    height = 10.0

    def build(self):
        return Box(self.length, self.width, self.height, anchor=Anchor.BOTTOM)


SimpleBox()
