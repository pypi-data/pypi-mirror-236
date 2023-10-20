from setuptools import find_packages, setup

PACKAGE_NAME = "tool_for_enabled_by"

setup(
    name=PACKAGE_NAME,
    version="0.0.3",
    description="This is a tool to test enabled_by",
    packages=find_packages(),
    entry_points={
        "package_tools": ["my_tools = tool_for_enabled_by.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
