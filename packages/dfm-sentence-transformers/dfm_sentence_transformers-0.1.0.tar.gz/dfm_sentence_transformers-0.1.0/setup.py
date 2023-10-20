# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfm_sentence_trf', 'dfm_sentence_trf.tasks']

package_data = \
{'': ['*']}

install_requires = \
['catalogue>=2.0.0,<3.0.0',
 'confection>=0.1.0,<0.2.0',
 'datasets>=2.14.0,<3.0.0',
 'radicli>=0.0.25,<0.0.26',
 'sentence-transformers>=2.2.0,<3.0.0',
 'torch>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'dfm-sentence-transformers',
    'version': '0.1.0',
    'description': 'Module for finetuning dfm base-models to sentence transformers',
    'long_description': '# dfm-sentence-transformers\nCode for curating data and training sentence transformers for the Danish Foundation Models project.\n\n## Training\n\nInstall the CLI:\n\n```bash\npip install dfm_sentence_trf\n```\n\nWARNING: The package is not on PyPI yet, so this won\'t actually work as of yet.\n\n### Config system (_TODO_)\n\nYou have to specify basic model and training parameters, as well as all the tasks/datasets the model should be trained on.\n\n```\n[model]\nname="dfm-sentence-encoder-small-v1"\nbase_model="chcaa/dfm-encoder-small-v1"\ndevice="cpu"\n\n[training]\nepochs=5\nwarmup_steps=100\nbatch_size=120\n\n[tasks]\n\n[tasks.bornholmsk]\n@tasks="multiple_negatives_ranking"\nsentence1="da_bornholm"\nsentence2="da"\n\n[tasks.bornholmsk.dataset]\n@loaders="load_dataset"\npath="strombergnlp/bornholmsk_parallel"\n\n[tasks.hestenet]\n@tasks="multiple_negatives_ranking"\nsentence1="question"\nsentence2="answer"\n\n[tasks.hestenet.dataset]\n@loaders="load_dataset"\npath="some/local/path"\n\n```\n\nThen you can train a sentence transformer by using the `finetune` command.\n\n```bash\npython3 -m dfm_sentence_trf training.cfg --output_folder "output/"\n```\n\nYou can push the finetuned model to HuggingFace Hub:\n\n```bash\npython3 -m dfm_sentence_trf training.cfg --model_path "output/" --organization "chcaa"\n```\n\n## Tasks (_TODO_)\n\n### ContrastiveParallel (_TODO_)\n\nThe task uses a contrastive loss on a parallel corpus, where negative examples (aka. non-matching sentence pairs labelled with 0) are randomly sampled.\nYou can specify the dataset, and the number of negative samples for each positive sample. As well as basic training parameters.\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
