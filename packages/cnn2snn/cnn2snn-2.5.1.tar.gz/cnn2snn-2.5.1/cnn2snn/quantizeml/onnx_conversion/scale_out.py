#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ["set_output_scale_variables"]

import numpy as np

from .weights import broadcast_and_set_variable


def set_output_scale_variables(ak_layer, scale, shift):
    """Set output scale into akida variables.

    Args:
        ak_layer (akida.Layer): the akida layer to set variables.
        scale (np.ndarray): the scale.
        shift (np.ndarray): the power of two that represent the shift.
    """
    broadcast_and_set_variable(ak_layer.variables, "output_scales", scale)
    shift = np.log2(shift)
    # In akida, shift is applied as left shift (when positive) or right shift (otherwise).
    # However, in onnx scale out, shift was performed through one division.
    # It explains the minus sign.
    broadcast_and_set_variable(ak_layer.variables, "output_shift", -shift)
