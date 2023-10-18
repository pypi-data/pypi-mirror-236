from asphalt.core import Component, Context
from jupyter_ydoc import YNotebook

from txl.base import Notebook, NotebookFactory


class _Notebook(Notebook):
    """A collaborative notebook document."""

    def __init__(self, ynotebook: YNotebook):
        self.ynotebook = ynotebook
        super().__init__()


class NotebookComponent(Component):
    async def start(
        self,
        ctx: Context,
    ) -> None:
        def notebook_factory(ynotebook: YNotebook) -> Notebook:
            return _Notebook(ynotebook)

        ctx.add_resource(notebook_factory, types=NotebookFactory)
