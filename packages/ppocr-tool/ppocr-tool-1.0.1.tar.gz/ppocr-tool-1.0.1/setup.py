from setuptools import setup, find_packages

setup(
    name="ppocr-tool",
    version="1.0.1",
    packages=find_packages('src'),
    package_dir={'ppocrtool': 'src/ppocrtool'},
    install_requires=[
        # 在这里列出你的依赖项，例如：
        'paddlepaddle',
        'paddleocr',
    ],
    entry_points={"console_scripts": ["ppocrtool = ppocrtool.ppocrtool:main"]},
)
