from setuptools import setup, find_packages
setup(
    zip_safe=False,
    name = "easy_profiler",
    version = "0.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'easyprofile = easyprofiler:main',
        ],
    }
)

