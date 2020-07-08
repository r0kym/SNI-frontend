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

```sh
python3 manage.py migrate
```
This will initialize Django Database

# Running:

```sh
python3 manage.py runserver
```

# TODO:
- [ ] check that the callback is working (should deploy a live version to do this)
- [x] `character/[player_id]` will diplay basic informations about a character
  - [ ] check if the character is registered and send 404 if he's not
  - [ ] fetch additional information through the ESI on the character
- [x] `character/` should display the list of characters registered
  - [x] add ways to order the list
  - [ ] deny the list for those that doesn't have a certain clearence level? (or just diplay a part of them)
- [ ] `groups` add a full group management
- [ ] `coalitions` add a full coalition management
- [ ] `teamspeak` add a full teamspeak management
- [ ] `alliance` add alliance management

# Web config:

No idea how to do it atm, come back later pls ^-^
