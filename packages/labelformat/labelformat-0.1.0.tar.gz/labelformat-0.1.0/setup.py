# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['labelformat', 'labelformat.cli', 'labelformat.formats', 'labelformat.model']

package_data = \
{'': ['*']}

install_requires = \
['pillow', 'pyyaml', 'tqdm']

entry_points = \
{'console_scripts': ['labelformat = labelformat.cli.cli:main']}

setup_kwargs = {
    'name': 'labelformat',
    'version': '0.1.0',
    'description': 'Computer vision label and prediction conversion',
    'long_description': '# Labelformat - Label Conversion, Simplified\n\nAn open-source tool to seamlessly convert between popular computer vision label formats.\n\n**Why Labelformat:** Popular label formats are sparsely documented and store different\ninformation. Understanding them and dealing with the differences is tedious\nand time-consuming. Labelformat aims to solve this pain.\n\n**Supported Tasks and Formats:**\n- object-detection\n    - [COCO](https://cocodataset.org/#format-data)\n    - [KITTI](https://github.com/bostondiditeam/kitti/blob/master/resources/devkit_object/readme.txt)\n    - [Lightly](https://docs.lightly.ai/docs/prediction-format#prediction-format)\n    - [PascalVOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#devkit)\n    - [YOLOv8](https://docs.ultralytics.com/datasets/detect/)\n    - [Labelbox](https://docs.labelbox.com/reference/label-export) (input only)\n- instance-segmentation\n    - [COCO](https://cocodataset.org/#format-data)\n    - [YOLOv8](https://docs.ultralytics.com/datasets/segment/)\n\n\n> **Note**\n> Labelformat is a young project, contributions and bug reports are welcome. Please see [Contributing](#contributing) section below.\n\n\n## Installation\n\n```shell\npip install labelformat\n```\n\n## Usage\n\n### CLI\n\nExample command:\n```shell\nlabelformat convert \\\n    --task object-detection \\\n    --input-format coco \\\n    --input-file coco-labels/train.json \\\n    --output-format yolov8 \\\n    --output-file yolo-labels/data.yaml \\\n    --output-split train\n```\n\n#### Command Arguments\n\nList the available tasks with:\n```console\n$ labelformat convert --help\nusage: labelformat convert [-h] --task\n                           {instance-segmentation,object-detection}\n\nConvert labels from one format to another.\n\noptional arguments:\n  -h, --help\n  --task {instance-segmentation,object-detection}\n```\n\nList the available formats for a given task with:\n```console\n$ labelformat convert --task object-detection --help\nusage: labelformat convert [-h] --task\n                           {instance-segmentation,object-detection}\n                           --input-format\n                           {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                           --output-format\n                           {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n\nConvert labels from one format to another.\n\noptional arguments:\n  -h, --help\n  --task {instance-segmentation,object-detection}\n  --input-format {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                        Input format\n  --output-format {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                        Output format\n```\n\nSpecify the input and output format to get required options for specific formats:\n```console\n$ labelformat convert \\\n          --task object-detection \\\n          --input-format coco \\\n          --output-format yolov8 \\\n          --help\nusage: labelformat convert [-h] --task\n                           {instance-segmentation,object-detection}\n                           --input-format\n                           {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                           --output-format\n                           {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                           --input-file INPUT_FILE --output-file OUTPUT_FILE\n                           [--output-split OUTPUT_SPLIT]\n\nConvert labels from one format to another.\n\noptional arguments:\n  -h, --help\n  --task {instance-segmentation,object-detection}\n  --input-format {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                        Input format\n  --output-format {coco,kitti,labelbox,lightly,pascalvoc,yolov8}\n                        Output format\n\n\'coco\' input arguments:\n  --input-file INPUT_FILE\n                        Path to input COCO JSON file\n\n\'yolov8\' output arguments:\n  --output-file OUTPUT_FILE\n                        Output data.yaml file\n  --output-split OUTPUT_SPLIT\n                        Split to use\n```\n\n### Code\n```python\nfrom pathlib import Path\nfrom labelformat.formats import COCOObjectDetectionInput, YOLOv8ObjectDetectionOutput\n\nlabel_input = COCOObjectDetectionInput(\n    input_file=Path("coco-labels/train.json")\n)\nYOLOv8ObjectDetectionOutput(\n    output_file=Path("yolo-labels/data.yaml"),\n    output_split="train",\n).save(label_input=label_input)\n```\n\n## Contributing\n\nIf you encounter a bug or have a feature suggestion we will be happy if you file a GitHub issue.\n\nWe also welcome contributors, please submit a PR.\n\n### Development\n\nThe library targets python 3.7 and higher. We use poetry to manage the development environment.\n\nHere is an example development workflow:\n\n```bash\n# Create a virtual environment with development dependencies\npoetry env use python3.7\npoetry install\n\n# Make changes\n...\n\n# Autoformat the code\npoetry run make format\n\n# Run tests\npoetry run make all-checks\n```\n\n## Maintained By\n[Lightly](https://www.lightly.ai) is a spin-off from ETH Zurich that helps companies \nbuild efficient active learning pipelines to select the most relevant data for their models.\n\nYou can find out more about the company and it\'s services by following the links below:\n\n- [Homepage](https://www.lightly.ai)\n- [Web-App](https://app.lightly.ai)\n- [Lightly Solution Documentation (Lightly Worker & API)](https://docs.lightly.ai/)\n',
    'author': 'Lightly.ai',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
