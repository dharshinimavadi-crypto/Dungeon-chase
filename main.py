
import random
from collections import deque
grid=[list("####################"),
      list("##...$......##....##"),
      list("###....##....##....#"),
      list("##..P....##.$...#.P#"),
      list("#..##...##........##"),
      list("#..$.##...##...##..#"),
      list("##....##...##...##.#"),
      list("##################.E")]

moves={
    "u":(0, -1),
    "d":(0, 1),
    "l":(-1, 0),
    "r":(1, 0)
}

class player:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.health=20
        self.score=0
        self.steps=0

class monster:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.health=12



def next_step(start, goal):
    if start==goal:
        return start
    queue=deque([start])
    came_from={start:None}
    while queue:
        current=queue.popleft()
        if current==goal:
            break
        x, y= current
        for dx, dy in [(0, -1),(0, 1),(-1, 0),(1, 0)]:
            nxt=(x+dx, y+dy)
            if 0<=nxt[0]<len(grid[0]) and 0<=nxt[1] < len(grid) and grid[nxt[1]][nxt[0]]!="#" and nxt not in came_from:
                came_from[nxt]=current
                queue.append(nxt)
    if goal not in came_from:
        return start
    step=goal
    while came_from[step]!=start:
        step= came_from[step]
    return step

def draw_map(player, monster):
    for y in range(len(grid)):
            row=""  
            for x in range(len(grid[y])):
                if x==player.x and y==player.y:
                    row+="@"
                elif monster and x==monster.x and y==monster.y:
                    row+="M"
                else:
                    row+=grid[y][x]
            print(row)

player=player(2, 1)
monster=monster(2, 4)


while True:
    draw_map(player, monster)
    print("HP:", player.health, "| Score:", player.score, "| Steps:",player.steps)
    key=input("Move (u/d/l/r/q to quit):")
    if key=="q":
        print("Thanks for playing")
        break
    if key not in moves:
        print("Use u, d, l, r or q.")
        continue
    dx, dy=moves[key]
    nx, ny=player.x+dx, player.y+dy
    if monster and (nx, ny)==(monster.x, monster.y):
        damage=random.randint(1, 4)
        monster.health-=damage
        print("you hit the monster for", damage)
        if monster.health<=0:
            print("You Win...!")
            break
    elif grid[ny][nx]!="#":
        player.x, player.y=nx, ny
        player.steps+=1
        if grid[ny][nx]=="$":
            print("Yeah! You found treasure")
            grid[ny][nx]="."
            player.score+=10
    else:
        print("Ouch! That's a wall")
    if grid[ny][nx]=="P":
        print("You drank a potion!")
        grid[ny][nx]="."
        player.health+=5

    if grid[ny][nx]=="E":
            print("You found the exit🏆!")

    if monster:
        distance=abs(monster.x-player.x) + abs(monster.y-player.y)
        if distance==1:
            damage=random.randint(1, 3)
            player.health-=damage
            print("The monster hits you for",damage)
        else:
            monster.x, monster.y =next_step(
                (monster.x, monster.y),(player.x, player.y)
            )
    if player.health<=0:
        print("you died. Game Over!")
        break

