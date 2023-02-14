from src.brain import Brain
from src.options import *
from src.map import Map


class User:
    
    def __init__(self, name):
        self.action = ''
        self.brain = Brain()
        self.direction = DIRECTION_UP
        self.health = MAX_USER_HEALTH
        self.inventory = []
        self.name = name
        self.position = [-1, -1]
    
    def get_position(self):
        return self.position
    
    def has(self, quantity, char):
        return self.inventory.count(char) == quantity
    
    def to_inventory(self, char):
        self.inventory.append(char)
    
    def is_dead(self):
        return self.health <= 0
    
    def see(self, map):
        return map.get_in_direction(self.position[0], self.position[1], self.direction)
    
    def place_on(self, map: Map):
        x, y = self.position = map.get_empty_random_position()
        self.position = [x, y]
        map.put(x, y, USER)
    
    def show_info(self, map: Map):
        print(f"В вашем инвентаре {self.inventory.count(TREASURE)} сокровищ")
        knowledge_about = self.brain.recognize(self.see(map))
        # can_do = self.can_do_action(self.see(map))
        print(knowledge_about.message())
        direction = ','.join(self.can_walk_to(self.direction, knowledge_about))
        self.action = input(
            f"Идти в направлении [{direction}] или [{'.'.join(knowledge_about.can_do())}]: ")

    @staticmethod
    def can_walk_to(direction, knowledge_about):
        directions = [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]
        if knowledge_about.it_barier():
            directions.remove(direction)
        
        return directions

    def do(self, map, knowledge_about):
        pass
    
    def move(self):
        pass
    

