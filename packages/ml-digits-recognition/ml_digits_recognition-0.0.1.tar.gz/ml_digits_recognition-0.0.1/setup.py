import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='ml_digits_recognition',
        version='0.0.1',
        author='Martin Braquet',
        description='A simple digits recognition neural network',
        url='https://github.com/MartinBraquet/ml-digits-recognition',
        packages=setuptools.find_packages(),
        data_files=[('', ['ml_digits_recognition/model_precise.pt'])],
        long_description=open('README.md').read(),
        python_requires='>=3.7',
        license='MIT',
        install_requires=[
            'torch',
            'torchvision',
            'Pillow',
        ]
    )
