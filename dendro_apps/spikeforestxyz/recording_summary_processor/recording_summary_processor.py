import os
from dendro.sdk import ProcessorBase, InputFile, OutputFile
from dendro.sdk import BaseModel, Field


class RecordingSummaryContext(BaseModel):
    input: InputFile = Field(description="Input .nwb.lindi.json file")
    output: OutputFile = Field(description="Output .json file")


class RecordingSummaryProcessor(ProcessorBase):
    name = "spikeforestxyz.recording_summary"
    description = "Create recording summary for a recording .nwb.lindi.json file"
    label = "spikeforestxyz.recording_summary"
    tags = []
    attributes = {"wip": True}

    @staticmethod
    def run(context: RecordingSummaryContext):
        from .create_recording_summary import create_recording_summary

        output_fname = 'output.nwb.lindi.json'
        context.input.download(output_fname)
        cache_dir = os.path.join(os.getcwd(), 'local_cache')
        os.makedirs(cache_dir, exist_ok=True)
        create_recording_summary(
            output_fname,
            cache_dir=cache_dir
        )
        context.output.upload(output_fname)
