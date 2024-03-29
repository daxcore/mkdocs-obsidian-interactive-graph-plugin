import os

from setuptools import setup, find_packages

def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mkdocs-obsidian-interactive-graph-plugin',
    description='A MkDocs plugin that generates a obsidian like interactive graph',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    url='https://github.com/daxcore/mkdocs-obsidian-interactive-graph-plugin',
    author='daxcore',
    author_email='300ccda6-8d43-4f23-808e-961e653ff7d6@anonaddy.com',
    license='MIT',
    python_requires='>=3.6',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['mkdocs-material'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'obsidian-interactive-graph = obsidian_interactive_graph.plugin:ObsidianInteractiveGraphPlugin'
        ]
    }
)
