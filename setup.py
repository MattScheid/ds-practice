from setuptools import setup, find_packages

setup(
    name="interview-practice",
    version="0.1.0",
    description="A Jupyter-based interview question practice tool",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "jupyter",
        "notebook",
        "ipython",
        "IPython",
        "sentence-transformers",
    ],
    extras_require={
        "dev": ["pytest"],
    },
)
