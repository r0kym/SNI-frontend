SNI - frontend part
==================

[SNI backend part](https://github.com/altaris/seat-navy-issue)

For now the homepage is displayed and you can press `login with eve online` to attempt a connection to the ESI through SNI.


# Dependencies:

Run:

```sh
virtualenv venv -p python3.8
. ./venv/bin/activate
pip install -r requirements.txt
```

# Set up:

Run:
```sh
cp utils.py.template utils.py
```

Fill th new `utils.py` with relevent informations

# Running:

```sh
python3 manage.py runserver
```

# Web config:

No idea how to do it atm, come back later pls ^-^
