import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="XenonUI",
    version="1.1.2",
    author="Junxiang Huang",
    author_email="huangjunxiang@mail.ynu.edu.cn",
    description="XUI is a page management GUI framework for python that is based on the platform-independent GUI package tinker.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/wacmkxiaoyi/Xenon-UI", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)