# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from io import open


def readme():
    with open('README.md', encoding="utf-8") as f:
        README = f.read()
    return README


setup(
    name='docx_tbx',
    # packages=['docx_tbx',
    #           'docx_tbx.dml',
    #           'docx_tbx.enum',
    #           'docx_tbx.image',
    #           'docx_tbx.opc',
    #           'docx_tbx.opc.parts',
    #           'docx_tbx.oxml'
    #           'docx_tbx.oxml.text',
    #           'docx_tbx.parts',
    #           'docx_tbx.styles',
    #           'docx_tbx.templates',
    #           'docx_tbx.text'],
    packages=find_packages(),
    package_data={'docx_tbx.templates': ['*.xml', '*.docx']},
    # package_dir={'paddleocr': ''},
    include_package_data=True,
    # entry_points={"console_scripts": ["paddleocr= paddleocr.paddleocr:main"]},
    version='0.0.2',
    # install_requires=load_requirements(['requirements.txt', 'ppstructure/recovery/requirements.txt']),
    license='MIT License',
    description='Based on python-docx-0.8.11, modifications have been made to allow the insertion of text boxes in Word documents.',
    long_description=readme(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/PaddlePaddle/PaddleOCR',
    # download_url='https://github.com/PaddlePaddle/PaddleOCR.git',
    # keywords=[
    #     'ocr textdetection textrecognition paddleocr crnn east star-net rosetta ocrlite db chineseocr chinesetextdetection chinesetextrecognition'
    # ],
    classifiers=[
        'Intended Audience :: Developers', 'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8', 'Topic :: Utilities'
    ], )
