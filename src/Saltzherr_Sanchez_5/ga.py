import copy
import heapq
import metrics
import multiprocessing.pool as mpool
import os
import random
import shutil
import time
import math

width = 200
height = 16

options = [
    "-",  # an empty space
    "X",  # a solid wall
    "?",  # a question mark block with a coin
    "M",  # a question mark block with a mushroom
    "B",  # a breakable block
    "o",  # a coin
    "|",  # a pipe segment
    "T",  # a pipe top
    "E",  # an enemy
    #"f",  # a flag, do not generate
    #"v",  # a flagpole, do not generate
    #"m"  # mario's start position, do not generate
]

# The level as a grid of tiles


class Individual_Grid(object):
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None

    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.
    def calculate_fitness(self):
        measurements = metrics.metrics(self.to_level())
        # Print out the possible measurements or look at the implementation of metrics.py for other keys:
        # print(measurements.keys())
        # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
        # STUDENT Modify this, and possibly add more metrics.  You can replace this with whatever code you like.
        coefficients = dict(
            meaningfulJumpVariance=0.7,
            negativeSpace=0.6,
            pathPercentage=0.5,
            emptyPercentage=0.6,
            linearity=-0.5,
            solvability=2.0,
            decorationPercentage = 2.0,
            


        )
        self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                                coefficients))
        return self

    # Return the cached fitness value or calculate it as needed.
    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        
        return self._fitness

    # Mutate a genome into a new genome.  Note that this is a _genome_, not an individual!
    def mutate(self, genome):
        # STUDENT implement a mutation operator, also consider not mutating this individual
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
        

        if random.random() < 0.9 and len(genome) > 0:

            
                               
            to_change_y = random.randint(0, len(genome) - 1)    
            dey = genome[to_change_y]
            to_change_x = random.randint(0, len(dey) - 1)
            # dex = dey[to_change_x]                      
                         
            if to_change_x == 1 or to_change_x == len(dey)-1 or to_change_y == 0 or to_change_y == 15:
                return genome
            choice = random.random()       
            # if dey[dex] == "-":                  
            
            if choice < 1.0/3:
                # move right
                swap = dey[to_change_x +1]
                dey[to_change_x +1] = dey[to_change_x]
                dey[to_change_x] = swap
            elif choice < 2.0/3:
                # move left
                swap = dey[to_change_x - 1]
                dey[to_change_x - 1] = dey[to_change_x]
                dey[to_change_x] = swap
                
            else:
                # change block  
                dex =      options[random.randint(1, len(options) - 1)]
                new_item = options[random.randint(1, len(options) - 1)]

                for item in dey:                        #for each item in the row
                    if item == dex:                     #if the item is equal to the random item we want to replace
                        item = new_item                 #replace the item with a new random item
                
                pass

            # options[random.randint(1,len(options) - 1)]
        



            # print("Genome", genome)
            #     if choice < 0.5:         
            #         x = offset_by_upto(x, width / 8, min=1, max=width - 2)     
            #     else:                                            
            #         y = offset_by_upto(y, height / 2, min=0, max=height - 1)   
            #     # else:                                                          
            #         # breakable = not de[3]                                      
            #     new_de = (x, de_type, y)       



            # elif de_type == 'X':

            # elif de_type == '?':

            # elif de_type == 'M':  

            # elif de_type == 'B':

            # elif de_type == 'o':
            
            # elif de_type == '|':    
            
            # elif de_type == 'T':
            
            # elif de_type == 'E':
                                             


        left = 1
        right = width - 1
        for y in range(height):
            for x in range(left, right):
                # if (y == 15):
                #     Individual_Grid.create_pits(genome, x= x, y= y)
                
                # Individual_Grid.pipe(genome, x=x, y=y)
                # Individual_Grid.wall_height(genome, x=x, y=y)
                # Individual_Grid.enemy_spawn(genome, x=x, y=y)
                # Individual_Grid.coin_block_spawn(genome, x=x, y=y)
                pass
        return genome

    # Create zero or more children from self and other
    def generate_children(self, other):
        #print(self.genome, "selfGenome in Grid")
        new_genome = copy.deepcopy(self.genome)
        # print("THing",new_genome)
        # Leaving first and last columns alone...
        # do crossover with other
        left = 1
        right = width - 1
        # inverse so it populates from top to bottom

        not_obstacles = ['-', 'o', 'E']
        
        for y in range(height-1, -1, -1):
            if y < 14:
                new_genome[y][0] = "-"
                new_genome[y][width-2] = "-"
            for x in range(left, right):
                # STUDENT Which one should you take?  Self, or other?  Why?
                # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
                #pick a random parent 
                #if parent 0 is chosen, populate with parent 0 
                #if parent 1 is chosen, populate with parent 1
                
                # if new_genome[y][x] in not_obstacles:
                #     new_genome[y][x] = "-"

                parent = random.randint(0,1)
                if parent == 1:
                    new_genome[y][x] = other.genome[y][x]
                        # Logic for Pit to be crossable
                
                if (y == 15):
                    Individual_Grid.create_pits(new_genome, x= x, y= y)
                
                Individual_Grid.pipe(new_genome, x=x, y=y)
                Individual_Grid.wall_height(new_genome, x=x, y=y)
                Individual_Grid.enemy_spawn(new_genome, x=x, y=y)
                Individual_Grid.coin_block_spawn(new_genome, x=x, y=y)
                Individual_Grid.gaps(new_genome, x=x, y=y)





                # else:
                #     if (y == 15):
                #         Individual_Grid.create_pits(new_genome, x= x, y= y)

                # possible to jump up to walls and or pipes, 4 high, 
                 #      pipes need to have pip bottoms/tops with them
                # if the previous column has ground or wall or pit, the difference in height <= 4

                # ? blocks need to have > 2 space underneath, and distance from ground and block must be <= 4

                # walls at minimum at the bottom, unless Pit introduced(Hole_size)

                #pass
        # do mutation; note we're returning a one-element tuple here
        self.mutate(new_genome)
        return (Individual_Grid(new_genome),)

    def coin_block_spawn(new_genome, x, y):
        non_obs = ['o', '-', 'E']
        if (new_genome[y][x] == "?" or new_genome[y][x] == "M"):
            if y == 14:
                new_genome[y][x] = '-'
            if y < 14:
                if new_genome[y+1][x] not in non_obs or new_genome[y+2][x] not in non_obs:
                    new_genome[y][x] = '-'
            
    def create_pits(new_genome, x, y):
        randNum = random.randint(0,4)
        if randNum < 1:
            if x > 2 and new_genome[y][x-3] == "X":
                new_genome[y][x] = '-'
            else:
                new_genome[y][x] = 'X' 
        else:
            new_genome[y][x] = 'X'  
        
    def enemy_spawn(new_genome, x, y):
        obstacle_list = ['X', '?', 'M', 'B', 'T']
        if y < 15:
            if new_genome[y][x] == 'E':
                if new_genome[y+1][x] not in obstacle_list:
                    new_genome[y][x] = '-'


    def wall_height(new_genome, x, y):
        #check and see if the wall height is 4 or less, otherwise spawn from the list [space, enemy, coin]
        obstacle_list = ['X', '?', 'M', 'B', '|','T'] # list with obstacles wall, question block, mushroom block, Breakable block, pipe seg, pipe top
        pipe_list = ['|', 'T'] #list containing pip parts
        if x < 1:
            return
        if(y < 13): # checks if its even possible to be > 4
            for i in range(1,3): 
                if new_genome[y+i][x-1] not in obstacle_list:
                    if new_genome[y+i][x-2] not in pipe_list:
                        return
        else:
            return
        
        new_genome[y][x] = "-"


        # if not, check if the previous column is completely empty up until that height,
            #if yes, check if the there is an obstacle at the same height or higher than the wall height being created

    def gaps(new_genome, x, y):
        #make sure if there is a gap under an obstacle, there needs to be 2 gaps under it
        
        non_obs = ['o', '-', 'E']
        if (new_genome[y][x] == "X" or new_genome[y][x] == "B"):
            
            if y < 14:
                if new_genome[y+1][x] in non_obs and new_genome[y+2][x] not in non_obs:
                    new_genome[y][x] = '-'
                    new_genome[y+2][x] = '-'
                    new_genome[y+1][x+1] = '-'
                    new_genome[y+2][x+1] = '-'
                    new_genome[y+1][x-1] = '-'
                    new_genome[y+2][x-1] = '-'
                # if new_genome[y+1][x+1] in non_obs and new_genome[y+2][x+1] not in non_obs:
                #     new_genome[y][x] = '-'
                # if new_genome[y+1][x-1] in non_obs and new_genome[y+2][x-1] not in non_obs:
                #     new_genome[y][x] = '-'

    def pipe(new_genome, x, y):
        # make the pipe full
        

        if y > 14:
            return
        if new_genome[y][x] != 'T' and new_genome[y][x] != '|':
            if new_genome[y+1][x] == "|":
                new_genome[y][x] = 'T'


        elif(new_genome[y][x] == "T"): 
            if new_genome[y][x+1] != '-':
                new_genome[y][x+1] = '-'
            if new_genome[y+1][x] == "|":
                return
            new_genome[y][x] = '-'

        elif new_genome[y][x] == "|":
            if new_genome[y][x+1] != '-':
                new_genome[y][x+1] = '-'
            if new_genome[y+1][x] == "|":
                return
            elif new_genome[y+1][x] == "X" and new_genome[y+1][x+1] == "X":    
                return
            
            new_genome[y][x] = '-'
    # Turn the genome into a level string (easy for this genome)
    def to_level(self):
        return self.genome

    # These both start with every floor tile filled with Xs
    # STUDENT Feel free to change these
    @classmethod
    def empty_individual(cls):
        g = [["-" for col in range(width)] for row in range(height)]
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        for col in range(8, 14):
            g[col][-1] = "f"
        for col in range(14, 16):
            g[col][-1] = "X"
        return cls(g)

    @classmethod
    def random_individual(cls):
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        g = [random.choices(options, k=width) for row in range(height)]
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        g[8:14][-1] = ["f"] * 6
        g[14:16][-1] = ["X", "X"]
        return cls(g)







def offset_by_upto(val, variance, min=None, max=None):
    val += random.normalvariate(0, variance**0.5)
    if min is not None and val < min:
        val = min
    if max is not None and val > max:
        val = max
    return int(val)


def clip(lo, val, hi):
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val

# Inspired by https://www.researchgate.net/profile/Philippe_Pasquier/publication/220867545_Towards_a_Generic_Framework_for_Automated_Video_Game_Level_Creation/links/0912f510ac2bed57d1000000.pdf


class Individual_DE(object):
    # Calculating the level isn't cheap either so we cache it too.
    __slots__ = ["genome", "_fitness", "_level"]

    # Genome is a heapq of design elements sorted by X, then type, then other parameters
    def __init__(self, genome):
        self.genome = list(genome)
        heapq.heapify(self.genome)
        self._fitness = None
        self._level = None

    # Calculate and cache fitness
    def calculate_fitness(self):
        measurements = metrics.metrics(self.to_level())
        # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
        # STUDENT Add more metrics?
        # STUDENT Improve this with any code you like
        coefficients = dict(
            meaningfulJumpVariance=1.0,
            negativeSpace=0.1,
            pathPercentage=0.7,
            emptyPercentage=0.3,
            linearity=-0.6,
            solvability=6.0,
            decorationPercentage = 2.0,
            meaningfulJumps = 7,

        )
        penalties = 0
        # STUDENT For example, too many stairs are unaesthetic.  Let's penalize that
        if len(list(filter(lambda de: de[1] == "6_stairs", self.genome))) > 5:
            penalties -= 2
        # STUDENT If you go for the FI-2POP extra credit, you can put constraint calculation in here too and cache it in a new entry in __slots__.
        self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                                coefficients)) + penalties
        return self

    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        return self._fitness

    def mutate(self, new_genome):
        # STUDENT How does this work?  Explain it in your writeup.
        # STUDENT consider putting more constraints on this, to prevent generating weird things
        if random.random() < 0.15 and len(new_genome) > 0:                           #if a random number at 10% to mutate: and the length of the new genome is greater than 0
            to_change = random.randint(0, len(new_genome) - 1)                      #assign a random integer from 0 to the length of the new genome list minus 1
            de = new_genome[to_change]                                              # de = the genome to change
            new_de = de                                                             # set the new_de to the de
            x = de[0]                                                               # set x to the first element of the de list
            de_type = de[1]                                                         # set de_type to the second element of the de list
            choice = random.random()                                                # set choice to a random number
            if de_type == "4_block":                                                # id the type of de_type is a 4_block
                y = de[2]                                                           # set y to the 3rd element of de
                breakable = de[3]                                                   # set breakable to the 4th element of de
                if choice < 0.33:                                                   # if the choice number is less than .33
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)          #set x to the return of the offset_by_upto function
                elif choice < 0.66:                                                 #else if the choice is less than 66%
                    y = offset_by_upto(y, height / 2, min=0, max=height - 1)        #set y to the return of the offset_by_upto function
                else:                                                               #else
                    breakable = not de[3]                                           #set breakable to not the 4th element of de
                new_de = (x, de_type, y, breakable)                                 #set the new_de to x, de_type, y, and breakable
            elif de_type == "5_qblock":
                y = de[2]
                has_powerup = de[3]  # boolean
                if choice < 0.33:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.66:
                    y = offset_by_upto(y, height / 2, min=0, max=height - 1)
                else:
                    has_powerup = not de[3]
                new_de = (x, de_type, y, has_powerup)
            elif de_type == "3_coin":
                y = de[2]
                if choice < 0.5:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                else:
                    y = offset_by_upto(y, height / 2, min=0, max=height - 1)
                new_de = (x, de_type, y)
            elif de_type == "7_pipe":
                h = de[2]
                if choice < 0.5:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                else:
                    h = offset_by_upto(h, 2, min=2, max=height - 4)
                new_de = (x, de_type, h)
            elif de_type == "0_hole":
                w = de[2]
                if choice < 0.5:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                else:
                    w = offset_by_upto(w, 4, min=1, max=width - 2)
                new_de = (x, de_type, w)
            elif de_type == "6_stairs":
                h = de[2]
                dx = de[3]  # -1 or 1
                if choice < 0.33:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.66:
                    h = offset_by_upto(h, 8, min=1, max=height - 4)
                else:
                    dx = -dx
                new_de = (x, de_type, h, dx)
            elif de_type == "1_platform":
                w = de[2]
                y = de[3]
                madeof = de[4]  # from "?", "X", "B"
                if choice < 0.25:
                    x = offset_by_upto(x, width / 8, min=1, max=width - 2)
                elif choice < 0.5:
                    w = offset_by_upto(w, 8, min=1, max=width - 2)
                elif choice < 0.75:
                    y = offset_by_upto(y, height, min=0, max=height - 1)
                else:
                    madeof = random.choice(["?", "X", "B"])
                new_de = (x, de_type, w, y, madeof)
            elif de_type == "2_enemy":
                pass
            new_genome.pop(to_change)                                           #pops off the piece you want to change
            heapq.heappush(new_genome, new_de)                                  #pushes the new piece onto the genome
        return new_genome                                                       #returns the new genome

    def generate_children(self, other):
        # STUDENT How does this work?  Explain it in your writeup.
        #print(self.genome, "selfGenome in Individual")
        pa = random.randint(0, len(self.genome) - 1)                #get a random integer index from the first genome     
        pb = random.randint(0, len(other.genome) - 1)               #get a random integer index from the second genome
        a_part = self.genome[:pa] if len(self.genome) > 0 else []   #set a_part as list to the index ap of self genome if its longer than 0 else set to empty list
        b_part = other.genome[pb:] if len(other.genome) > 0 else [] #set b_part as list from the index bp to end of second genome if it is longer than 0, else set to empty list
        ga = a_part + b_part                                        #add apart and bpart together
        b_part = other.genome[:pb] if len(other.genome) > 0 else [] #set b_part as list to the index of pb of second genome if it longer than 0, else set to list
        a_part = self.genome[pa:] if len(self.genome) > 0 else []   #set a_part as list from index ap to end of self genom if it is longer than 0, else set to empty list
        gb = b_part + a_part                                        # add apart and bpart together
        # do mutation
        return Individual_DE(self.mutate(ga)), Individual_DE(self.mutate(gb))  #create a individuals by calling mutation on list in ga and list in gb

    # Apply the DEs to a base level.
    def to_level(self):
        if self._level is None:
            base = Individual_Grid.empty_individual().to_level()
            for de in sorted(self.genome, key=lambda de: (de[1], de[0], de)):
                # de: x, type, ...
                x = de[0]
                de_type = de[1]
                if de_type == "4_block":
                    y = de[2]
                    breakable = de[3]
                    base[y][x] = "B" if breakable else "X"
                elif de_type == "5_qblock":
                    y = de[2]
                    has_powerup = de[3]  # boolean
                    base[y][x] = "M" if has_powerup else "?"
                elif de_type == "3_coin":
                    y = de[2]
                    base[y][x] = "o"
                elif de_type == "7_pipe":
                    h = de[2]
                    base[height - h - 1][x] = "T"
                    for y in range(height - h, height):
                        base[y][x] = "|"
                elif de_type == "0_hole":
                    w = de[2]
                    for x2 in range(w):
                        base[height - 1][clip(1, x + x2, width - 2)] = "-"
                elif de_type == "6_stairs":
                    h = de[2]
                    dx = de[3]  # -1 or 1
                    for x2 in range(1, h + 1):
                        for y in range(x2 if dx == 1 else h - x2):
                            base[clip(0, height - y - 1, height - 1)][clip(1, x + x2, width - 2)] = "X"
                elif de_type == "1_platform":
                    w = de[2]
                    h = de[3]
                    madeof = de[4]  # from "?", "X", "B"
                    for x2 in range(w):
                        base[clip(0, height - h - 1, height - 1)][clip(1, x + x2, width - 2)] = madeof
                elif de_type == "2_enemy":
                    base[height - 2][x] = "E"
            self._level = base
        return self._level

    @classmethod
    def empty_individual(_cls):
        # STUDENT Maybe enhance this
        g = []
        return Individual_DE(g)

    @classmethod
    def random_individual(_cls):
        # STUDENT Maybe enhance this
        elt_count = random.randint(8, 128)
        g = [random.choice([
            (random.randint(1, width - 2), "0_hole", random.randint(1, 8)),
            (random.randint(1, width - 2), "1_platform", random.randint(1, 8), random.randint(0, height - 1), random.choice(["?", "X", "B"])),
            (random.randint(1, width - 2), "2_enemy"),
            (random.randint(1, width - 2), "3_coin", random.randint(0, height - 1)),
            (random.randint(1, width - 2), "4_block", random.randint(0, height - 1), random.choice([True, False])),
            (random.randint(1, width - 2), "5_qblock", random.randint(0, height - 1), random.choice([True, False])),
            (random.randint(1, width - 2), "6_stairs", random.randint(1, height - 4), random.choice([-1, 1])),
            (random.randint(1, width - 2), "7_pipe", random.randint(2, height - 4))
        ]) for i in range(elt_count)]
        return Individual_DE(g)


# Individual = Individual_Grid
Individual = Individual_DE


def generate_successors(population):
    results = []
    # STUDENT Design and implement this
    # Hint: Call generate_children() on some individuals and fill up results.
    # print("------------------",population)

    
    
    

    sorted_population = sorted(population, key=lambda individual: individual.fitness(), reverse=True)

    # for i in range(0, len(population)-1, 2):
    # Elitests: using the top2 that havent been used in generation yet.
    child1 = Individual.generate_children(sorted_population[0], sorted_population[1])
    

    if child1[0].fitness() > sorted_population[0].fitness():
        results += child1
    
    elif child1[0].fitness() > sorted_population[1].fitness():
        results += child1
    else:
        results += (sorted_population[0],)

    # Roulette
    choice1 = random.randint(0, len(population) - 1)
    choice2 = random.randint(0, len(population) - 1)
    child2 = Individual.generate_children(sorted_population[choice1], sorted_population[choice2])
    
    results += child2

    
    # print("Results: ", results)
    # Individual_DE.generate_children)
    return results


def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 480
    # Code to parallelize some computations
    batches = os.cpu_count()
    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))
    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()
        # STUDENT (Optional) change population initialization

       
        population = [Individual.random_individual() if random.random() < 0.9
                      else Individual.empty_individual()
                      for _g in range(pop_limit)]
        # print("Population1", population)
        # But leave this line alone; we have to reassign to population because we get a new population that has more cached stuff in it.
        population = pool.map(Individual.calculate_fitness,
                              population,
                              batch_size)

        init_done = time.time()
        print("Created and calculated initial population statistics in:", init_done - init_time, "seconds")
        generation = 0
        start = time.time()
        now = start
        print("Use ctrl-c to terminate this loop manually.")
        try:
            while True:
                now = time.time()
                # Print out statistics
                if generation > 0:
                    # print("pop", population)
                    best = max(population, key=Individual.fitness)
                    print("Generation:", str(generation))
                    print("Max fitness:", str(best.fitness()))
                    print("Average generation time:", (now - start) / generation)
                    print("Net time:", now - start)
                    with open("levels/last.txt", 'w') as f:
                        for row in best.to_level():
                            f.write("".join(row) + "\n")
                generation += 1
                # STUDENT Determine stopping condition
                stop_condition = False
                
                if generation > 10:
                    stop_condition = True
                    
                if stop_condition:
                    break
                # STUDENT Also consider using FI-2POP as in the Sorenson & Pasquier paper
                gentime = time.time()
                next_population = generate_successors(population)
                gendone = time.time()
                print("Generated successors in:", gendone - gentime, "seconds")
                # Calculate fitness in batches in parallel
                next_population = pool.map(Individual.calculate_fitness,
                                           next_population,
                                           batch_size)
                popdone = time.time()
                print("Calculated fitnesses in:", popdone - gendone, "seconds")
                population = next_population
        except KeyboardInterrupt:
            pass
    return population


if __name__ == "__main__":
    final_gen = sorted(ga(), key=Individual.fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness: " + str(best.fitness()))
    now = time.strftime("%m_%d_%H_%M_%S")
    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...
    # for k in range(0, 10):
    #     with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
    #         for row in final_gen[k].to_level():
    #             f.write("".join(row) + "\n")
