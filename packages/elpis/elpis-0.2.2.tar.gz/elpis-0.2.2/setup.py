# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elpis',
 'elpis.datasets',
 'elpis.models',
 'elpis.trainer',
 'elpis.transcriber',
 'elpis.utils']

package_data = \
{'': ['*']}

install_requires = \
['accelerate>=0.22.0,<0.23.0',
 'datasets>=2.6.1,<3.0.0',
 'evaluate>=0.4.0,<0.5.0',
 'jiwer>=3.0.3,<4.0.0',
 'librosa>=0.9.2,<0.10.0',
 'loguru>=0.6.0,<0.7.0',
 'pedalboard>=0.8.3,<0.9.0',
 'pympi-ling>=1.70.2,<2.0.0',
 'sounddevice>=0.4.6,<0.5.0',
 'torch>=2.0.0,!=2.0.1,!=2.1.0',
 'transformers>=4.34.0,<5.0.0']

setup_kwargs = {
    'name': 'elpis',
    'version': '0.2.2',
    'description': 'A library to perform automatic speech recognition with huggingface transformers.',
    'long_description': '# Elpis Core Library\n\nThe Core Elpis Library, providing a quick api to [:hugs: transformers](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=downloads)\nfor automatic-speech-recognition.\n\nYou can use the library to:\n\n- Perform standalone inference using a pretrained HFT model.\n- Fine tune a pretrained ASR model on your own dataset.\n- Generate text and Elan files from inference results for further analysis.\n\n## Documentation\n\nDocumentation for the library can be be found [here](https://coedl.github.io/elpis_lib/index.html).\n\n## Dependencies\n\nWhile we try to be as machine-independant as possible, there are some dependencies\nyou should be aware of when using this library:\n\n- Processing datasets (`elpis.datasets.processing`) requires `librosa`, which\n  depends on having `libsndfile` installed on your computer. If you\'re using\n  elpis within a docker container, you may have to manually install\n  `libsndfile`.\n- Transcription (`elpis.transcription.transcribe`) requires `ffmpeg` if your\n  audio you\'re attempting to transcribe needs to be resampled before it can\n  be used. The default sample rate we assume is 16khz.\n- The preprocessing flow (`elpis.datasets.preprocessing`) is free of external\n  dependencies.\n\n## Installation\n\nYou can install the elpis library with:\n`pip3 install elpis`\n\n## Usage\n\nBelow are some typical examples of use cases\n\n### Standalone Inference\n\n```python\nfrom pathlib import Path\n\nfrom elpis.transcriber.results import build_text\nfrom elpis.transcriber.transcribe import build_pipeline, transcribe\n\n# Perform inference\nasr = build_pipeline(pretrained_location="facebook/wav2vec2-base-960h")\naudio = Path("<to_some_audio_file.wav>")\nannotations = transcribe(audio, asr) # Timed, per word annotation data\n\nresult = build_text(annotations) # Combine annotations to extract all text\nprint(result)\n\n# Build output files\ntext_file = output_dir / "test.txt"\nwith open(text_file, "w") as output_file:\n    output_file.write(result)\n```\n\n### Fine-tuning a Pretrained Model on Local Dataset\n\n```python\nfrom pathlib import Path\nfrom typing import List\n\nfrom elpis.datasets import Dataset\nfrom elpis.datasets.dataset import CleaningOptions\nfrom elpis.datasets.preprocessing import process_batch\nfrom elpis.models import ElanOptions, ElanTierSelector\nfrom elpis.trainer.job import TrainingJob, TrainingOptions\nfrom elpis.trainer.trainer import train\nfrom elpis.transcriber.results import build_elan, build_text\nfrom elpis.transcriber.transcribe import build_pipeline, transcribe\n\nfiles: List[Path] = [...] # A list of paths to the files to include.\n\ndataset = Dataset(\n    name="dataset",\n    files=files,\n    cleaning_options=CleaningOptions(), # Default cleaning options\n    # Elan data extraction info- required if dataset includes .eaf files.\n    elan_options=ElanOptions(\n        selection_mechanism=ElanTierSelector.NAME, selection_value="Phrase"\n    ),\n)\n\n# Setup\ntmp_path = Path(\'...\')\n\ndataset_dir = tmp_path / "dataset"\nmodel_dir = tmp_path / "model"\noutput_dir = tmp_path / "output"\n\n# Make all directories\nfor directory in dataset_dir, model_dir, output_dir:\n    directory.mkdir(exist_ok=True, parents=True)\n\n# Preprocessing\nbatches = dataset.to_batches()\nfor batch in batches:\n    process_batch(batch, dataset_dir)\n\n# Train the model\njob = TrainingJob(\n    model_name="some_model",\n    dataset_name="some_dataset",\n    options=TrainingOptions(epochs=2, learning_rate=0.001),\n    base_model="facebook/wav2vec2-base-960h"\n)\ntrain(\n    job=job,\n    output_dir=model_dir,\n    dataset_dir=dataset_dir,\n)\n\n# Perform inference with pipeline\nasr = build_pipeline(\n    pretrained_location=str(model_dir.absolute()),\n)\naudio = Path("<to_some_audio_file.wav>")\nannotations = transcribe(audio, asr)\n\n# Build output files\ntext_file = output_dir / "test.txt"\nwith open(text_file, "w") as output_file:\n    output_file.write(build_text(annotations))\n\nelan_file = output_dir / "test.eaf"\neaf = build_elan(annotations)\neaf.to_file(str(elan_file))\n\nprint(\'voila ;)\')\n```\n',
    'author': 'Harry Keightley',
    'author_email': 'harrykeightley@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CoEDL/elpis_lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
