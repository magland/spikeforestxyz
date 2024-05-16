from dendro.sdk import ProcessorBase, InputFile, OutputFile
from dendro.sdk import BaseModel, Field


class Mountainsort5Context(BaseModel):
    input: InputFile = Field(description="Input .nwb.lindi.json file")
    output: OutputFile = Field(description="Output .json file")


class Mountainsort5Processor(ProcessorBase):
    name = "spikeforestxyz.mountainsort5"
    description = "Run mountainsort5 spike sorting on a recording."
    label = "spikeforestxyz.mountainsort5"
    tags = []
    attributes = {"wip": True}

    @staticmethod
    def run(context: Mountainsort5Context):
        from .run_mountainsort5 import run_mountainsort5

        output_fname = 'output.nwb.lindi.json'
        print('Downloading input file')
        context.input.download(output_fname)
        print('Running mountainsort5')
        run_mountainsort5(
            output_fname
        )
        print('Uploading output file')
        context.output.upload(output_fname)
        print('Done')
