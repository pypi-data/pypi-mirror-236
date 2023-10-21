# Mesos CLI

## Prerequisites

Make sure you have python 3.6 or newer installed
on your system before you begin.

## How to install 

```bash

pip install avmesos-cli

```

## Setting up your configuration

In order to use this tool, you will need to create a
configuration file in your home directory under
`~/.mesos/config.toml`. A template for this config can be
seen below:

```
# The `plugins` is an array listing the absolute paths of the
# plugins you want to add to the CLI.
plugins = [
  "</absolute/path/to/plugin-1/directory>",
  "</absolute/path/to/plugin-2/directory>"
]

# The `master` is a field that has to be composed of an
# `address` or `zookeeper` field, but not both. For example:
[master]
  address = "10.10.0.30:5050"
  principal = "username"
  secret = "password"

[agent]
  ssl = true
  ssl_verify = false
  principal = "username"
  secret = "password"
  timeout = 5
```

You can override the location of this configuration file using
the environment variable `MESOS_CLI_CONFIG`.

## How to use it

```bash
$ mesos-cli 

Mesos CLI

Usage:
  mesos (-h | --help)
  mesos --version
  mesos <command> [<args>...]

Options:
  -h --help  Show this screen.
  --version  Show version info.

Commands:
  agent      Interacts with the Mesos agents
  config     Interacts with the Mesos CLI configuration file
  framework  Interacts with the Mesos Frameworks
  task       Interacts with the tasks running in a Mesos cluster

See 'mesos help <command>' for more information on a specific command.

```
