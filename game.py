from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import choice, random
from freegames import vector

# Define colors
COLORS = [(0, 0, 0), (0, 1, 0), (1, 1, 0)]  # RGB tuples

# Ball speed factors
BALL_SPEED_X = 3
BALL_SPEED_Y = 3


# Paddle size
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50

# Screen size
SCREEN_WIDTH = 420
SCREEN_HEIGHT = 420

# Initialize ball, aim, and state
ball = vector(0, 0)
aim = vector(BALL_SPEED_X, BALL_SPEED_Y)
state = {1: 0, 2: 0}


def value():
    """Randomly generate value between (-5, -3) or (3, 5)."""
    return (3 + random() * 2) * choice([1, -1])


def move(player, change):
    """Move player position by change."""
    state[player] += change


def draw_paddle(x, y, width, height):
    """Draw paddle."""
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def draw_ball(x, y):
    """Draw ball."""
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw():
    """Draw game and move pong ball."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw paddles
    glColor3f(COLORS[1][0], COLORS[1][1], COLORS[1][2])
    draw_paddle(-200, state[1], PADDLE_WIDTH, PADDLE_HEIGHT)
    glColor3f(COLORS[2][0], COLORS[2][1], COLORS[2][2])
    draw_paddle(190, state[2], PADDLE_WIDTH, PADDLE_HEIGHT)

    # Draw ball
    ball.move(aim)
    x = ball.x
    y = ball.y
    glColor3f(COLORS[0][0], COLORS[0][1], COLORS[0][2])
    draw_ball(x, y)

    # Handle ball-wall collisions
    if y < -200 or y > 200:
        aim.y = -aim.y

    # Handle ball-paddle collisions
    if x < -185:
        low = state[1]
        high = state[1] + PADDLE_HEIGHT
        if low <= y <= high:
            aim.x = -aim.x
        else:
            return
    if x > 185:
        low = state[2]
        high = state[2] + PADDLE_HEIGHT
        if low <= y <= high:
            aim.x = -aim.x
        else:
            return

    glutSwapBuffers()


def change_frame_rate(rate):
    """Change the frame rate of the game."""
    glutTimerFunc(rate, draw, 0)


def change_ball_speed(new_speed_x, new_speed_y):
    """Change the speed of the ball."""
    aim.x = new_speed_x
    aim.y = new_speed_y


def change_paddle_size(width, height):
    """Change the size of the paddles."""
    global PADDLE_WIDTH, PADDLE_HEIGHT
    PADDLE_WIDTH = width
    PADDLE_HEIGHT = height


def change_wall_bounce_behavior():
    """Change how the ball bounces off walls."""
    aim.x *= 0.9
    aim.y *= 0.9


def add_computer_player():
    """Add a computer player."""
    pass  # Implement AI logic to control the second paddle


def add_second_ball():
    """Add a second ball."""
    pass  # Implement logic to add another ball


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Pong Game')

    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutTimerFunc(50, draw, 0)

    glutKeyboardFunc(keyboard)

    setup()

    glutMainLoop()


def setup():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    if key == b'w':
        move(1, 20)
    elif key == b's':
        move(1, -20)
    elif key == b'i':
        move(2, 20)
    elif key == b'k':
        move(2, -20)


if __name__ == "__main__":
    main()
