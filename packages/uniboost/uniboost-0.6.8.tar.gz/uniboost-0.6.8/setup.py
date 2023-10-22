from setuptools import setup, find_packages

setup(
    name='uniboost',
    version='0.6.8',
    packages=find_packages(),
    install_requires=[
        # your dependencies, e.g.,
        # 'requests',
    ],
    # other metadata
    author='MIT',
    description='AWS',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/your-package-name',  # if applicable
)
