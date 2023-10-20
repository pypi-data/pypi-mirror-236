from setuptools import setup, find_packages

setup(
    name='jaen_mod',
    version='0.0.6',
    description='Module for assisting JAEN project system written by ssim',
    author='ssim',
    author_email='sjk3037@gmail.com',
    url='http://git.jaen.kr/ssim/jaen_mod',
    install_requires=['pandas'],
    packages=find_packages(exclude=[]),
    keywords=['ssim', 'jaen', 'jaen_mod'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)