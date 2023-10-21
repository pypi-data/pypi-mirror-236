from setuptools import setup

setup(name = 'hebwatch',
      version = '0.3',
      description = 'this library calculates the relative hour clock from the jewish talmud',
      author = 'Tal Amar',
      packages = ['hebwatch'],
      zip_safe = False,
      include_package_data=True,
          install_requires=[
        'suntime',
        'pyyaml',
    ]
)
