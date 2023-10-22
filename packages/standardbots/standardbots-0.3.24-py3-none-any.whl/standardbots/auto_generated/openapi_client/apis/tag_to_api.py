import typing_extensions

from standardbots.auto_generated.openapi_client.apis.tags import TagValues
from standardbots.auto_generated.openapi_client.apis.tags.configuration_api import ConfigurationApi
from standardbots.auto_generated.openapi_client.apis.tags.control_api import ControlApi
from standardbots.auto_generated.openapi_client.apis.tags.equipment_grippers_api import EquipmentGrippersApi
from standardbots.auto_generated.openapi_client.apis.tags.movement_brakes_api import MovementBrakesApi
from standardbots.auto_generated.openapi_client.apis.tags.movement_position_api import MovementPositionApi
from standardbots.auto_generated.openapi_client.apis.tags.routine_editor_api import RoutineEditorApi
from standardbots.auto_generated.openapi_client.apis.tags.status_api import StatusApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.CONFIGURATION: ConfigurationApi,
        TagValues.CONTROL: ControlApi,
        TagValues.EQUIPMENT__GRIPPERS: EquipmentGrippersApi,
        TagValues.MOVEMENT__BRAKES: MovementBrakesApi,
        TagValues.MOVEMENT__POSITION: MovementPositionApi,
        TagValues.ROUTINE_EDITOR: RoutineEditorApi,
        TagValues.STATUS: StatusApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.CONFIGURATION: ConfigurationApi,
        TagValues.CONTROL: ControlApi,
        TagValues.EQUIPMENT__GRIPPERS: EquipmentGrippersApi,
        TagValues.MOVEMENT__BRAKES: MovementBrakesApi,
        TagValues.MOVEMENT__POSITION: MovementPositionApi,
        TagValues.ROUTINE_EDITOR: RoutineEditorApi,
        TagValues.STATUS: StatusApi,
    }
)
