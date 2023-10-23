import typer
from sona.core.inferencer import InferencerBase
from sona.settings import settings

INFERENCER_CLASS = settings.SONA_INFERENCER_CLASS

app = typer.Typer()


@app.command()
def test(inferencer_cls: str):
    inferencer: InferencerBase = InferencerBase.load_class(inferencer_cls)()
    inferencer.on_load()
    retult = inferencer.process(inferencer.context_example())
    print(retult)
