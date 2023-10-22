# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from standardbots.auto_generated.openapi_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    CONFIGURATION = "Configuration"
    CONTROL = "Control"
    EQUIPMENT__GRIPPERS = "Equipment → Grippers"
    MOVEMENT__BRAKES = "Movement → Brakes"
    MOVEMENT__POSITION = "Movement → Position"
    ROUTINE_EDITOR = "Routine Editor"
    STATUS = "Status"
