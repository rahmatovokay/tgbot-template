from pathlib import Path
from fluent.runtime import FluentResourceLoader, FluentLocalization

from src.config import DEFAULT_LANGUAGE

loader = FluentResourceLoader(str(Path(__file__).parent))

i18n = FluentLocalization(
    locales=[DEFAULT_LANGUAGE],
    resource_ids=[
        "base.ftl"
    ],
    resource_loader=loader,
)
