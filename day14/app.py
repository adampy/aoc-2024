from dataclasses import dataclass

@dataclass
class Robot:
    posX: int
    posY: int
    velX: int
    velY: int
    
f = open("day14/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

robots = []
for line in lines:
    pos, vel = line.split(" ")
    pos = pos.replace("p=", "").split(",")
    vel = vel.replace("v=", "").split(",")
    robots.append(Robot(int(pos[0]), int(pos[1]), int(vel[0]), int(vel[1])))

# --- Part 1 ---

HEIGHT = 103
WIDTH = 101
TIMESTEPS = 10000

def print_grid(positions):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in positions:
                print(positions[(x,y)], end="")
            else:
                print(".", end="")
        print()

def get_robot_pos_at_time(robot, time):
    return ((robot.posX + robot.velX * time) % WIDTH, (robot.posY + robot.velY * time) % HEIGHT)

# Get positions of robots at time
positions = {}
for robot in robots:
    pos = get_robot_pos_at_time(robot, TIMESTEPS)
    if pos in positions:
        positions[pos] += 1
    else:
        positions[pos] = 1
    
# Count number in each quadrant
top_left = 0
top_right = 0
bottom_left = 0
bottom_right = 0

for pos in positions:
    tmp1 = (WIDTH // 2)
    tmp2 = (HEIGHT // 2)
    x, y = pos
    if x < tmp1 and y < tmp2:
        top_left += positions[pos]
    elif x > tmp1 and y < tmp2:
        top_right += positions[pos]
    elif x < tmp1 and y > tmp2:
        bottom_left += positions[pos]
    elif x > tmp1 and y > tmp2:
        bottom_right += positions[pos]

print(f"Part 1: {top_left * top_right * bottom_left * bottom_right}")

# --- Part 2 ---

def is_suspicious(positions, limit=5):
    count = 0
    for y in range(HEIGHT):
        count = 0
        for x in range(WIDTH):
            if (x, y) in positions:
                count += 1
                if count >= limit:
                    return True
            else:
                count = 0
    return False

for timestep in range(TIMESTEPS):
    # Calculate for each timestep
    positions = {}
    for robot in robots:
        pos = get_robot_pos_at_time(robot, timestep)
        if pos in positions:
            positions[pos] += 1
        else:
            positions[pos] = 1

    # Check for suspicious timesteps (i.e. that contain 5 or more robots aligned in a row)
    if is_suspicious(positions, limit=8):
        print_grid(positions)
        print(f"Above is timestep {timestep}")
    