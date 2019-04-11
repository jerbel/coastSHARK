Plugin Packaging
================

*coastSHARK* is supposed to run as a plugin for serverSHARK.
To build the .tar for serverSHARK the following steps have to be executed.

Create Plugin
-------------

.. code-block:: bash
    
    cd ./plugin_packaging

    # create schema.json for the packaging
    python build_schema.py

    # create the coastSHARK_plugin.tar
    ./build_plugin.sh

