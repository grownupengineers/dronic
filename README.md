# Dronic

**TODO**: document (better)

## Installing (development)

Setup a virtual env and install it in development mode

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

And run dronic as `dronic-cli`.

For the podman plugin, for some reason it may not be able to connect to the
socket for lack of permissions (or whatever). A solution can be to enable the
podman user socket `systemctl --user start podman.socket`.


## Architecture

### CLI vs Agent

Dronic can run in one of two modes: _CLI_ (or runner) and _Agent_.

The sole difference between the two modes is that while the _CLI_ will execute
the steps from the start, the _Agent_ will wait for connections which in turn
will request that specific stages be run.

One _instance_, when wishing to execute a stage in an _Agent_, will connect to
it and request that that stage be executed. The logs will then be streamed back
to the caller.

> Is it mentioned _"instance"_ because _Agents_ may invoke others _Agents_.

### Plugins

Plugins allow to extend _dronic_ with more features and capabilities.

> As the type of plugins may change faster than the documentation is updated,
> check `dronic/plugin.py` for them.

Each type of plugin follows a specific interface and lifecycle. Usually it
involves initialization, followed by calls to its main interface, ending with a
finalization.

#### Discovery

> As of the time of writing, this package exposes some plugins. Check `setup.py`
> for an example on how to export them.

They are discovered by the setuptools' (or whatever python is using these days)
_entry_points_, more specifically, the `dronic.plugin` entrypoint.

Each entry should point to a class that implements a plugin type.

### Execution

#### Discovery

When starting the _instance_, the pipeline script will be _executed_, gathering
the declared stages.

The final stages will be mostly linear.

_Parallel_ and _remote_ function as a kind of "stage gatherers". They appear to
the top level list of stages as a single stage, but will execute multiple stages
inside. This way, the overall stages will form a tree.

> All stages should be declared on the first _execution_ of the pipeline script.
> It is unclear/undefined what happens if the execution of stages declare other
> stages. See `jobs/test_inner.py` for example.

#### Execution

Each stage will then be executed. Unless modified by `parallel`, they will be
executed linearly.

If a stage raises an exception or the return value of a stage is non _None_ and
evaluates to _false_, the stage and pipeline are marked as failing and are
finished.

