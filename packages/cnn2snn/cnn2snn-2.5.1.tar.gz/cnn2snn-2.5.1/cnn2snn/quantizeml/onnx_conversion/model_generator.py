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
__all__ = ["generate_onnx_model"]

from onnx.helper import make_node
from onnx.checker import check_model
from copy import deepcopy

import akida

from .base_converter import DOMAIN
from .register import map_node_to_converter


def get_convertible_nodes(model):
    """Return the node list of candidates to convert.

    Args:
        model (ModelProto): the model to convert.

    Returns:
        list of NodeProto: the node list.
    """
    # Remove first QuantizedLinear (we allow to skip it at conversion)
    input_names = [x.name for x in model.graph.input]
    if len(model.graph.node) > 0 and model.graph.node[0].op_type == "QuantizeLinear":
        node = model.graph.node.pop(0)
        # QuantizedLinear ouput will be the real input to convert
        input_names = node.output

    # Check if there is a Dequantizer at the end of the graph.
    # Nodes after that will be skipped from conversion.
    idx = 0
    for idx, node in enumerate(model.graph.node):
        if node.op_type == "DequantizeLinear":
            # Add right domain to match with others
            node.domain = DOMAIN
            break

    # Check model is not empty (at least one node to convert is required)
    if len(model.graph.node[: idx + 1]) == 0:
        raise ValueError("Model is empty or does not have any node to convert.")

    # Check if model needs to add an InputData: when first node is not an input layer
    input_layer = map_node_to_converter(model.graph.node[0], model)
    if not input_layer.is_input_layer:
        idx += 1
        model.graph.node.insert(0, make_node("InputData", [], input_names, domain=DOMAIN))
    return model.graph.node[: idx + 1]


def generate_onnx_model(model):
    """Generates an Akida model based on an ONNX quantizeml model.

    Args:
        model (obj:`onnx.ModelProto`): a ONNX model to convert.

    Returns:
        akida.Model: the generated Akida model.
    """
    # Clone model to keep the original intact
    model = deepcopy(model)

    # Model must be compatible with ONNX
    check_model(model, full_check=True)

    # Checks over model
    assert len(model.graph.input) == 1, "Unsupported mode: it must have exactly one input."
    assert len(model.graph.output) == 1, "Unsupported mode: it must have exactly one output."

    # Now create akida model and iterate nodes to convert each one in an akida layer.
    target_nodes = get_convertible_nodes(model)
    akida_model = akida.Model()
    for node in target_nodes:
        converter = map_node_to_converter(node, model)
        converter.convert(akida_model)
    return akida_model
