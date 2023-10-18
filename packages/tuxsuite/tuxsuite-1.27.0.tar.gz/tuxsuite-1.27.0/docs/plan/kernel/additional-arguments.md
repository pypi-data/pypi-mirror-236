
# callback

`--callback` is an optional argument to plan `submit` subcommand which POSTs JSON data that has
the status of the respective plan `build` or `test`, at the end of the respective `build` or `test` to the given URL. The
URL should be a valid http(s) link that accepts POST data.

[See Callbacks Reference, for more details](../../callbacks.md)
