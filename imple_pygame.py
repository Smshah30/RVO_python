#!/usr/bin/env python

import rvo2
import matplotlib.pyplot as plt
import math
import threading
import random
import pygame
import time 

class Py_RVO():

    def __init__(self,radius, num_agents,obstacle,distribution) -> None:
        self.sim = rvo2.PyRVOSimulator(1/60.0, 1.5, 5, 4.0, 3.0, 0.4, 2)
        self.goals = []
        self.flag = 0
        self.num_agents = num_agents
        self.new_agents_x = []
        self.new_agents_y = []
        self.update = False
        self.agents = []
        self.show_obstacle = obstacle
        self.createAgents(r=radius,num=num_agents,distribution=distribution)
        # Static Obstacle 
        if self.show_obstacle:
            self.obstacle_vertices = [[(2.0,0.75),(2.0,2.0),(-2.0,2.0),(-2.0,0.75)],[(-0.75,-2.0),(-0.75,-0.75),(-2.0,-0.75),(-2.0,-2.0)],[(2.0,-2.0),(2.0,-0.75),(0.75,-0.75),(0.75,-2.0)] ]                           # Obstacle setup for Narrow
            # self.obstacle_vertices = [[(2.0,1.0),(2.0,2.0),(1.0,2.0),(1.0,1.0)],[(-1.0,1.0),(-1.0,2.0),(-2.0,2.0),(-2.0,1.0)],[(-1.0,-2.0),(-1.0,-1.0),(-2.0,-1.0),(-2.0,-2.0)],[(2.0,-2.0),(2.0,-1.0),(1.0,-1.0),(1.0,-2.0)] ]   # 4 obstacles in a plus setup 
            
            for i in self.obstacle_vertices:
                self.createObstacle(i)
    


# Pass either just the position (the other parameters then use
# the default values passed to the PyRVOSimulator constructor),
# or pass all available parameters.

    def createAgent(self,pos,goal):
        a0 = self.sim.addAgent(pos)
        self.agents.extend([a0])
        self.goals.extend([goal])
        self.update = True
        self.num_agents +=1

    def addGoals(self,r,num):
        pi = math.pi
        for p in range(0,num):
            x = math.cos((2*pi/num*p) - pi)*r
            y = math.sin((2*pi/num*p) - pi)*r
            self.goals.extend([(x,y)])

    def createAgents(self,r,num,distribution):
        pi = math.pi
        rand = random.randint(0,num)
        for p in range(0,num):
            if distribution:
                x = random.uniform(-r,r)
                y = random.uniform(-r,r)
            else:
                x = math.cos(2*pi/num*p)*r
                y = math.sin(2*pi/num*p)*r            
            if p == rand:
                x += 0.1
                y += 0.2
            self.new_agents_x.extend([x])
            self.new_agents_y.extend([y])
            self.agents.extend([self.sim.addAgent((x,y))])
        
        self.addGoals(r=r,num=num)
        self.new_agents_x = []
        self.new_agents_y = []
        


    def createObstacle(self,pos):
        # Obstacles are also supported.
        o1 = self.sim.addObstacle(pos)
        self.sim.processObstacles()

    def setPrefVelocity(self):
        ''' Preferred velocity in the direction of goal
        '''
        for agent,goal in zip(self.agents,self.goals):
            pos = self.sim.getAgentPosition(agent)
            vel = ((goal[0]-pos[0])*2 ,(goal[1]-pos[1])*2)
            if abs(vel[0]) <= 0.2 and abs(vel[1]) <= 0.2 :
                vel = (0,0)
            elif abs(vel[0]) < 1 and abs(vel[1]) < 1 :
                vel = (vel[0]*2,vel[1]*2)
            self.sim.setAgentPrefVelocity(agent,vel)
        

    def reachedGoal(self): 
        ''' Checks how many reached goal
        '''
        count = 1
        reached = self.num_agents
        for agent,goal in zip(self.agents,self.goals):
            pos = self.sim.getAgentPosition(agent)
            if abs(pos[0]-goal[0]) > 0.1 or abs(pos[1]-goal[1]) > 0.1:
                count = 0
                reached -= 1
        return (count,reached)
    
    def draw_text(self,text,screen,text2):
            '''
                Display the count of robots reached goal and scale
               '''
            text_font = pygame.font.SysFont(None,30)
            img2 = text_font.render(text2,True,(255,255,255))
            screen.blit(img2,(1000,130))
            if text == "Done":
                text_font = pygame.font.SysFont(None,100)
                img = text_font.render("",True,(255,255,255))
                screen.blit(img,(550,500))
            else:
                img = text_font.render(text,True,(255,255,255))
                screen.blit(img,(1000,100))


    
    def run(self):
        print('Simulation has %i agents and %i obstacle vertices in it.' %
            (self.sim.getNumAgents(), self.sim.getNumObstacleVertices()))
        
        # Display Parameters
        pygame.init()
        SCREEN_WIDTH = 1400
        SCREEN_HEIGHT = 1000
        ZOOM_FACTOR = 1.1

        # Scaling Factors to improve Agents Visualization
        if self.num_agents<= 50:
            zoom_level = 20.0
            radius = 5.0
        elif self.num_agents <= 100:
            zoom_level = 4.0
            radius = 2.0
        elif self.num_agents <= 200:
            zoom_level = 2.0
            radius = 1.5
        else:
            zoom_level = 1.0
            radius = 1.0

        screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # Initialize Screen

        path_print_flag = 0 # Whether to print path of not and how often 

        cmap = plt.get_cmap('gist_rainbow')   # Select unique colors for each agents
        followed_path = []                    # Stores Path followed by each agent
        
        
        while self.flag < 1:
            screen.fill((0,0,0))            # Make screen Black

            self.sim.doStep()
            self.setPrefVelocity()
            positions = [self.sim.getAgentPosition(agent_no)
                        for agent_no in self.agents]

            x_vals = []
            y_vals = []
            n = len(positions)
            for pose,x in zip(positions,range(n)):
                i = cmap(x)
                color = (math.floor(i[0]*255),math.floor(i[1]*255),math.floor(i[2]*255))
                pos_x = SCREEN_WIDTH/2 + (pose[0] * zoom_level)
                pos_y = SCREEN_HEIGHT/2 - (pose[1] * zoom_level)
                pygame.draw.circle(screen,color,center=(pos_x,pos_y),radius=radius)
                x_vals.extend([pose[0]])
                y_vals.extend([pose[1]])
               
                if self.num_agents <=50 and path_print_flag % 15 == 0:
                    path_print_flag = 0
                    element = [pos_x,pos_y,color]
                    followed_path.extend([element])
                


            path_print_flag +=1

            for point in followed_path:
                pygame.draw.circle(screen,point[2],center=(point[0],point[1]),radius=1.0)

            if self.show_obstacle:
                for points in self.obstacle_vertices:
                    left_top = points[2]
                    right_bottom = points[0]
                    left_bottom = points[3]
                    player = pygame.Rect((SCREEN_WIDTH/2 + (left_top[0] * zoom_level)),(SCREEN_HEIGHT/2 - (left_top[1] * zoom_level)),(abs(left_top[0]-right_bottom[0])* zoom_level),(abs(left_top[1]-right_bottom[1])*zoom_level))
                    pygame.draw.rect(screen,(255,255,255),player)

                

            # time.sleep(0.05)     # Only to be used for 1/10 Timestep or greater

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.flag = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Zoom in
                        zoom_level *= ZOOM_FACTOR
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Zoom out
                        zoom_level /= ZOOM_FACTOR

            if self.update:
                self.update = False
                continue

            val = self.reachedGoal()
            self.flag = val[0]
            if val[1] == self.num_agents:
                text = "Done"
            else:
                text = f"Reached Goal: {val[1]} / {self.num_agents}"
            text2 = f"Scale: {round(zoom_level,3)}"
            self.draw_text(text=text,screen=screen,text2=text2)
            pygame.display.update()

        time.sleep(3)
        pygame.quit()
        print("All Agents reached their goal successfully")


class AddAgents():
    def __init__(self,py_rvo):
        self.sim = py_rvo
        pass
    
    def run(self):
        time.sleep(2)

        ask_agent = int(input("Do you want to add agents? "))
        if ask_agent:
            number = int(input("How many agents: "))
            for i in range(number):
                pos =tuple(map(float, input("Position of Agent: ").strip().split()))
                goal = tuple(map(float, input("Goal of Agent: ").strip().split()))
                self.sim.createAgent(pos,goal)

def main():
    agents = int(input("Number Of Agents: "))
    radius = float(input("Enter radius of circle such that it can easily accomodate the agents: "))
    obstacle = int(input("Do you want obstacles(not recommended for agents > 100)? Enter 1(Yes) or 0(No): "))
    distribution = int(input("Enter 1 for random initialization of agents and 0 for initialization in a circle: "))
    py_rvo = Py_RVO(radius=radius,num_agents=agents,obstacle=obstacle,distribution=distribution)
    add_new_agents = AddAgents(py_rvo)

    seperate_thread = threading.Thread(target=add_new_agents.run)
    seperate_thread.start()

    py_rvo.run()

if __name__ == "__main__":
    main()


