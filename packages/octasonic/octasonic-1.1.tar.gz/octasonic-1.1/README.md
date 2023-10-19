# Python library for the Octasonic Breakout board

Python library for interacting with the [Octasonic HC-SR04 Breakout](https://www.tindie.com/products/andygrove73/octasonic-8-x-hc-sr04-ultrasonic-breakout-board/)

## Building

```shell
python -m venv venv
python -m pip install build twine
python -m build
```

## Publish to TestPyPi

```shell
twine check dist/*
twine upload -r testpypi dist/*
```

## Publish to PyPi

```shell
twine check dist/*
twine upload dist/*
```
