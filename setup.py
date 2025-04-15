from setuptools import setup, find_packages

setup(
    name='f1_strategy_optimizer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'xgboost',
        'tensorflow',
        'flaml',
        'fastf1',
        'tqdm'
    ],
    author='Pranav Vats',
    description='F1-PitStop-Strategy-Optimizer-using-ML',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)
