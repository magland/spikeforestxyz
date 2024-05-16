FROM python:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Install dendro
RUN pip install dendro==0.2.17

# Install kachery-cloud
RUN pip install kachery-cloud==0.4.9

# Install spikeinterface
RUN pip install spikeinterface==0.100.6

# Install lindi from source
RUN git clone https://github.com/neurodatawithoutborders/lindi.git && \
    cd lindi && \
    git checkout dev10 && echo "4" && \
    pip install -e .

# Install sortingview
RUN pip install sortingview==0.13.3

# Install spikeinterface-pipelines from source, for now
RUN git clone https://github.com/SpikeInterface/spikeinterface_pipelines.git && \
    cd spikeinterface_pipelines && \
    # git checkout dev && \
    pip install -e .

# Install neuroconv
RUN pip install neuroconv==0.4.8

# Install mountainsort5
RUN pip install mountainsort5==0.5.6

# Copy files into the container
RUN mkdir /app
COPY *.py /app/
COPY recording_summary_processor/*.py /app/recording_summary_processor/
COPY recording_summary_processor/helpers/*.py /app/recording_summary_processor/helpers/
COPY mountainsort5_processor/*.py /app/mountainsort5_processor/
