#!/usr/bin/env python

import rvo2
import matplotlib.pyplot as plt
import math
import threading
import random

class Py_RVO():

    def __init__(self,radius, num_agents) -> None:
        self.sim = rvo2.PyRVOSimulator(1/60., 1.5, 5, 1.5, 2, 0.4, 2)
        self.goals = []
        self.flag = 0
        self.radius = radius
        self.new_agents_x = []
        self.new_agents_y = []
        self.colors = []
        self.update = False
        # self.colors = ['red','orange','blue','pink']
        # self.createAgent()
        self.agents = []
        self.createAgents(r=self.radius,num=num_agents)
        plt.figure(figsize=(8,8))
        self.obstacle_vertices = [(0.0,0.0),(0.0,2.0),(-2.0,2.0),(-2.0,0.0)]
        self.createObstacle(self.obstacle_vertices)

        # self.createObstacle()
    


# Pass either just the position (the other parameters then use
# the default values passed to the PyRVOSimulator constructor),
# or pass all available parameters.
    def createAgent(self,pos,goal):
        a0 = self.sim.addAgent(pos)
        self.agents.extend([a0])
        self.goals.extend([goal])
        self.colors.extend(['black'])
        self.update = True

    def addGoals(self,r,num):
        pi = math.pi
        for p in range(0,num):
            x = math.cos((2*pi/num*p) - pi)*r
            y = math.sin((2*pi/num*p) - pi)*r
            self.goals.extend([(x,y)])

    def createAgents(self,r,num):
        pi = math.pi
        rand = random.randint(0,num)
        for p in range(0,num):
            x = math.cos(2*pi/num*p)*r
            y = math.sin(2*pi/num*p)*r
            if p == rand:
                x += 0.1
                y += 0.2
            self.new_agents_x.extend([x])
            self.new_agents_y.extend([y])
            self.agents.extend([self.sim.addAgent((x,y))])
            self.colors.extend(['black'])
        
        self.addGoals(r=r,num=num)
        self.new_agents_x = []
        self.new_agents_y = []
        


    def createObstacle(self,pos):
        # Obstacles are also supported.
        o1 = self.sim.addObstacle(pos)
        self.sim.processObstacles()

    def setPrefVelocity(self):
        for agent,goal in zip(self.agents,self.goals):
            pos = self.sim.getAgentPosition(agent)
            vel = ((goal[0]-pos[0])*2 ,(goal[1]-pos[1])*2)
            if abs(vel[0]) <= 0.2 and abs(vel[1]) <= 0.2 :
                vel = (0,0)
            elif abs(vel[0]) < 1 and abs(vel[1]) < 1 :
                vel = (vel[0]*2,vel[1]*2)
            self.sim.setAgentPrefVelocity(agent,vel)
        

    def reachedGoal(self):
        count = 1
        for agent,goal in zip(self.agents,self.goals):
            pos = self.sim.getAgentPosition(agent)
            if abs(pos[0]-goal[0]) > 0.2 and abs(pos[1]-goal[1]) > 0.2:
                count = 0
        return count
    
    def run(self):
        print('Simulation has %i agents and %i obstacle vertices in it.' %
            (self.sim.getNumAgents(), self.sim.getNumObstacleVertices()))
        once = True
        while self.flag < 1:
            self.sim.doStep()
            self.setPrefVelocity()
            positions = [self.sim.getAgentPosition(agent_no)
                       for agent_no in self.agents]
#           print('step=%2i  t=%.3f  %s' % (step, sim.getGlobalTime(), '  '.join(positions)))

            x_vals = []
            y_vals = []
            for pose in positions:
                x_vals.extend([pose[0]])
                y_vals.extend([pose[1]])
            # sc.set_offsets(x_vals,y_vals)
            for x,y in self.obstacle_vertices:
                x_vals.extend([x])
                y_vals.extend([y])
                if once:
                    self.colors.extend(['red'])
            once = False

            plt.pause(0.1)
            plt.clf()  # Clear plot for the next frame
            # plt.figure(figsize=(self.radius+2,self.radius+2))
            plt.xlim((-(self.radius+2),self.radius+2))
            plt.ylim((-(self.radius+2),self.radius+2))
            if self.update:
                self.update = False
                continue
            plt.scatter(x_vals, y_vals,c=self.colors)

            plt.show(block=False)
            self.flag = self.reachedGoal()
        print("All Agents reached their goal successfully")

# def main():
    # agents = int(input("Number Of Agents: "))
    # radius = float(input("Enter radius of circle such that it can easily accomodate the agents: "))
    # obj = Py_RVO(radius=radius,num_agents=agents)
    # obj.run()

class Addition():
    def __init__(self,py_rvo):
        self.sim = py_rvo
        pass
    
    def run(self):
        # ask_obstacle = int(input("Want to add obstacles ?"))
        # if ask_obstacle:
        #     loc = tuple(map(float, input("Enter X and Y position of Obstacle: ").strip().split()))
        #     self.sim.createObstacle(loc)
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
    py_rvo = Py_RVO(radius=radius,num_agents=agents)
    obstacle = Addition(py_rvo)

    # thread_1 = threading.Thread(target=py_rvo.run)
    thread_2 = threading.Thread(target=obstacle.run)

    # thread_1.start()
    thread_2.start()

    # thread_1.join()
    py_rvo.run()

if __name__ == "__main__":
    main()


