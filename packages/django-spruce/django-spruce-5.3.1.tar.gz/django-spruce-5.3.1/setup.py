from setuptools import setup

setup(
    name='django-spruce',
    version='5.3.1',
    packages=['spruce_ui'],
    include_package_data=True,
    install_requires=[
        'Django',
        'pyarmor',
        'requests',
        # 添加其他依赖
    ],
    author='江绿岸',
    author_email='jlarjjszx@tom.com',
    zip_safe=False,
)
