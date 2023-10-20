import logging
import os
import pathlib
import sys
import traceback
from concurrent import futures
from datetime import datetime
from datetime import timezone
from types import FunctionType
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import grpc
import numpy
import pandas

from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_proto.common.id_pb2 import Id
from tecton_proto.feature_server.transform import transform_service_pb2
from tecton_proto.feature_server.transform import transform_service_pb2_grpc
from tecton_proto.feature_server.transform import transform_value_pb2


logger = logging.getLogger(__name__)


class IngestionRecord:
    def __init__(self, proto_request: transform_service_pb2.IngestionRecord, is_python_mode: bool):
        self.proto_request: transform_service_pb2.IngestionRecord = proto_request
        self.id: Id = self.proto_request.push_source_id
        self.payload = map_transform_value_to_python(self.proto_request.payload)
        if not is_python_mode:
            # In pandas mode, convert the dictionaries to dataframes with one row. Also need to convert top-level "list"
            # type values to numpy arrays for consistency with the offline behavior.
            np_arrays = convert_list_values_to_numpy_arrays(self.payload)
            self.payload = pandas.DataFrame.from_records([np_arrays])


def to_string(_id_proto: Id) -> str:
    return f"{_id_proto.most_significant_bits:016x}{_id_proto.least_significant_bits:016x}"


class UDFError(Exception):
    """An error in the definition of a UDF that could not be detected by the SDK/MDS."""


def eval_node(
    node,
    request_ds,
    intermediate_data,
    transforms: Dict[str, FunctionType],
    ingestion_record: Optional[IngestionRecord] = None,
):
    if node.HasField("request_data_source_node"):
        return request_ds
    elif node.HasField("feature_view_node"):
        return intermediate_data[node.feature_view_node.input_name]
    elif (
        node.HasField("data_source_node")
        and ingestion_record
        and node.data_source_node.virtual_data_source_id == ingestion_record.id
    ):
        return ingestion_record.payload
    elif node.HasField("transformation_node"):
        t = transforms[to_string(node.transformation_node.transformation_id)]
        args = []
        kwargs = {}
        for i in node.transformation_node.inputs:
            val = eval_node(i.node, request_ds, intermediate_data, transforms, ingestion_record=ingestion_record)
            if i.HasField("arg_index"):
                args.append(val)
            elif i.HasField("arg_name"):
                kwargs[i.arg_name] = val
        return t(*args, **kwargs)
    elif node.HasField("constant_node"):
        constant_node = node.constant_node
        if constant_node.HasField("string_const"):
            return constant_node.string_const
        elif constant_node.HasField("int_const"):
            return int(constant_node.int_const)
        elif constant_node.HasField("float_const"):
            return float(constant_node.float_const)
        elif constant_node.HasField("bool_const"):
            return constant_node.bool_constant
        elif constant_node.HasField("null_const"):
            return None
        msg = f"Unknown ConstantNode type: {constant_node}"
        raise KeyError(msg)
    else:
        msg = "unexpected node type in pipeline"
        raise Exception(msg)


# evaluate an individual odfv in the feature service request
def transform(
    odfv_request: transform_service_pb2.TransformRequest,
    request_context_input: Dict[str, Any],
    transforms: Dict[str, FunctionType],
    pipeline: Pipeline,
    is_python_mode: bool,
) -> List:
    # Could be further optimized to clone rather than repeatedly convert from the transform proto.
    fv_intermediate_inputs: Dict[str, Any] = {
        k: map_transform_value_to_python(v) for k, v in odfv_request.intermediate_data.items()
    }

    if not is_python_mode:
        # In pandas mode, convert the dictionaries to dataframes with one row. Also need to convert top-level "list"
        # type values to numpy arrays for consistency with the offline behavior.
        fv_intermediate_inputs = {k: convert_list_values_to_numpy_arrays(v) for k, v in fv_intermediate_inputs.items()}
        fv_intermediate_inputs = {k: pandas.DataFrame.from_records([v]) for k, v in fv_intermediate_inputs.items()}
        request_context_input = convert_list_values_to_numpy_arrays(request_context_input)
        request_context_input = pandas.DataFrame.from_records([request_context_input])

    _ingestion_record = (
        IngestionRecord(odfv_request.ingestion_record, is_python_mode)
        if odfv_request.HasField("ingestion_record")
        else None
    )

    out = eval_node(
        pipeline.root,
        request_context_input,
        fv_intermediate_inputs,
        transforms,
        ingestion_record=_ingestion_record,
    )

    root_func_name = transforms[to_string(pipeline.root.transformation_node.transformation_id)].__name__

    if is_python_mode:
        if (not isinstance(out, dict)) and (not isinstance(out, list)):
            msg = f"UDF for '{root_func_name}' returned type {type(out)}; expected type `dict` or `list`."
            raise UDFError(msg)
        if isinstance(out, dict):
            out = [out]
    else:
        # Convert the dataframe to a python dictionary.
        if len(out) != 1:
            root_func_name = transforms[
                to_string(odfv_request.pipeline.root.transformation_node.transformation_id)
            ].__name__
            logger.warning(
                f"UDF for '{root_func_name}' returned a dataframe " f"with an unexpected number of rows: {len(out)}."
            )
        out = out.to_dict("records")

    return [python_to_transform_value(r).map_value for r in out]


# Note that this method mutates the input dictionary. It does not make a copy.
def convert_list_values_to_numpy_arrays(dictionary):
    for k, v in dictionary.items():
        if isinstance(v, list):
            dictionary[k] = numpy.array(v)
    return dictionary


class TransformServerException(Exception):
    def __init__(self, code: grpc.StatusCode, details: str):
        self.code = code
        self.details = details


# evaluate all odfvs in the feature service request
def all_transforms(service_request: transform_service_pb2.ServiceRequest) -> transform_service_pb2.ServiceResponse:
    response = transform_service_pb2.ServiceResponse()

    transformation_modes: Dict[str, TransformationMode] = {}
    transformations: Dict[str, FunctionType] = {}

    for transformation in service_request.transformations:
        transformation_id = to_string(transformation.transformation_id)
        if transformation_id in transformations:
            continue
        scope: Dict[str, Any] = {}
        name = transformation.user_function.name
        exec(transformation.user_function.body, scope, scope)
        transformations[transformation_id] = scope[name]
        transformation_modes[transformation_id] = transformation.transformation_mode

    request_contexts_dict = map_transform_value_to_python(service_request.request_context)

    for request in service_request.requests:
        start = datetime.now()
        fv_id: str = request.feature_view_id  # This is already a string
        pipeline = service_request.pipelines[fv_id]
        try:
            # I think this is super fragile
            root_transformation_id = to_string(pipeline.root.transformation_node.transformation_id)
            odfv_mode = transformation_modes[root_transformation_id]
            is_python_mode = odfv_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON
            cloned_rc_input = request_contexts_dict.copy()
            output = transform(request, cloned_rc_input, transformations, pipeline, is_python_mode)
            for o in output:
                result = transform_service_pb2.TransformResponse(request_index=request.request_index, outputs=o)
                response.outputs.append(result)
        except UDFError as e:
            raise TransformServerException(grpc.StatusCode.FAILED_PRECONDITION, str(e))
        except Exception as e:
            print("Unexpected error executing ODFV\n" + traceback.format_exc(), file=sys.stderr)
            root_func_name = transformations[
                to_string(service_request.pipelines[fv_id].root.transformation_node.transformation_id)
            ].__name__
            raise TransformServerException(
                grpc.StatusCode.INVALID_ARGUMENT, f"{type(e).__name__}: {str(e)} (when evaluating UDF {root_func_name})"
            )
        # Adds the amount of time that the actual odfv transform took per transform request(per feature view)
        response.execution_times[request.feature_view_id].nanos += (datetime.now() - start).microseconds * 1000
    return response


def map_transform_value_to_python(value: transform_value_pb2.MapTransformValue) -> Dict[str, Any]:
    return {k: transform_value_to_python(v) for k, v in value.value_map.items()}


def transform_value_to_python(value: transform_value_pb2.TransformValue):
    value_type = value.WhichOneof("value")
    if value_type == "float64_value":
        return value.float64_value
    elif value_type == "int64_value":
        return value.int64_value
    elif value_type == "bool_value":
        return value.bool_value
    elif value_type == "string_value":
        return value.string_value
    elif value_type == "null_value":
        return None
    elif value_type == "map_value":
        return {k: transform_value_to_python(v) for k, v in value.map_value.value_map.items()}
    elif value_type == "array_value":
        return [transform_value_to_python(v) for v in value.array_value.elements]
    else:
        assert False, f"Unexpected value_type {value_type}"


def python_to_transform_value(python_value) -> transform_value_pb2.TransformValue:
    python_type = type(python_value)
    value_proto = transform_value_pb2.TransformValue()
    if python_value is None:
        # Return nulls explicitly.
        value_proto.null_value.CopyFrom(transform_value_pb2.NullTransformValue())
    elif python_type in (float, numpy.float64, numpy.float32):
        value_proto.float64_value = python_value
    elif python_type in (int, numpy.int32, numpy.int64):
        value_proto.int64_value = python_value
    elif python_type == bool:
        value_proto.bool_value = python_value
    elif python_type == str:
        value_proto.string_value = python_value
    elif python_type in (list, numpy.ndarray):
        value_proto.array_value.elements.extend([python_to_transform_value(v) for v in python_value])
    elif python_type == dict:
        if python_value:
            for k, v in python_value.items():
                value_proto.map_value.value_map[k].CopyFrom(python_to_transform_value(v))
        else:
            # An empty map is distinct from null, so fill an empty map value.
            value_proto.map_value.CopyFrom(transform_value_pb2.MapTransformValue())
    elif python_type == pandas.Timestamp:
        value_proto.string_value = python_value.isoformat()
    elif python_type == datetime:
        # This ensures that the datetime is timezone-aware. If it's not, assume UTC.
        if python_value.tzinfo is None:
            python_value = python_value.replace(tzinfo=timezone.utc)
        value_proto.string_value = python_value.isoformat()
    else:
        assert False, f"Unexpected python data type {python_type}"
    return value_proto


class TransformServer(transform_service_pb2_grpc.TransformServiceServicer):
    def Evaluate(self, request: transform_service_pb2.ServiceRequest, context):
        try:
            return all_transforms(request)
        except TransformServerException as e:
            context.abort(e.code, e.details)


def main():
    try:
        socket = pathlib.Path(os.environ["TRANSFORM_SERVER_SOCKET"])
    except KeyError as e:
        msg = "TRANSFORM_SERVER_SOCKET must be set in the environment"
        raise AssertionError(msg) from e
    assert not socket.exists(), "TRANSFORM_SERVER_SOCKET points to an existing socket"

    options = []

    # Set the maximum size of a request the server can receive from the client. Defaults to 4MB.
    max_recv_length = os.environ.get("MAX_TRANSFORM_SERVICE_REQUEST_SIZE_BYTES", None)
    if max_recv_length is not None:
        options.append(("grpc.max_receive_message_length", int(max_recv_length)))

    print(
        f"Python server starting at {socket}",
        flush=True,
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2), options=options)
    server.add_insecure_port(f"unix:/{socket.absolute()}")
    transform_service_pb2_grpc.add_TransformServiceServicer_to_server(TransformServer(), server)
    server.start()
    print("Python server started", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
