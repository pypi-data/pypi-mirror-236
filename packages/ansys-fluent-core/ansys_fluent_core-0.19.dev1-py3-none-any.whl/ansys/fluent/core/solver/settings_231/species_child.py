#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .axis_direction_child import axis_direction_child

class species_child(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'child_object_type' of /home/ansys/actions-runner/_work/pyfluent/pyfluent/src/ansys/fluent/core/solver/settings_231/species.
    """

    fluent_name = "child-object-type"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of species_child.
    """
