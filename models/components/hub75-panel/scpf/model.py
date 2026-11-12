"""Standalone entry point for the shared HUB75 mechanical component.

Opening the panel by itself runs the exact same Hub75Panel class that screen
assemblies import. The part keeps its own local CAD axes: front face in XY,
rear depth along +Z. Assemblies are responsible for world placement/rotation.
"""
from components.hub75 import Hub75Panel


Hub75Panel()
