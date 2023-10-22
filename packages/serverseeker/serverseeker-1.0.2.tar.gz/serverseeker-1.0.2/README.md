# ServerSeeker Python Wrapper

This is a Python wrapper for [ServerSeeker](https://serverseeker.net/) designed to be used as a [CLI](https://en.wikipedia.org/wiki/Command-line_interface). The original API was written by a user going by [DAM](https://damcraft.de/) and the [API documentation](https://serverseeker.net/docs) can be found here: [Link](https://serverseeker.net/docs)

## Installation
Installation by `pip` will be supported in the near future. However, for right now: you can download the `.exe` file found on the [releases](https://github.com/Igyeom/ServerSeeker/releases) tab and drag it to a folder that is added to the PATH environment variable.<br><br>

## Quickstart
### API Key
`serverseeker auth <api_key>` will configure your API key. This information is stored locally and the credentials are not sent to anybody.<br><br>

### `/whereis`
Now try `serverseeker whereis <username> [--copy]` to search players via username or `serverseeker whereis <uuid> --uuid [--copy]` to search players via UUID (remember the `--uuid` option!)<br><br>


For example: `serverseeker whereis 069a79f4-44e9-4726-a5be-fca90e38aaf5 --uuid` which can be substituted with `serverseeker whereis Notch`

You can append the `--copy` option to any API call command (i.e. all commands except for `serverseeker auth <api_key>`) to copy the response to your clipboard if it gets very long.

### `/server_info`
Now try `serverseeker info <ip> <port: 25565> [--copy]`. The `port` argument is 25565 by default, therefore it is optional.<br><br>

For example: `serverseeker info 109.123.240.84 --copy` will copy the returned information about `109.123.240.84:25565` to your clipboard. 

### `/servers`
Now try `serverseeker search <online_players: [0, "inf"]> <max_players: [0, "inf"]> <protocol: 764> <online_after: 0> <software: "any"> <country_code: ""> <description: ""> [--cracked] [--copy]`. Append the `--cracked` option to search for cracked servers