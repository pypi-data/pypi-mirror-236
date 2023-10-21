from setuptools import setup, find_packages

setup(
    name="rabbitmq_toolkit",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'pika',
    ],
    python_requires='>=3.6',  # example version, adjust according to your compatibility
    author="Infinity Team",
    description="A streamlined toolkit for efficient RabbitMQ operations.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/your_username/rabbitmq_toolkit",  # replace with your repository link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # replace with your License
        "Operating System :: OS Independent",
    ],
    keywords="rabbitmq, messaging, queue, producer, consumer",
)
