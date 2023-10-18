from __future__ import annotations

from typing import Any

from mknodes.basenodes import mknode
from mknodes.utils import clihelpers, log, reprhelpers


logger = log.get_logger(__name__)


class MkClickDoc(mknode.MkNode):
    """Documentation for click / typer CLI apps."""

    ICON = "material/api"

    def __init__(
        self,
        target: str | None = None,
        prog_name: str | None = None,
        show_hidden: bool = False,
        show_subcommands: bool = False,
        **kwargs: Any,
    ):
        r"""Constructor.

        Arguments:
            target: Dotted path to Click command
            prog_name: Program name
            show_hidden: Show commands and options that are marked as hidden.
            show_subcommands: List subcommands of a given command.
            kwargs: Keyword arguments passed to parent
        """
        super().__init__(**kwargs)
        self._target = target
        self._prog_name = prog_name
        self.show_hidden = show_hidden
        self.show_subcommands = show_subcommands

    def __repr__(self):
        return reprhelpers.get_repr(self, target=self._target)

    @property
    def attributes(self) -> dict[str, Any]:
        # sourcery skip: use-named-expression
        dct: dict[str, Any] = {}
        match self._target:
            case str():
                module, command = self._target.split(":")
                dct = dict(module=module, command=command, prog_name=self._prog_name)
            case None:
                cli_eps = self.ctx.metadata.entry_points.get("console_scripts")
                if cli_eps:
                    module, command = cli_eps[0].dotted_path.split(":")
                    dct = dict(module=module, command=command, prog_name=cli_eps[0].name)
        if not dct:
            return {}
        dct.update(show_hidden=self.show_hidden, show_subcommands=self.show_subcommands)
        return dct

    def _to_markdown(self) -> str:
        import importlib

        if not self.attributes:
            return ""
        app = self.ctx.metadata.cli
        if not app:
            return ""
        attrs = self.attributes
        mod = importlib.import_module(attrs["module"])
        instance = getattr(mod, attrs["command"])
        info = clihelpers.get_typer_info(instance, command=attrs["prog_name"])
        return info.to_markdown(recursive=self.show_subcommands)

    @classmethod
    def create_example_page(cls, page):
        # import mknodes as mk

        page += "The MkClickDoc node shows DocStrings for Click / Typer."
        page += MkClickDoc(target="mkdocs_mknodes.cli:cli")
        # node = MkClickDoc(module="cli", command="cli")
        # page += mk.MkReprRawRendered(node)


if __name__ == "__main__":
    docstrings = MkClickDoc.with_default_context("mkdocs_mknodes.cli:cli")
    print(docstrings)
