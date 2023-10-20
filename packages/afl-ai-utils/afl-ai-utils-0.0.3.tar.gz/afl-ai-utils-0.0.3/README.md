# afl-ai-utils
    rm -rf build dist 
    python3 setup.py sdist bdist_wheel
    twine upload --repository pypi dist/* 