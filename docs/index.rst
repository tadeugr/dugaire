Quickly build custom Docker images for local development without having
to write Dockerfiles.

|PyPI| |Python| |Code style: black| |test| |publish| |codecov|
|Documentation Status| |FOSSA Status|

Examples
========

.. code:: bash

   # Build an image with vim and curl using apt-get
   docker run -it --rm $(dugaire build --apt=vim,curl)

   # Build an image with wget, and nano using apt-get and install latest azure-cli version using pip3.
   docker run -it --rm $(dugaire build --apt=wget,nano --pip3=azure-cli)

   # Build an image with latest kubectl version
   docker run -it --rm $(dugaire build --with-kubectl=latest)

   # Build an image with kubectl 1.15.0
   docker run -it --rm $(dugaire build --with-kubectl=1.15.0)

Install (on Linux)
==================

Using pip (recommended)
-----------------------

.. code:: bash

   pip install dugaire

From source
-----------

Clone this repository.

.. code:: bash

   git clone https://github.com/tadeugr/dugaire.git

``cd`` to its directory.

.. code:: bash

   cd dugaire

Install it (requires ``pip``).

.. code:: bash

   make install

You should have the command available.

.. code:: bash

   dugaire build --help

Usage
=====

.. code:: bash

   Usage: dugaire [OPTIONS] COMMAND [ARGS]...

     CLI tool to build and manage custom Docker images.

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     build    Build Docker images with custom packages.
     list     List images built with dugaire.
     rmi      Remove images built with dugaire.
     version  Show the version and exit.

dugaire build
-------------

.. code:: bash

   Usage: dugaire build [OPTIONS]

     Build Docker images with custom packages.

     Examples:

     Build an image and install vim and curl using apt-get.

     $ dugaire build --apt=vim,curl

     Build an image and install python3 using apt-get and ansible using pip3.

     $ dugaire build --apt=python3-pip --pip3=ansible

     Build an image and install the latest version of kubectl.

     $ dugaire build --with-kubectl=latest

   Options:
     --from <name:tag>               Base image (used in Dockerfile FROM).
                                     Example: --from=ubuntu:20.04  [default:
                                     ubuntu:18.04; required]
     --name <name:tag>               Image name. Example: --name="myimage:0.0.1"
                                     [default: random]
     --apt <pkg01|pkg01,pkg02>       Comma separeted list of packages (no blank
                                     space) to install using apt-get install.
                                     Requires a base image with apt-get. Example:
                                     -apt=curl,vim
     --pip3 <pkg01|pkg01,pkg02>      Comma separeted list of packages (no blank
                                     space) to install using pip3 install.
                                     WARNING: requires -apt=python3-pip. Example:
                                     -apt=python3-pip -pip3=ansible,jinja2
     --with-kubectl <latest|semantic versioning>
                                     Install kubectl. Examples: --with-
                                     kubectl=latest / --with-kubectl=1.17.0
     --with-terraform <latest|semantic versioning>
                                     Install terrafom. Examples: --with-
                                     terraform=latest / --with-terraform=0.15.5
     --with-velero <latest|semantic versioning>
                                     Install velero. Examples: --with-
                                     velero=latest / --with-velero=1.5.2
     --force                         Ignore Docker cache and build from scratch.
     --dry-run                       Do not build image.
     -o, --output [image.id|image.id.short|image.name|dockerfile]
                                     Command output options.  [default:
                                     image.id.short]
     --help                          Show this message and exit.

Enable autocomplete
===================

To enable autocomplete for your current terminal session, run:

.. code:: bash

   eval "$(_DUGAIRE_COMPLETE=source dugaire)"

Follow the instructions bellow to permanently enable autocomplete.

bash
----

.. code:: bash

   echo 'eval "$(_DUGAIRE_COMPLETE=source dugaire)"' >> ~/.bashrc

zsh
---

.. code:: bash

   echo 'eval "$(_DUGAIRE_COMPLETE=source dugaire)"' >> ~/.zshrc

Supported features
==================

Base images
-----------

Tested with:

-  ``ubuntu:20.04``

-  ``ubuntu:18.04``

..

   You may use base images that were built from the tested images.

Package/Dependency managers
---------------------------

apt-get
~~~~~~~

You can install any package using ``apt``.

Use a comma separated list (no blank space) of packages you want to
install.

Example:

.. code:: bash

   dugaire build --apt=wget,iputils-ping

pip3
~~~~

You can install any package using ``pip3``.

Use a comma separated list (no blank space) of packages you want to
install.

Use ``<package name>==<version>`` to install specific versions.

Example:

.. code:: bash

   dugaire build --pip3=jinja2,azure-cli==2.39.0

Applications
------------

kubectl
~~~~~~~

Options
^^^^^^^

``--with-kubectl=latest`` to install the latest version.

``--with-kubectl=1.17.0`` *(example)* to install specific versions.

See all versions available
`here <https://github.com/kubernetes/kubectl/releases>`__.

Covered by automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

   You may install any version available. The commands bellow only
   describes versions included in the automated tests.

.. code:: bash

   dugaire build --from=ubuntu:20.04 --with-kubectl=latest
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.18.0
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.17.0
   dugaire build --from=ubuntu:18.04 --with-kubectl=1.16.0
   dugaire build --from=ubuntu:18.04 --with-kubectl=1.15.0

terraform
~~~~~~~~~

.. _options-1:

Options
^^^^^^^

``--with-terraform=latest`` to install the latest version.

``--with-terraform=0.15.05`` *(example)* to install specific versions.

See all versions available
`here <https://releases.hashicorp.com/terraform/>`__.

.. _covered-by-automated-tests-1:

Covered by automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

   You may install any version available. The commands bellow only
   describes versions included in the automated tests.

.. code:: bash

   dugaire build --from=ubuntu:20.04 --with-terraform=latest
   dugaire build --from=ubuntu:20.04 --with-terraform=0.15.05

velero
~~~~~~

.. _options-2:

Options
^^^^^^^

``--with-velero=latest`` to install the latest version.

``--with-velero=1.5.2`` *(example)* to install specific versions.

See all versions available
`here <https://github.com/vmware-tanzu/velero/releases>`__.

.. _covered-by-automated-tests-2:

Covered by automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

   You may install any version available. The commands bellow only
   describes versions included in the automated tests.

.. code:: bash

   dugaire build --from=ubuntu:20.04 --with-kubectl=latest --with-velero=latest
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.17.0 --with-velero=1.5.2

License
=======

Product license
---------------

Apache License Version 2.0, January 2004. `Read
more. <https://github.com/tadeugr/dugaire/blob/master/LICENSE>`__

FOSSA scan overview
-------------------

|image1|

FOSSA Live Project report
-------------------------

The report is available
`here <https://app.fossa.com/reports/826e35e3-c1be-4f82-a260-da5b362aa83b>`__

.. |PyPI| image:: https://img.shields.io/badge/pypi-latest-blue
   :target: https://pypi.org/project/dugaire/
.. |Python| image:: https://img.shields.io/badge/python-3.7%20%7C%203.8-blue
   :target: https://pypi.org/project/dugaire/
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |test| image:: https://github.com/tadeugr/dugaire/workflows/test/badge.svg?branch=master
   :target: https://github.com/tadeugr/dugaire/actions?query=workflow%3Atest
.. |publish| image:: https://github.com/tadeugr/dugaire/workflows/publish/badge.svg
   :target: https://github.com/tadeugr/dugaire/actions?query=workflow%3Apublish
.. |codecov| image:: https://codecov.io/gh/tadeugr/dugaire/branch/develop/graph/badge.svg?token=Q6OURIL1ZK
   :target: https://codecov.io/gh/tadeugr/dugaire
.. |Documentation Status| image:: https://readthedocs.org/projects/dugaire/badge/?version=latest
   :target: https://dugaire.readthedocs.io/en/latest/?badge=latest
.. |FOSSA Status| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftadeugr%2Fdugaire.svg?type=shield
   :target: https://app.fossa.com/projects/git%2Bgithub.com%2Ftadeugr%2Fdugaire?ref=badge_shield
.. |image1| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Ftadeugr%2Fdugaire.svg?type=large
   :target: https://app.fossa.com/projects/git%2Bgithub.com%2Ftadeugr%2Fdugaire?ref=badge_large
