To have the project running in your local:
```console
make docker/run
```
Admin will be at http://localhost:8000/admin/ and you can access it through `admin 12345`

To send a broadcast message to all chats with a photo you need to use the action `Send banner message`
It doesn't matter which chats you select, the action would send the message to all chats anyway.

![admin.png](admin.png)

To run unit tests you can do:
```console
make docker/tests
```

To create fake chats and messages, use the following command (change `total` argument to your liking)
```console
make docker/create-fake-chats total=1000
```
