from setuptools import setup
import pathlib
file = pathlib.Path(__file__).parent

README = (file / "README.md").read_text()

setup(
    name='opencv-cuda',
    version='0.0.2',
    packages=['opencv_cuda'],
    author="Nuhman Pk",
    author_email="nuhmanpk7@gmail.com",
    long_description = README,
    long_description_content_type = "text/markdown",
    description="opencv-cuda simplifies the installation of GPU-accelerated OpenCV with CUDA support for efficient image and video processing. ",
    license="MIT",
        classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/nuhmanpk/opencv-cuda",
    install_requires=[
        'numpy',
        'opencv-python'
    ],
    entry_points={
        'console_scripts': [
            'install_opencv_cuda = opencv_cuda.install_script:main'
        ]
    },
    python_requires=">=3.6",
)
