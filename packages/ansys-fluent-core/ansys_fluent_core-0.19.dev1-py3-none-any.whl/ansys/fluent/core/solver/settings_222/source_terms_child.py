#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _HasAllowedValuesMixin

from .child_object_type_child import child_object_type_child

class source_terms_child(ListObject[child_object_type_child]):
    """
    'child_object_type' of /home/ansys/actions-runner/_work/pyfluent/pyfluent/src/ansys/fluent/core/solver/settings_222/source_terms.
    """

    fluent_name = "child-object-type"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of source_terms_child.
    """
