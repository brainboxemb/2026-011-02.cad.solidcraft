# HUB75 improved v2 source

Corrected native source supplied by the project owner on 2026-11-25.

- `hub75_improved_v2.json`
  - SolidCraft JSON export
  - size: 85623 bytes
  - SHA-256: `6ca80ad1c6c0e790ab7607097f5a6e9f2450c5b4f90406d94c76a66664ab3ce0`
  - format: `solidcraft/68`
- `hub75_improved_v2.sc`
  - native SolidCraft container
  - size: 3050197 bytes
  - SHA-256: `bb2ee4d6889e9a3ca3030578a3cc66ad46235d5eaf81c55840f81f720e72ca75`

## v2 correction scope

Compared semantically with the previously retained `hub75_improved.json`, v2
contains three mechanically meaningful mirror corrections:

1. the two middle reinforcement sets move to (+mount_x,+11) and (-mount_x,-11);
2. the locator pins move to (+75,+110) and (-75,-110);
3. the power connector moves to the opposite X side.

The two HUB75 data connector envelopes and all four white orientation-arrow
profiles are unchanged. Two empty native hole `face_names` changes are source
metadata only and are not modelled as separate Forge geometry.
