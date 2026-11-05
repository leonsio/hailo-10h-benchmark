"""Native prompt renderer extracted unchanged from hailo-10h-services; Apache-2.0."""
from jinja2 import StrictUndefined, TemplateError
from jinja2.sandbox import ImmutableSandboxedEnvironment

def render_prompt(model, prompt, *, model_kind="VLM", template_options=None):
    """Render the native chat template in a strict Jinja sandbox.

    Args:
        model (Any): Native model exposing tokenization/template methods, or a catalogue identifier.
        prompt (str | list[dict[str, Any]]): Question text or prepared native prompt messages.
        model_kind (str): Native backend role label: LLM or VLM.
        template_options (dict[str, Any] | None): Catalogue options controlling native template rendering.

    Returns:
        str: Exact model-bound prompt text, or conservative ChatML fallback.

    Raises:
        ValueError: prompt_template.empty_tool_calls must be include or omit.
    """
    template_method = getattr(model, "prompt_template", None)
    if not callable(template_method):
        # Older bindings: ChatML plus conservative margin; native tokenize still required.
        return (
            "".join(
                "<|im_start|>"
                + message["role"]
                + "\n"
                + (
                    message["content"]
                    if isinstance(message["content"], str)
                    else "".join(
                        part.get("text", "<|vision_start|><|image_pad|><|vision_end|>")
                        for part in message["content"]
                    )
                )
                + "<|im_end|>\n"
                for message in prompt
            )
            + "<|im_start|>assistant\n"
        )
    environment = ImmutableSandboxedEnvironment(undefined=StrictUndefined)

    def raise_exception(message):
        """Expose the native template error helper inside the Jinja sandbox.

        Args:
            message (str | dict[str, Any]): Formatted diagnostic text or ASGI message.

        Returns:
            None: Never returns; raises the supplied template error.

        Raises:
            ValueError: The native Jinja template explicitly reports an unsupported prompt.
        """
        raise ValueError(str(message))

    environment.globals["raise_exception"] = raise_exception
    # Qwen3 reads optional tool_calls directly; Llama checks field membership
    # and requires exactly one call when present. Use catalogue metadata rather
    # than model-name checks, preserving StrictUndefined for other variables.
    empty_tool_calls = (template_options or {}).get("empty_tool_calls", "include")
    if empty_tool_calls not in {"include", "omit"}:
        raise ValueError("prompt_template.empty_tool_calls must be include or omit")
    template_messages = []
    for message in prompt:
        template_message = dict(message)
        if empty_tool_calls == "omit":
            if template_message.get("tool_calls") == []:
                template_message.pop("tool_calls")
        else:
            template_message.setdefault("tool_calls", [])
        template_messages.append(template_message)
    try:
        return environment.from_string(template_method()).render(
            messages=template_messages,
            add_generation_prompt=True,
            tools=None,
            bos_token="",
            eos_token="" if model_kind == "LLM" else "<|im_end|>",
            enable_thinking=False,
            add_vision_id=False,
        )
    except TemplateError as exc:
        raise ValueError(
            f"Cannot render the loaded {model_kind}'s prompt template for input budgeting"
        ) from exc
