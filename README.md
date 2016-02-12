# rdb-fullstack
## Requirements
- Python 2.7
- Vagrant VM

## Running

```
  $ cd vagrant
  $ vagrant up
  $ vagrant ssh
vm$ cd /vagrant/tournament/
vm$ psql -f tournament.sql
vm$ python tournament_tester.py
```

## Using the tournament api
To use the api in your own work, simply add `from tournament import *` to the bottom of your import list and place the `tournament.sql` in the same folder as your `tournament.py` file.
