from pathlib import Path
from fluent.runtime import FluentResourceLoader, FluentLocalization

loader = FluentResourceLoader(str(Path(__file__).parent))

i18n = FluentLocalization(
    locales=["en"],
    resource_ids=["main.ftl"],
    resource_loader=loader,
)