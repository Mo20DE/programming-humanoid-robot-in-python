'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent

from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from time import time
import json


class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def __init__(self):
        super(ServerAgent, self).__init__()
        self.server = SimpleXMLRPCServer(("localhost", 8000))

        methods = ["get_angle", "set_angle", "get_posture", "execute_keyframes", "get_transform", "set_transform"]
        for method in methods:
            exec(f"self.server.register_function(self.{method}, \"{method}\")")

        thr = Thread(target=self.server.serve_forever)
        thr.start()
        print("Started ServerAgent on port 8000.")
    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.perception.joint[joint_name]
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.target_joints[joint_name] = angle
        return True

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.posture

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.passed_time = time()
        self.keyframes = keyframes
        _max = 0
        for times in self.keyframes[1]:
            curr = times[-1]
            if curr > _max:
                _max = curr
        
        # blocking (not nice but it's working)
        done = False
        while not done:
            current_time = time() - self.passed_time
            if current_time > _max:
                done = True
        
        return True

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return json.dumps(self.transforms[name].tolist())

    # didn't implement the inverse kinematics functions
    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.target_joints = self.inverse_kinematics(effector_name, json.loads(transform))
        return True

if __name__ == '__main__':

    agent = ServerAgent()
    agent.run()

