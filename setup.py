from setuptools import setup, find_packages

setup(
    name='flask_login_apple',
    version='0.1.0',
    description='A Flask extension to support Sign in with Apple',
    author='Pradip Bhattarai',
    author_email='contact@pradeepbhattarai.me',
    url='https://github.com/prdp1137/flask_apple_login',
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
