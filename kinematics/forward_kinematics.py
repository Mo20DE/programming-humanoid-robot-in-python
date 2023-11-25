'''In this exercise you need to implement forward kinematics for NAO robot

* Tasks:
    1. complete the kinematics chain definition (self.chains in class ForwardKinematicsAgent)
       The documentation from Aldebaran is here:
       http://doc.aldebaran.com/2-1/family/robots/bodyparts.html#effector-chain
    2. implement the calculation of local transformation for one joint in function
       ForwardKinematicsAgent.local_trans. The necessary documentation are:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    3. complete function ForwardKinematicsAgent.forward_kinematics, save the transforms of all body parts in torso
       coordinate into self.transforms of class ForwardKinematicsAgent

* Hints:
    1. the local_trans has to consider different joint axes and link parameters for different joints
    2. Please use radians and meters as unit.
'''

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))

from numpy.matlib import matrix, identity
import numpy as np

from recognize_posture import PostureRecognitionAgent


class ForwardKinematicsAgent(PostureRecognitionAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(ForwardKinematicsAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.transforms = {n: identity(4) for n in self.joint_names}

        # chains defines the name of chain and joints of the chain
        self.chains = {'Head': ['HeadYaw', 'HeadPitch'],
                       # YOUR CODE HERE
                       'LArm': ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'],
                       'RArm': ['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'],
                       'LLeg': ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'],
                       'RLeg': ['RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll']
                    }
        self.lengths = {
            # head
            'HeadYaw': 0,
            'HeadPitch': 0,
            # left arm
            'LShoulderPitch': 0,
            'LShoulderRoll': 0,
            'LElbowYaw': 0.105,
            'LElbowRoll': 0,
            # right arm
            'RShoulderPitch': 0,
            'RShoulderRoll': 0,
            'RElbowYaw': 0.105,
            'RElbowRoll': 0,
            # left leg
            'LHipYawPitch': 0, 
            'LHipRoll': 0, 
            'LHipPitch': 0, 
            'LKneePitch': -0.1, 
            'LAnklePitch': -0.129, 
            'LAnkleRoll': 0,
            # right leg
            'RHipYawPitch': 0, 
            'RHipRoll': 0, 
            'RHipPitch': 0, 
            'RKneePitch': -0.1, 
            'RAnklePitch': -0.129, 
            'RAnkleRoll': 0
        }

    def think(self, perception):
        self.forward_kinematics(perception.joint)
        return super(ForwardKinematicsAgent, self).think(perception)

    def local_trans(self, joint_name, joint_angle):
        '''calculate local transformation of one joint

        :param str joint_name: the name of joint
        :param float joint_angle: the angle of joint in radians
        :return: transformation
        :rtype: 4x4 matrix
        '''
        T = identity(4)
        # YOUR CODE HERE

        s, c = np.sin(joint_angle), np.cos(joint_angle)

        # add the length of the joint
        T[0, 3] = self.lengths[joint_name]

        # # rotate around x-axis
        if 'Roll' in joint_name:
            T[1, 1] = c
            T[1, 2] = s
            T[2, 1] = -s
            T[2, 2] = c
        # rotate around y-axis
        elif 'Pitch' in joint_name:
            T[0, 0] = c
            T[0, 2] = -s
            T[2, 0] = s
            T[2, 2] = c
        # rotate around z-axis (Yaw)
        else:
            T[0, 0] = c
            T[0, 1] = -s
            T[1, 0] = s
            T[1, 1] = c

        return T

    def forward_kinematics(self, joints):
        '''forward kinematics

        :param joints: {joint_name: joint_angle}
        '''
        for chain_joints in self.chains.values():
            Transform = identity(4)
            for joint in chain_joints:
                angle = joints[joint]

                # YOUR CODE HERE
                Transform *= self.local_trans(joint, angle)
                self.transforms[joint] = Transform
        

if __name__ == '__main__':
    agent = ForwardKinematicsAgent()
    agent.run()

