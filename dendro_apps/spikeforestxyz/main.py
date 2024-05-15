#!/usr/bin/env python


from dendro.sdk import App
from recording_summary.recording_summary import RecordingSummaryProcessor
from mountainsort5.mountainsort5 import Mountainsort5Processor

app = App(
    name="spikeforestxyz",
    description="Processors for SpikeForestXYZ",
    app_image="ghcr.io/magland/spikeforestxyz:latest",
    app_executable="/app/main.py",
)


app.add_processor(RecordingSummaryProcessor)
app.add_processor(Mountainsort5Processor)

if __name__ == "__main__":
    app.run()
