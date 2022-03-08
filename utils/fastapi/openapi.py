from fastapi.openapi.utils import *


def base_get_openapi_path(
        *, route: routing.APIRoute, model_name_map: Dict[type, str]
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    path = {}
    security_schemes: Dict[str, Any] = {}
    definitions: Dict[str, Any] = {}
    assert route.methods is not None, "Methods must be a list"
    if isinstance(route.response_class, DefaultPlaceholder):
        current_response_class: Type[Response] = route.response_class.value
    else:
        current_response_class = route.response_class
    assert current_response_class, "A response class is needed to generate OpenAPI"
    route_response_media_type: Optional[str] = current_response_class.media_type
    if route.include_in_schema:
        for method in route.methods:
            operation = get_openapi_operation_metadata(
                route=route, method=method)
            parameters: List[Dict[str, Any]] = []
            flat_dependant = get_flat_dependant(
                route.dependant, skip_repeats=True)
            security_definitions, operation_security = get_openapi_security_definitions(
                flat_dependant=flat_dependant
            )
            if operation_security:
                operation.setdefault("security", []).extend(operation_security)
            if security_definitions:
                security_schemes.update(security_definitions)
            all_route_params = get_flat_params(route.dependant)
            operation_parameters = get_openapi_operation_parameters(
                all_route_params=all_route_params, model_name_map=model_name_map
            )
            parameters.extend(operation_parameters)
            if parameters:
                operation["parameters"] = list(
                    {param["name"]: param for param in parameters}.values()
                )
            if method in METHODS_WITH_BODY:
                request_body_oai = get_openapi_operation_request_body(
                    body_field=route.body_field, model_name_map=model_name_map
                )
                if request_body_oai:
                    operation["requestBody"] = request_body_oai
            if route.callbacks:
                callbacks = {}
                for callback in route.callbacks:
                    if isinstance(callback, routing.APIRoute):
                        (
                            cb_path,
                            cb_security_schemes,
                            cb_definitions,
                        ) = base_get_openapi_path(
                            route=callback, model_name_map=model_name_map
                        )
                        callbacks[callback.name] = {callback.path: cb_path}
                operation["callbacks"] = callbacks
            status_code = str(route.status_code) if route.status_code else '200'
            operation.setdefault("responses", {}).setdefault(status_code, {})[
                "description"
            ] = route.response_description
            if (
                    route_response_media_type
                    and route.status_code not in STATUS_CODES_WITH_NO_BODY
            ):
                response_schema = {"type": "string"}
                if lenient_issubclass(current_response_class, JSONResponse):
                    if route.response_field:
                        response_schema, _, _ = field_schema(
                            route.response_field,
                            model_name_map=model_name_map,
                            ref_prefix=REF_PREFIX,
                        )
                    else:
                        response_schema = {}
                operation.setdefault("responses", {}).setdefault(
                    status_code, {}
                ).setdefault("content", {}).setdefault(route_response_media_type, {})[
                    "schema"
                ] = response_schema
            if route.responses:
                operation_responses = operation.setdefault("responses", {})
                for (
                        additional_status_code,
                        additional_response,
                ) in route.responses.items():
                    process_response = additional_response.copy()
                    process_response.pop("model", None)
                    status_code_key = str(additional_status_code).upper()
                    if status_code_key == "DEFAULT":
                        status_code_key = "default"
                    openapi_response = operation_responses.setdefault(
                        status_code_key, {}
                    )
                    assert isinstance(
                        process_response, dict
                    ), "An additional response must be a dict"
                    field = route.response_fields.get(additional_status_code)
                    additional_field_schema: Optional[Dict[str, Any]] = None
                    if field:
                        additional_field_schema, _, _ = field_schema(
                            field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
                        )
                        media_type = route_response_media_type or "application/json"
                        additional_schema = (
                            process_response.setdefault("content", {})
                                .setdefault(media_type, {})
                                .setdefault("schema", {})
                        )
                        deep_dict_update(additional_schema,
                                         additional_field_schema)
                    status_text: Optional[str] = status_code_ranges.get(
                        str(additional_status_code).upper()
                    ) or http.client.responses.get(int(additional_status_code))
                    description = (
                            process_response.get("description")
                            or openapi_response.get("description")
                            or status_text
                            or "Additional Response"
                    )
                    deep_dict_update(openapi_response, process_response)
                    openapi_response["description"] = description
            # http422 = str(HTTP_422_UNPROCESSABLE_ENTITY)
            # if (all_route_params or route.body_field) and not any(
            #     [
            #         status in operation["responses"]
            #         for status in [http422, "4XX", "default"]
            #     ]
            # ):
            #     operation["responses"][http422] = {
            #         "description": "Validation Error",
            #         "content": {
            #             "application/json": {
            #                 "schema": {"$ref": REF_PREFIX + "HTTPValidationError"}
            #             }
            #         },
            #     }
            #     if "ValidationError" not in definitions:
            #         definitions.update(
            #             {
            #                 "ValidationError": validation_error_definition,
            #                 "HTTPValidationError": validation_error_response_definition,
            #             }
            #         )
            path[method.lower()] = operation
    return path, security_schemes, definitions


def base_get_openapi(
        *,
        title: str,
        version: str,
        openapi_version: str = "3.0.2",
        description: Optional[str] = None,
        routes: Sequence[BaseRoute],
        tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
) -> Dict[str, Any]:
    info = {"title": title, "version": version}
    if description:
        info["description"] = description
    output: Dict[str, Any] = {"openapi": openapi_version, "info": info}
    if servers:
        output["servers"] = servers
    components: Dict[str, Dict[str, Any]] = {}
    paths: Dict[str, Dict[str, Any]] = {}
    flat_models = get_flat_models_from_routes(routes)
    model_name_map = get_model_name_map(flat_models)
    definitions = get_model_definitions(
        flat_models=flat_models, model_name_map=model_name_map
    )
    for route in routes:
        if isinstance(route, routing.APIRoute):
            result = base_get_openapi_path(
                route=route, model_name_map=model_name_map)
            if result:
                path, security_schemes, path_definitions = result
                if path:
                    paths.setdefault(route.path_format, {}).update(path)
                if security_schemes:
                    components.setdefault("securitySchemes", {}).update(
                        security_schemes
                    )
                if path_definitions:
                    definitions.update(path_definitions)
    if definitions:
        components["schemas"] = {k: definitions[k]
                                 for k in sorted(definitions)}
    if components:
        output["components"] = components
    output["paths"] = paths
    if tags:
        output["tags"] = tags
    # type: ignore
    return jsonable_encoder(OpenAPI(**output), by_alias=True, exclude_none=True)
