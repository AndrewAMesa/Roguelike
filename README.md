# Roguelike

This is a roguelike game developed using Python and Pygame, featuring procedural generation to produce unique levels. The goal is to see how many levels you can survive until you lose by running out of health.

## Gameplay

To progress to the next level, you will be assigned one of three tasks:
1. **Find a Portal:** Upon finding it (in portal levels, your health is lowered).
2. **Defeat Enemies:** A certain number of enemies need to be defeated to proceed.
3. **Defeat a Boss:** Every five levels, you’ll face a boss. In this level, sprinting is disabled, and to damage the boss, you must stun it by making it charge into a wall.

### Controls

- **Movement:** `W`, `A`, `S`, `D` or Arrow keys
- **Sprint:** `Shift` (limited duration)
- **Attack:** 
  - **Sword:** Left-click
  - **Gun:** Right-click (you gain one projectile every five sword hits)

The player will face the cursor’s direction on the screen.

### Features

- **Collectibles:** Heal or increase your damage.
- **Traps and Tiles:** Some tiles will hurt you; others are traps you can set off.

## Known Issues

- **Enemy Pathfinding Bug:** In rare positions, some enemies may temporarily stop chasing you.
