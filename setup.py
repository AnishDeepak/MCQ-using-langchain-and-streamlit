from setuptools import find_packages,setup

setup(
    name='mcq_generator',
    version='0.0.1',
    author='Anish Deepak',
    author_email='anishdeepak34@gmail.com',
    install_requires=["langchain","streamlit","python-dotenv","PyPDF2",'anthropic','huggingface-hub','transformers'],
    packages=find_packages()
)