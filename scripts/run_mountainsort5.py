import dendro.client as dc
from create_recording_summaries import _get_all_recording_names


def create_recording_summaries():
    dendro_project_id = '9e302504'  # https://dendro.vercel.app/project/9e302504?tab=project-home

    project = dc.load_project(dendro_project_id)
    batch_id = dc.create_batch_id()

    all_recording_names = _get_all_recording_names(project)
    for name in all_recording_names:
        print('=====================')
        print(name)
        output_fname = f'spike_sorting/mountainsort5/{name}.nwb.lindi.json'
        ff = project.get_file(output_fname)
        if ff is not None:
            print("Skipping - already exists")
            continue
        dc.submit_job(
            project=project,
            processor_name='spikeforestxyz.mountainsort5',
            input_files=[
                dc.SubmitJobInputFile(
                    name='input',
                    file_name=f'recordings/{name}.nwb.lindi.json'
                )
            ],
            output_files=[
                dc.SubmitJobOutputFile(
                    name='output',
                    file_name=output_fname
                )
            ],
            parameters=[],
            batch_id=batch_id,
            required_resources=dc.DendroJobRequiredResources(
                numCpus=4,
                numGpus=0,
                memoryGb=16,
                timeSec=60 * 60 * 24
            ),
            run_method='local'
        )


if __name__ == "__main__":
    create_recording_summaries()
