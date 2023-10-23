from contextlib import contextmanager
from collections.abc import Generator

from .auto_generated import models
class ControlApi(robot_control_api.RobotControlApi):
  def brake(self, state: str):
    return self.set_brakes_state(body=robot_control_api.ControlBrakesRequest(state='engaged'))
  
  def unbrake(self):
    return self.set_brakes_state(body=robot_control_api.ControlBrakesRequest(state='disengaged'))

  def move(self, **kwargs: models.MoveRequest):
    return self.set_arm_position(body=models.MoveRequest(**kwargs))

  def grip(self, **kwargs: models.GripperCommandRequest):
    return self.control_gripper(body=models.GripperCommandRequest(**kwargs))

class StandardBotsSdk:
  def __init__(self, endpoint: str, token: str, robot_kind: str):
    self.endpoint = endpoint
    self.token = token
    self.robot_kind = robot_kind
  
  @contextmanager
  def api_client(self) -> Generator[ApiClient, None, None]:
    configuration = Configuration(
      host=self.endpoint,
    )
    configuration.proxy_headers={'robot_kind': self.robot_kind}
    configuration.api_key['token'] = self.token
    with ApiClient(configuration) as api_client:
      yield api_client

  @contextmanager
  def control_api(self) -> Generator[ControlApi, None, None]:
    with self.api_client() as api_client:
      yield ControlApi(api_client)

  @contextmanager
  def configuration_api(self) -> Generator[robot_configuration_api.RobotConfigurationApi, None, None]:
    with self.api_client() as api_client:
      yield robot_configuration_api.RobotConfigurationApi(api_client)
