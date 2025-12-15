'''
Tower Defense - AI development area


'''


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Offensive player
class OffensivePlayer:
    _resource = 0

    def __init__(self, location):
        self._location = location
        #TODO: Update logic (intelligence) when new player is created

    def move_player(self, field):
        
        # Assume all moves are possible
        prop = np.ones(8)

        # Bias moves towards target
        if self.resource <= 0:
            resource_bias = np.array([0,0,2,6,2,0,0,0])
        else:
            resource_bias = np.array([2,0,0,0,0,0,2,6])

        # Distance between all possibilities
        if self.resource <= 0:
            x_goal = np.ones(8) * GOAL_LOCATION[0]
            y_goal = np.ones(8) * GOAL_LOCATION[1]
        else:
            x_goal = np.ones(8) * SPAWNING_LOCATION[0]
            y_goal = np.ones(8) * SPAWNING_LOCATION[1]

        x_move = np.empty(8)
        y_move = np.empty(8)
        for dir in range(len(compass_moves)):
            new_location = add_coordinates(self.location, compass_moves[dir])
            x_move[dir] = new_location[0]
            y_move[dir] = new_location[1]

        diffDist = 0.5 + (x_move - x_goal)**2 + (y_move - y_goal)**2
        diffDist = diffDist / np.min(diffDist)
        diffDist[diffDist > 1] = 0
        resource_bias = diffDist

        # Take out illegal moves
        legal_moves = np.ones(8)
        if self.location[0] == 0:
            legal_moves[[5, 6, 7]] = 0# No moves west
        if self.location[1] == 0:
            legal_moves[[0, 1, 7]] = 0 # No moves north
        if self.location[0] == (GRID_WIDTH - 1):
            legal_moves[[1, 2, 3]] = 0 # No moves east
        if self.location[1] == (GRID_HEIGHT - 1):
            legal_moves[[3, 4, 5]] = 0 # No moves south

        # compass_moves = [N, NE, E, SE, S, SW, W, NW]

        # Normalise distributions
        dist = self._normArray(legal_moves * (
            self._normArray(prop) + 
            self._normArray(resource_bias) * 10
        )
        )
        cumDist = np.cumsum(dist)
        rnd = np.random.rand(1)
        index = np.argmax(rnd <= cumDist)

        response = check_move(self, compass_moves[index], field)
        if response != None:
            print(f"Move error: {MOVE_ERRORS.get(response)}")

    def _normArray(self, arr):
        if sum(arr) == 0: return arr * 0
        return arr / sum(arr)

    @property
    def location(self):
        return self._location
    @location.setter
    def location(self, value):
        self._location = value

    @property
    def resource(self):
        return self._resource
    @resource.setter
    def resource(self, value):
        self._resource = value


def check_move(player, move, field):
    # Calc. new location
    new_location = add_coordinates(player.location, move)
    # If new location empty
    # TODO: Logic
    # If new location on field
    if (
        (new_location[0] < 0) or
        (new_location[1] < 0) or
        (new_location[0] > (GRID_WIDTH - 1)) or 
        (new_location[1] > (GRID_HEIGHT -1))
    ):
         return MOVE_ERRORS.get('off field')

    # Requested move is acceptable
    player.location = new_location
    return None

def add_coordinates(a, b):
        # TODO: Check inputs are valid
        return (a[0] + b[0], a[1] + b[1])

def compare_coordinates(a, b):
    # Same
    if ((a[0] == b[0]) and (a[1] == b[1])):
        return COORD_COMPARISON.get('same')
    # Within 1 move
    elif ((abs(a[0] - b[1]) <= 1) and (abs(a[1] - b[1]) <= 1)):
        return COORD_COMPARISON.get('within 1 move')
    else:
        return COORD_COMPARISON.get('other')

def init():
     point.set_data([],[])
     return home, goal, point

def update_plot(player_list):
     x = []
     y = []
     for player in player_list:
         x.append(player.location[0])
         y.append(player.location[1])
     point.set_data(x, y)
     return point,

def game_loop():
    running = True
    turns = 0
    max_turns = 10000
    max_players_on_field = 10

    total_resource = 10
    goal_resource = total_resource
    spawn_resource = 0

    while running:

        ## Spawn player?
        if len(player_list) < max_players_on_field: 
            if len(player_list) <= spawn_resource / 2:
                player_list.append(OffensivePlayer(SPAWNING_LOCATION))

        ## Game select player
        for player in player_list:

            ## Game ask player to move, Player requests move, Game allows move or not
            player.move_player(field_grid)

            ## Game assesses impact of move
            if compare_coordinates(player.location, GOAL_LOCATION) == COORD_COMPARISON.get('same'):
                if goal_resource > 0: 
                    player.resource += 1
                    goal_resource -= 1
                    print(f"Resource update - Goal: {goal_resource}, Spawn: {spawn_resource} (No. Players: {len(player_list)})")
            if compare_coordinates(player.location, SPAWNING_LOCATION) == COORD_COMPARISON.get('same'):
                if player.resource > 0:
                    spawn_resource += player.resource
                    player.resource = 0
                    print(f"Resource update - Goal: {goal_resource}, Spawn: {spawn_resource} (No. Players: {len(player_list)})")


        ## Update graphics
        yield player_list

        ## Loop delay 

        if spawn_resource >= total_resource:
            running = False
            print(f"All resource at spawn location in {turns} turns")

        turns += 1
        if turns >= max_turns: 
            running = False
            print(f"Turn {turns} complete, exit loop: {running}")
        


# 1. Initalise game

# Possible coordinate comparision
COORD_COMPARISON = {
    'same': 1,
    'within 1 move': 2,
    'other': 3
}

# Possible move errors
MOVE_ERRORS = {
     'off field': 1, 
     'space occupied': 2,
     'other': 3
}

# Possible moves
N  = (0, -1)
S  = (0, 1)
E  = (1, 0)
W  = (-1, 0)
NE = (1, -1)
NW = (-1, -1)
SE = (1, 1)
SW = (-1, 1)

compass_moves = [N, NE, E, SE, S, SW, W, NW]

# compass_moves = {
#      'N': N,
#      'S': S,
#      'E': E,
#      'W': W,
#      'NE': NE,
#      'NW': NW,
#      'SE': SE,
#      'SW': SW
# }

# Define grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Set key locations
SPAWNING_LOCATION = (0, 0)
GOAL_LOCATION = (GRID_HEIGHT - 1, GRID_WIDTH - 1)

# Initialise game tracking 
field_grid = np.zeros([GRID_HEIGHT, GRID_WIDTH], dtype=int)
player_list = []

# Setup plot
fig, ax = plt.subplots()
ax.set_xlim([-1, GRID_WIDTH + 1])
ax.set_ylim([-1, GRID_HEIGHT + 1])
ax.grid(True)

cmap = mpl.colormaps['viridis']
color_list = cmap.resampled(10).colors

point, = ax.plot([], [], 'o', color = 'red')
home, = ax.plot([SPAWNING_LOCATION[0]], [SPAWNING_LOCATION[1]], 's', color = 'blue', ms=20)
goal, = ax.plot([GOAL_LOCATION[0]], [GOAL_LOCATION[1]], 's', color = 'grey', ms=20)

# 2. Game loop

ani = animation.FuncAnimation(
     fig=fig,
     func=update_plot,
     frames=game_loop(),
     init_func=init,
     interval=100,
     blit=False,
     cache_frame_data=False,
     repeat=False
)
plt.show()
# Exit and clean up
