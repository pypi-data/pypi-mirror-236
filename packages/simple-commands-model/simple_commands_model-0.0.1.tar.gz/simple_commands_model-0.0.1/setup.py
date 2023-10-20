from setuptools import setup, find_packages

setup(
    name="simple_commands_model",
    version="0.0.1",
    description="simple_commands_model",
    python_requires=">=3.9",
    
    packages=[
        'simple_commands_model',
        'simple_commands_model/tf',
        'simple_commands_model/image_process'
    ],
    include_package_data=True,
    install_requires=[
        'tensorflow',
        'simple_commands'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
