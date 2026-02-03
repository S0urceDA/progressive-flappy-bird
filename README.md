# Arcade Hardware Deployment: Progressive Flappy Bird

## Project Overview
This project is a custom modification of a Python-based game engine designed specifically for physical arcade hardware. It was deployed to a dedicated cabinet running Windows in a high-traffic student environment, logging over **3,000+ played sessions** with zero reported crashes.

Unlike standard clones, this version implements a **Progressive Difficulty Algorithm** that dynamically adjusts game physics based on player performance, designed to "lull the player into a false sense of security" before ramping up difficulty.

## Key Engineering Features

### 1. Progressive Difficulty Algorithm
Instead of static gameplay, the engine calculates difficulty deltas every frame based on the current score:
* **Scroll Speed Acceleration:** `scroll_speed += 0.00005 * score`
* **Obstacle Frequency:** `pipe_frequency -= 0.005 * score`
* **Pipe Gap:** Reduces as the game progresses, demanding higher precision from the user.

### 2. Hardware Adaptation & Resolution Scaling
The original engine was refactored to interface with specific arcade monitor constraints:
* **Resolution Port:** Scaled assets and hitboxes from native `864x936` to `1280x1024` to fit the cabinet display.
* **Input Handling:** Mapped arcade button inputs to Pygame event listeners for zero-latency response.

### 3. Persistent Data System
Implemented a robust file I/O system to track usage metrics across power cycles:
* **High Score Tracking:** Saves top performance locally.
* **Usage Metrics:** Logs total games played and timestamps of records (Unix Epoch) to monitor number of games played.

## Tech Stack
* **Language:** Python 3.x
* **Engine:** Pygame
* **Hardware:** Custom Arcade Cabinet running Windows

---
*Created by David Andras (S0urceDA)*
