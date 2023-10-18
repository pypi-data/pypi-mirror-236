import os
import setuptools

name = "bbat"
version = "0.2.6"

def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires


setuptools.setup(
    name=name,
    version=version,
    author="zlge",
    author_email="test@test.com",
    description="",
    long_description="testModule",
    long_description_content_type="text",
    packages=setuptools.find_packages(),
    install_requires=_process_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["bbat = bbat.zcli:main"]},
)
