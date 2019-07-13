# Deploy project into:
# https://pypi.org/project/csvql/

# rm -r /build
# rm -r /csvql.egg-info
# rm -r /dist

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*
