import shutil
import lindi
import kachery_cloud as kcl
import pynwb
import spikeinterface as si
from spikeinterface_pipelines import pipeline as si_pipeline
from .nwbextractors import NwbRecordingExtractor
from neuroconv.tools.spikeinterface import write_sorting


def run_mountainsort5(
    nwb_lindi_fname: str
):
    print('Running MountainSort5 on', nwb_lindi_fname)
    staging_area = lindi.StagingArea.create(dir=nwb_lindi_fname + '.d')
    f = lindi.LindiH5pyFile.from_lindi_file(
        nwb_lindi_fname,
        mode='r+',
        staging_area=staging_area,
        local_cache=lindi.LocalCache()
    )
    rec = NwbRecordingExtractor(h5py_file=f)  # type: ignore

    preprocessing_params = si_pipeline.PreprocessingParams()

    spikesorting_params = si_pipeline.SpikeSortingParams(
        sorter_name='mountainsort5',  # type: ignore
        sorter_kwargs=si_pipeline.MountainSort5Model()
    )

    postprocessing_params = si_pipeline.PostprocessingParams()

    curation_params = si_pipeline.CurationParams()

    visualization_params = si_pipeline.VisualizationParams()

    print('Running the pipeline')
    rec_pre, sorting, we, sc, vo = si_pipeline.run_pipeline(
        recording=rec,
        scratch_folder='./scratch/',
        results_folder='./results/',
        job_kwargs={},
        preprocessing_params=preprocessing_params,
        spikesorting_params=spikesorting_params,
        postprocessing_params=postprocessing_params,
        curation_params=curation_params,
        visualization_params=visualization_params,
        run_preprocessing=True,
        run_spikesorting=True,
        run_postprocessing=False,
        run_curation=False,
        run_visualization=False
    )
    print('Pipeline finished')
    assert isinstance(sorting, si.BaseSorting)

    print('Writing the sorting to the NWB file')
    with pynwb.NWBHDF5IO(file=f, mode='r+') as io:
        nwb = io.read()
        write_sorting(
            sorting=sorting,
            nwbfile=nwb,  # type: ignore
            write_as='processing',
            units_name='mountainsort5_units'
        )
        print('Writing the NWB file')
        io.write(nwb)  # type: ignore

    print('Writing changes to the file')
    f.flush()  # write changes to the file

    def on_store_blob(filename: str):
        url = kcl.store_file(filename)
        return url

    def on_store_main(filename: str):
        shutil.copyfile(filename, nwb_lindi_fname)
        return nwb_lindi_fname

    staging_store = f.staging_store
    assert staging_store is not None
    print('Uploading supporting files')
    f.upload(
        on_upload_blob=on_store_blob,
        on_upload_main=on_store_main
    )
    print('Done uploading supporting files')
