from setuptools import setup, find_packages

# Read the content of README.md into long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jaxlob',
    version='0.14',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'pandas',
        'numpy',
        'scipy',
        'six',
        'wheel',
        'jax[cuda]==0.4.11',
        'jaxlib==0.4.11+cuda11.cudnn86',
        'distrax',
        'brax',
        'chex',
        'flax',
        'optax',
        'gym',
        'notebook',
        'matplotlib',
        'tqdm',
        'gymnax',
        'jupyter',
        'ipython',
        'wandb'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

