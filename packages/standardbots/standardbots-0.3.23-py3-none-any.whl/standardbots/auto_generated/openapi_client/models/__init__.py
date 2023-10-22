# coding: utf-8

# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from standardbots.auto_generated.openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from standardbots.auto_generated.openapi_client.model.arm_joint_rotations import ArmJointRotations
from standardbots.auto_generated.openapi_client.model.arm_tooltip_position import ArmTooltipPosition
from standardbots.auto_generated.openapi_client.model.brakes_state import BrakesState
from standardbots.auto_generated.openapi_client.model.combined_arm_position import CombinedArmPosition
from standardbots.auto_generated.openapi_client.model.engage_emergency_stop_request import EngageEmergencyStopRequest
from standardbots.auto_generated.openapi_client.model.error_response import ErrorResponse
from standardbots.auto_generated.openapi_client.model.force_unit import ForceUnit
from standardbots.auto_generated.openapi_client.model.gripper_command_request import GripperCommandRequest
from standardbots.auto_generated.openapi_client.model.gripper_configuration import GripperConfiguration
from standardbots.auto_generated.openapi_client.model.joint_rotations import JointRotations
from standardbots.auto_generated.openapi_client.model.linear_unit import LinearUnit
from standardbots.auto_generated.openapi_client.model.move_request import MoveRequest
from standardbots.auto_generated.openapi_client.model.move_robot_canceled_event import MoveRobotCanceledEvent
from standardbots.auto_generated.openapi_client.model.move_robot_event import MoveRobotEvent
from standardbots.auto_generated.openapi_client.model.move_robot_failure_event import MoveRobotFailureEvent
from standardbots.auto_generated.openapi_client.model.orientation import Orientation
from standardbots.auto_generated.openapi_client.model.position import Position
from standardbots.auto_generated.openapi_client.model.robot_control_mode import RobotControlMode
from standardbots.auto_generated.openapi_client.model.routine import Routine
from standardbots.auto_generated.openapi_client.model.runtime_variable import RuntimeVariable
from standardbots.auto_generated.openapi_client.model.set_brake_state_request import SetBrakeStateRequest
