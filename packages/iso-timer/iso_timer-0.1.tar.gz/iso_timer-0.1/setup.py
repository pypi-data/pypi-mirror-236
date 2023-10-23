from setuptools import setup, find_packages

setup(
    name="iso_timer",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "rich >= 13.6.0",
        # 你的依赖包列表，例如：
        # "matplotlib >= 2.2.0"
    ],
)
