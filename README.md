# Graph sandbox

A simple sandbox to demonstate how graph algorithms work.
__Available__:
- Dijkstra algorithm


## Run 

```sh
python -m venv env                          # create virtual enviorment
source env/bin/activate                     # activate virtual enviorment
python -m pip install -r requirements.txt   # install all dependencies
python main.py                              # run sandbox
```

## Control

- __LMB__ for drag n drop or create connections between graph vertices
- __RMB__ for creating new graph vertices on the field
- __MMB__ for set *start* and *end* 
- __Mouse wheel__ for change edge price
- __Red square on top left__ for delete vertices (with bugs)

## Future plans (TODO)
- Create `World` class for encapsulate vertices and and their price
- Improove main loop (now with lags)
- Add other algorithms and other graph types
