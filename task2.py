import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle
from streamlit.components.v1 import html
import tempfile
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Weighted Character Lift & Toss",
    layout="centered"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown("""
# 🎬 Weighted Character Lift & Toss

Animate a simple character interacting with a heavy object.
The motion reflects:

- Anticipation
- Weight & Effort
- Balance
- Follow-through
""")

# ---------------------------------------------------
# FIGURE
# ---------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))

ax.set_xlim(0, 12)
ax.set_ylim(0, 8)

ax.set_aspect('equal')
ax.axis('off')

# Ground
ax.plot([0, 12], [1, 1], color='black', linewidth=3)

# ---------------------------------------------------
# OBJECT (Heavy Box)
# ---------------------------------------------------
box = Rectangle(
    (4, 1),
    1.5,
    1.5,
    facecolor='black'
)

ax.add_patch(box)

# Arrow on box
arrow_text = ax.text(
    4.75,
    1.75,
    "↑",
    fontsize=26,
    color='yellow',
    ha='center',
    va='center',
    weight='bold'
)

# ---------------------------------------------------
# CHARACTER
# ---------------------------------------------------
head = Circle((2, 4), 0.3, color='black')
ax.add_patch(head)

# Body Parts
body, = ax.plot([], [], lw=6, color='#8A2BE2')
left_arm, = ax.plot([], [], lw=4, color='black')
right_arm, = ax.plot([], [], lw=4, color='black')
left_leg, = ax.plot([], [], lw=4, color='black')
right_leg, = ax.plot([], [], lw=4, color='black')

# ---------------------------------------------------
# ANIMATION
# ---------------------------------------------------
TOTAL_FRAMES = 180
FPS = 30


def update(frame):

    # -------------------------------------------
    # PHASE 1 : ANTICIPATION (Squash)
    # -------------------------------------------
    if frame < 50:

        t = frame / 50

        char_x = 3
        char_y = 2.5 - 0.7 * t

        lean = -0.3 * t

        box_x = 4
        box_y = 1

    # -------------------------------------------
    # PHASE 2 : LIFT (Effort)
    # -------------------------------------------
    elif frame < 120:

        t = (frame - 50) / 70

        char_x = 3 + 1.2 * t
        char_y = 1.8 + 1.2 * t

        lean = 0.5

        box_x = 4 + 1.2 * t
        box_y = 1 + 2 * t

    # -------------------------------------------
    # PHASE 3 : TOSS + FOLLOW THROUGH
    # -------------------------------------------
    else:

        t = (frame - 120) / 60

        char_x = 4.2
        char_y = 3

        lean = 0.2 - 0.2 * t

        # Box toss trajectory
        box_x = 5.2 + 2 * t
        box_y = 3 + 3 * np.sin(t * np.pi)

    # -------------------------------------------
    # UPDATE BOX
    # -------------------------------------------
    box.set_xy((box_x, box_y))

    arrow_text.set_position((box_x + 0.75, box_y + 0.75))

    # -------------------------------------------
    # CHARACTER BODY
    # -------------------------------------------
    shoulder_x = char_x
    shoulder_y = char_y + 1.4

    hip_x = char_x - lean
    hip_y = char_y

    # Head
    head.center = (shoulder_x, shoulder_y + 0.5)

    # Body
    body.set_data(
        [shoulder_x, hip_x],
        [shoulder_y, hip_y]
    )

    # -------------------------------------------
    # ARMS
    # -------------------------------------------
    hand_x = box_x + 0.2
    hand_y = box_y + 1

    left_arm.set_data(
        [shoulder_x, hand_x],
        [shoulder_y - 0.1, hand_y]
    )

    right_arm.set_data(
        [shoulder_x, hand_x + 0.3],
        [shoulder_y - 0.1, hand_y]
    )

    # -------------------------------------------
    # LEGS
    # -------------------------------------------
    spread = 0.5 + abs(lean) * 0.5

    left_leg.set_data(
        [hip_x, hip_x - spread],
        [hip_y, 1]
    )

    right_leg.set_data(
        [hip_x, hip_x + spread],
        [hip_y, 1]
    )

    return (
        head,
        body,
        left_arm,
        right_arm,
        left_leg,
        right_leg,
        box,
        arrow_text
    )


# ---------------------------------------------------
# CREATE ANIMATION
# ---------------------------------------------------
ani = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=True
)

# ---------------------------------------------------
# SAVE TEMP HTML
# ---------------------------------------------------
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:

    ani.save(tmp.name, writer="html")

    temp_path = tmp.name

# ---------------------------------------------------
# DISPLAY ANIMATION
# ---------------------------------------------------
with open(temp_path, "r", encoding="utf-8") as f:
    source_code = f.read()

html(source_code, height=600)

# Cleanup
os.remove(temp_path)

# ---------------------------------------------------
# EXPLANATION
# ---------------------------------------------------
st.markdown("---")

st.subheader("🎯 Animation Principles Used")

st.markdown("""
### 1. Anticipation
The character squashes downward before lifting.

### 2. Effort
Slow lifting speed shows the object is heavy.

### 3. Balance
Legs spread wider while carrying the weight.

### 4. Follow-through
After tossing, the body settles naturally.

### 5. Realistic Weight
The object moves slowly upward and follows an arc.
""")
