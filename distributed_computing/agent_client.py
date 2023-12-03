'''In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
'''

import weakref
from threading import Thread

from xmlrpc.client import ServerProxy, Error
from keyframes import hello, wipe_forehead

class PostHandler(object):
    '''the post handler wraps function to be excuted in paralle
    '''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def execute_keyframes(self, keyframes):
        '''non-blocking call of ClientAgent.execute_keyframes'''
        # YOUR CODE HERE
        thread = Thread(target=self.proxy.execute_keyframes, args=(keyframes,))
        thread.start()

    def set_transform(self, effector_name, transform):
        '''non-blocking call of ClientAgent.set_transform'''
        # YOUR CODE HERE
        thread = Thread(target=self.proxy.set_keyframeset_transform, args=(effector_name, transform))
        thread.start()

class ClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self):
        self.post = PostHandler(self)
        self.rpc_server = ServerProxy("http://localhost:8000/")

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        try:
            return self.rpc_server.get_angle(joint_name)
        except Error as e:
            print("Error occurred: ", e)
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        try:
            return self.rpc_server.set_angle(joint_name, angle)
        except Error as e:
            print("Error occurred: ", e)

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        try:
            return self.rpc_server.get_posture()
        except Error as e:
            print("Error occurred: ", e)

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        try:
            return self.rpc_server.execute_keyframes(keyframes)
        except Error as e:
            print("Error occurred: ", e)

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        try:
            return self.rpc_server.get_transform(name)
        except Error as e:
            print("Error occurred: ", e)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        try:
            return self.rpc_server.set_transform(effector_name, transform)
        except Error as e:
            print("Error occurred: ", e)

if __name__ == '__main__':
    agent = ClientAgent()
    # TEST CODE HERE

    print(agent.get_angle("HeadYaw"))
    agent.set_angle("HeadYaw", 1)
    print(agent.get_angle("HeadYaw"))

    print(agent.get_posture())

    key1 = agent.post.execute_keyframes(hello())
    print("Hello world")
    print(key1)

    import time
    time.sleep(10)
    key2 = agent.post.execute_keyframes(wipe_forehead(None))
    print(key2)

