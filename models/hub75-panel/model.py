"""Original two-panel regression: one component definition, two occurrences."""
from scpf import component
from components.hub75 import Hub75Panel as Hub75PanelDefinition

Hub75Panel = component(Hub75PanelDefinition)

class TwoHub75Panels:
    pitch_x = 160.0

    def build(self):
        first = Hub75Panel()
        second = first.copy().move(x=self.pitch_x)
        return first + second

TwoHub75Panels()
