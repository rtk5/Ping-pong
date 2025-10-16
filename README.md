# Terminal-Based Ping Pong Game with Pygame

Build an interactive two-player ping pong game in your terminal using **Pygame**. This project teaches real-time game mechanics, object-oriented programming, and AI opponent behavior through hands-on development with LLM assistance.

---

## Project Overview

You'll receive a foundational ping pong game that includes:

- Controllable player paddle and computer-controlled opponent
- Dynamic ball physics with collision detection
- Live scoreboard tracking

Your mission: **debug, enhance, and extend** this codebase to create a polished, fully-featured game using AI-assisted development techniques.

### **Required LLM Tool: ChatGPT**

Use ChatGPT for all vibecoding activities in this assignment.

---

## Installation & Launch

### Environment Setup

1. Obtain the project files (clone repository or extract archive)
2. Verify Python 3.10 or higher is installed
3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Launch the game:

```bash
python main.py
```

---

## Beginning Your LLM Collaboration

Start your ChatGPT session with this foundational prompt:

```
I'm working on a real-time Ping Pong game using Python and Pygame. I have a partially working project structure. help me with reviewing the logic and also guide me as to how i shd implement the missing features. Review my code and answer subsequent questions
```

---

## Accelerated Development Prompts

Below are ready-to-use prompts for each development task. These are optimized for quick LLM interaction - simply copy and paste into your chat session.

**Important:** Generated code may work initially but could contain edge cases or implementation nuances requiring your scrutiny. This deliberate design helps you practice critical code evaluation skills.

---

## Development Tasks

Complete each objective through iterative collaboration with your LLM, followed by thorough code review and testing.

### Task 1: Enhanced Collision Detection

> Current issue: Ball occasionally phases through paddles during high-velocity gameplay. Improve collision accuracy.

**Starter Prompt:**
```
Please help me with my ping pong game's ball collision. Sometimes the ball goes through paddles. When it occurs, I must reverse velocity_x and see if the ball's rectangle overlaps with the paddle rectangles. Add the collision check as soon as you move the ball, and it should function flawlessly at high speeds.
```

### Task 2: Victory Condition & End Screen

> Implement game conclusion logic that triggers when any player achieves a target score (default: 5 points), displaying the winner before exit or restart.

**Starter Prompt:**
```
When a player scores five points, I need a game to play over the screen. Make a method that displays "Player Wins!" or "AI Wins!" on the screen after determining whether either score equals 5. To ensure that players see the message, make sure the game loop is maintained. Before ending the pygame, add a brief delay.
```

### Task 3: Match Replay System

> Post-game, present players with tournament format options (best of 3/5/7) or exit choice.

**Starter Prompt:**
```
After the game is over, provide a replay feature. "Best of 3", "Best of 5", "Best of 7", or "Exit" alternatives should be displayed. Await input from the user using keys 3, 5, 7, or ESC. Reset the ball location and update the winning score target when they make a decision. They should be able to play again after that.
```

### Task 4: Audio Feedback Integration

> Implement sound effects for key game events: paddle collisions, wall bounces, and scoring.

**Starter Prompt:**
```
Enhance my ping pong game in Python with sound effects. Use pygame.mixer to load.wav files for scoring, wall bounce, and paddle hit.Sound(). Every time ball.velocity_x or ball.velocity_y changes, play the sounds. At the beginning of the file, initialize pygame.mixer.
```

---

## Target Functionality

Upon completion, your game should feature:

- Responsive paddle control via `W` (up) and `S` (down) keys
- Challenging AI opponent with tracking behavior
- Accurate ball physics with proper rebound mechanics
- Real-time score updating for both players
- Automatic game termination with optional rematch functionality

---

## Project Architecture

```
pygame-pingpong/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── game/
│   ├── game_engine.py     # Core game logic
│   ├── paddle.py          # Paddle entity
│   └── ball.py            # Ball entity
└── README.md              # This file
```

---

## Submission Requirements

Verify all criteria before submitting:

- [ ] All four tasks implemented and functional
- [ ] Game runs without errors or crashes
- [ ] Expected behaviors match specifications
- [ ] LLM-assisted code review completed for all changes
- [ ] Victory screen displays correct winner
- [ ] Score rendering works for both player and AI
- [ ] All dependencies documented in `requirements.txt`
- [ ] Setup instructions verified through clean installation test
- [ ] Code maintains modularity and readability standards
- [ ] **Complete ChatGPT conversation history URL included with submission**

---

## Additional Notes

This project emphasizes learning through AI collaboration. While the LLM will provide working code suggestions, your responsibility is to:

- Understand every line of generated code
- Test edge cases thoroughly
- Refactor for clarity and maintainability
- Document your decision-making process

Good luck and enjoy building your game!
