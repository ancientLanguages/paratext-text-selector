from setuptools import setup

f = open("README.md", 'r')

long_desc = f.read()

f.close()

setup(
    name="paratext-text-selector",
    version="0.2",
    description="Python tool for selecting books and portions of books created with Paratext",
    url="",
    long_description= long_desc,
    long_description_content_type='text/markdown',
    license="MIT",
    packages=["pt_text_selector"],
    entry_points={"console_scripts": ["set-texts = pt_text_selector.main:main",],},
    install_requires=["configparser",],
    zip_safe=False,
)
