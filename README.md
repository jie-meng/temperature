## Install

pip install -Ur requirements.txt

## Prepare data

Put images under __images/{subdir}/__. Add a related config file with the same name as image file but extension with 'txt'. Put the __ruler_min__ and __ruler_max__ value in it.

Example:

```
ruler_min=20.2
ruler_max=24.1
```

## Execute

python cli.py
