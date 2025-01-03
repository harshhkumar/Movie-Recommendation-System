from setuptools import setup, find_packages

setup(
    name="movie-recommender",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'requests',
    ],
)