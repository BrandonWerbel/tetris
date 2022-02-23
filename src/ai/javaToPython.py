from py4j.java_gateway import JavaGateway

import numpy
from numpy import array

import time

class JavaToPython():

    def __init__(self, gateway):
        self.gateway = gateway
        self.tetris_game = self.gateway.jvm.tetris.TetrisDriver()
        self.actions_obj = self.tetris_game.getActionsObject()
        self.tetris_UI = self.tetris_game.getGameUI()
        self.terminal = self.gateway.jvm.System.out

    def get_python_wall(self):
        wall = self.tetris_UI.getWall()
        self.terminal.println("J2P")
        byteArray = self.tetris_UI.getByteArray(wall)
        self.terminal.println("got bytes")
        intArray = numpy.frombuffer(byteArray, dtype=numpy.int32)
        self.terminal.println("bytes to ints")
        print(self.tetris_UI.getWidth())
        finalArray = numpy.reshape(intArray, (self.tetris_UI.getGameWidth(), self.tetris_UI.getGameHeight() - 1))
        self.terminal.println("2d array")
        return finalArray
    
    def get_episode_over(self):
        return self.tetris_UI.getEpisodeOver()

    def restart(self):
        self.tetris_UI.newEpisode()
        
    def get_reward(self):
        if self.tetris_UI.getDeltaScore() != 0:
            return self.tetris_UI.getDeltaScore() / 200
        else:
            return 0.05
    
    def just_collided(self):
        if self.tetris_UI.getColliding():
            self.tetris_UI.stopColliding()
            return True
        else:
            self.actions_obj.dropDown()
            return False

    def go_to_location(self, x_pos, rotation):
        self.terminal.println("hello from java talker")
        while self.tetris_UI.getRotation() is not rotation:
            if self.tetris_UI.getRotation() - rotation < 0:
                self.actions_obj.rotateClockwise()
            else:
                self.actions_obj.rotateCounterClockwise()
            time.sleep(0.1)
        
        while self.tetris_UI.getX() != x_pos:
            if self.tetris_UI.getX() > x_pos:
                self.actions_obj.moveLeft()
            else:
                self.actions_obj.moveRight()
            time.sleep(0.1)

