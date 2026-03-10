# bvillage/core/materials/policies/fachwerk.py

ROLE_DEFAULT_MATERIAL: dict[str, str] = {
    "PRIMARY_POST": "timber.oak",
    "HALL_POST": "timber.oak",
    "EAVES_PLATE_N": "timber.oak",
    "EAVES_PLATE_S": "timber.oak",
    "BRACE": "timber.oak",
    "INFILL": "brick.low_fired",
}

from bvillage.core.materials.role_registry import register_role_defaults

register_role_defaults(ROLE_DEFAULT_MATERIAL)
