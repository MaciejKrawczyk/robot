# software manual

## route

### /exec-program


```
type => commands[]

where:
type command_sleep = {
    "name": "sleep",
    "body": {
        "seconds": float
    },
}

type command_move = {
    "name": "move",
    "body": {
        "x": float,
        "y": float,
        "z": float
    }
}
```


### websocket