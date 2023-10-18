from typing import Any, Dict, Optional, TypedDict

from autoflake import fix_code
from pylsp import hookimpl
from pylsp.config.config import Config
from pylsp.workspace import Document


class Position(TypedDict):
    line: int
    character: int


class Range(TypedDict):
    start: Position
    end: Position


ALLOWED_KEYS = {
    "additional_imports",
    "expand_star_imports",
    "remove_all_unused_imports",
    "remove_duplicate_keys",
    "remove_unused_variables",
    "remove_rhs_for_unused_variables",
    "ignore_init_module_imports",
    "ignore_pass_statements",
    "ignore_pass_after_docstring",
}


def _format(
    outcome,
    config: Config,
    document: Document,
    code_range: Optional[Range] = None,
):
    result = outcome.get_result()
    if result:
        text = result[0]["newText"]
        code_range = result[0]["code_range"]
    elif code_range:
        text = "".join(
            document.lines[
                code_range["start"]["line"] : code_range["end"]["line"]
            ]
        )
    else:
        text = document.source
        code_range = Range(
            start={"line": 0, "character": 0},
            end={"line": len(document.lines), "character": 0},
        )
    settings = config.plugin_settings("autoflake", document_path=document.path)
    settings = {k: v for k, v in settings.items() if k in ALLOWED_KEYS}
    new_text = fix_code(text, **settings)

    if new_text != text:
        result = [{"range": code_range, "newText": new_text}]
        outcome.force_result(result)


@hookimpl
def pylsp_settings() -> Dict[str, Any]:
    return {
        "plugins": {
            "autoflake": {
                "enabled": True,
            },
        },
    }


@hookimpl(hookwrapper=True)
def pylsp_format_document(config: Config, document: Document):
    outcome = yield
    _format(outcome, config, document)


@hookimpl(hookwrapper=True)
def pylsp_format_code_range(
    config: Config, document: Document, code_range: Range
):
    outcome = yield
    _format(outcome, config, document, code_range)
