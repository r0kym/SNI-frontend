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
- [x] `groups` add a full group management
  - [ ] Allow for existing characters to be selected when adding members (auto-completion)
  - [ ] When adding a new group, display sheet page rather than going back to main list
- [x] `coalitions` add a full coalition management
  - [ ] Allow for existing alliances to be selected when adding to coalition (auto-completion)
  - [ ] When adding a new coalition, display sheet page rather than going back to main list
- [x] `teamspeak` add a full teamspeak management
- [ ] `alliance` add alliance management

# Web config:

No idea how to do it atm, come back later pls ^-^

# Docker initialization

get Pumba:
```sh
git clone https://github.com/altaris/pumba.git
```

Create the container's volume:

```sh
docker volume create pumba-test-volume
```

Build the container:

```sh
docker build -t pumba .
```

Copy utils.py to container:

```sh
docker cp /dest/to/utils.py pumba-test-volume:/usr/src/app/
```

Run the docker (need to fix port assignment):

```sh
docker run --rm \
    --env "GIT_URL=https://github.com/r0kym/SNI-frontend.git" \
    --env "GIT_BRANCH=master" \
    --env "PYTHON_MAIN=manage.py runserver" \
    --volume "pumba-test-volume:/usr/src/app/" \
    --name "SNI-frontend" \
    --net=host \
    altaris/pumba
```
