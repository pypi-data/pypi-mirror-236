from setuptools import setup, find_packages
setup(
    name = 'scfoundation',
    version = '0.0.1',
    description = 'General API for all foundation models in single-cell genomics.',
    author = 'Yanshuo Chen',
    author_email = 'poseidonchan@icloud.com',
    url = 'https://github.com/poseidonchan/scFoundationModels',
    license = 'GPL-3.0 License',
    packages = find_packages(),
    python_requires='>=3.7.1,<3.8',
    platforms = 'any',
    install_requires = [
        'torch>=1.13.1',
        'numpy>=1.21.6',
        'anndata>=0.8.0',
        'scanpy>=1.9.3',
        'anndata>=0.7.6',
        'tqdm>=4.65.0',
        'scikit-learn>=1.0.2',
    ],
)