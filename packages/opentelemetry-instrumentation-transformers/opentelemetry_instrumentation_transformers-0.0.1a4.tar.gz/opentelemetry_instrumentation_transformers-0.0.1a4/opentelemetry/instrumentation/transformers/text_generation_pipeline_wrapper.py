import logging

from opentelemetry.semconv.ai import SpanAttributes
from opentelemetry.trace import Status, StatusCode

from opentelemetry import context as context_api

from opentelemetry.instrumentation.utils import (
    _SUPPRESS_INSTRUMENTATION_KEY
)

from opentelemetry.instrumentation.transformers.utils import _with_tracer_wrapper

logger = logging.getLogger(__name__)


def _set_span_attribute(span, name, value):
    if value is not None:
        if value != "":
            span.set_attribute(name, value)
    return


def _set_span_prompts(span, messages):
    if messages is None:
        return

    print(str(messages))

    if isinstance(messages, str):
        messages = [messages]

    for i, msg in enumerate(messages):
        prefix = f"{SpanAttributes.LLM_PROMPTS}.{i}"
        _set_span_attribute(span, f"{prefix}.role", "user")
        _set_span_attribute(span, f"{prefix}.content", msg)


def _set_input_attributes(span, kwargs):
    _set_span_prompts(span, kwargs.get("args"))

    return


def _set_span_completions(span, completions):
    if completions is None:
        return

    for completion in completions:
        index = completion.get("index")
        prefix = f"{SpanAttributes.LLM_COMPLETIONS}.{index}"
        _set_span_attribute(span, f"{prefix}.content", completion.get("text"))


def _set_response_attributes(span, response):
    print(str(response))
    # _set_span_completions(span, response.get("choices"))

    return


@_with_tracer_wrapper
def text_generation_pipeline_wrapper(tracer, to_wrap, wrapped, instance, args, kwargs):
    """Instruments and calls every function defined in TO_WRAP."""
    if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
        return wrapped(*args, **kwargs)

    name = to_wrap.get("span_name")
    with tracer.start_as_current_span(name) as span:
        if span.is_recording():
            try:
                if span.is_recording():
                    _set_input_attributes(span, kwargs)

            except Exception as ex:  # pylint: disable=broad-except
                logger.warning(
                    "Failed to set input attributes for transformers span, error: %s", str(ex)
                )

        response = wrapped(*args, **kwargs)

        if response:
            try:
                if span.is_recording():
                    _set_response_attributes(span, response)

            except Exception as ex:  # pylint: disable=broad-except
                logger.warning(
                    "Failed to set response attributes for transformers span, error: %s",
                    str(ex),
                )
            if span.is_recording():
                span.set_status(Status(StatusCode.OK))

        return response
