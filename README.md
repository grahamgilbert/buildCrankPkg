buildCrankPkg
========

``buildCrankPkg.py`` is a script that will build an Apple package that contains everything you need to use [crankd](https://github.com/acdha/pymacadmin) on your clients.

# Usage

## Preparation

I recommend reading my [blog post](http://grahamgilbert.com/blog/2013/07/12/using-crankd-to-react-to-network-events/) on the different parts that make up this package to get a deeper understanding. You need to copy a few items into the provided directories before running the script.

### crankd

You should put your actual python script in here. In the example post linked above, this would be ``CrankTools.py``. The contents of this directory will be installed to ``/Library/Application Support/crankd``.

### LaunchDaemons

If you want to use your own LaunchDaemon, you should put it here. One has been provided that should cover most use cases. The files here will be installed to ``/Library/LaunchDaemons``.

### Preferences

Shockingly, this is where you should put your preference file that will tell crankd what to run. An example to run the CrankTools.py script is in the blog post above.


## Options

The script takes a few options you can pass to it.

``--repopath``: This should be a file path to  a clone of the PyMacAdmin repository that  already exists on disk. You should use this is you've made customisations to crankd that only exist on your Mac. Optional.

``--remoterepo``: The address of a git repository that isn't the [default](https://github.com/acdha/pymacadmin). This is only used if ``--repopath`` isn't specified.

If neither ``--remoterepo`` nor ``--repopath`` are passed, the [main repository](https://github.com/acdha/pymacadmin) will be used.

``--version``: The version number of the package you're building. Defaults to 1.0 if not specified.

``--identifier``:  The identifier of the package. Defaults to com.grahamgilbert.crankd

## Building the package

Once all your files are in place, simply call the script using ``sudo``.

```
cd ~/src/CrankPkg
sudo ./buildCrankPkg.py --repo ~/src/PyMacAdmin --version 2.1 --identifier com.example.crankd
```