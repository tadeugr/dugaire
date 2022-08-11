Quickly build custom Docker images for local development without having
to write Dockerfiles.

.. figure:: https://github.com/tadeugr/dugaire/blob/master/docs/assets/tty.gif?raw=true
   :alt: dugaire

   dugaire

|PyPI| |Python| |Code style: black| |test| |publish| |codecov|
|Documentation Status| |FOSSA Status|

*Examples*

Install ``vim`` and ``curl`` using ``apt-get``.

::

   docker run -it --rm $(dugaire build --apt=vim,curl)

Install ``vim``, ``python3``, ``pip3`` using ``apt-get`` and install
``ansible`` using ``pip3``.

::

   docker run -it --rm $(dugaire build --apt=vim,python3-pip --pip3=ansible)

Install ``kubectl`` binary version ``v1.15.0`` (use
``--with-kubectl=latest`` to install the latest version).

::

   docker run -it --rm $(dugaire build --apt=vim --with-kubectl=1.15.0)

Do not build the image and just print the Dockerfile:

::

   dugaire build --apt=vim,curl --with-kubectl=latest --output=dockerfile --dry-run

Install (on Linux)
==================

Using pip (recommended)
-----------------------

::

   pip install dugaire

From source
-----------

Clone this repository.

::

   git clone https://github.com/tadeugr/dugaire.git

``cd`` to its directory.

::

   cd dugaire

Install it (requires ``pip``).

::

   make install

You should have the command available.

::

   dugaire build --help

Enable autocomplete
===================

To enable autocomplete for your current terminal session, run:

::

   eval "$(_DUGAIRE_COMPLETE=source dugaire)"

*Follow the instructions bellow to permanently enable autocomplete.*

bash
----

::

   echo 'eval "$(_DUGAIRE_COMPLETE=source dugaire)"' >> ~/.bashrc

zsh
---

::

   echo 'eval "$(_DUGAIRE_COMPLETE=source dugaire)"' >> ~/.zshrc

Usage
=====

::

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
     --with-azurecli, --with-az <latest>
                                     Install Azure CLI. Examples: --with-
                                     azurecli=latest / For older versions, use
                                     pip3: --apt=python3-pip --pip="azure-
                                     cli==2.2.0"
     --with-kubectl <latest|semantic versioning>
                                     Install kubectl. Examples: --with-
                                     kubectl=latest / --with-kubectl=1.17.0
     --with-terraform <latest|semantic versioning>
                                     Install Terraform. Examples: --with-
                                     terraform=latest / --with-terraform=0.15.5
     --with-velero <latest|semantic versioning>
                                     Install velero. Examples: --with-
                                     velero=latest / --with-velero=1.5.2
     --force                         Ignore Docker cache and build from scratch.
     --dry-run                       Do not build image.
     --output [image.id|image.id.short|image.name|dockerfile]
                                     Command output options.  [default:
                                     image.id.short]
     --help                          Show this message and exit.

Supported features
==================

Base images
-----------

====== =================================
Distro Tested with
====== =================================
ubuntu ``ubuntu:18.04`` ``ubuntu:20.04``
====== =================================

*You may use base images that were built from the tested images.*

Package/Dependency managers
---------------------------

apt-get
~~~~~~~

You can install any package using ``apt``. Use a comma separated (no
blank space) list of packages you want to install. Example:
``--apt=wget,iputils-ping``.

pip3
~~~~

**WARNING** to use ``pip3`` you must explicitly install ``pip3`` using
``apt``: ``--apt=python3-pip``.

You can install any package using ``pip3``. Use a comma separated (no
blank space) list of packages you want to install. Example:
``--pip3=jinja2,pyyaml``.

Applications
------------

azure-cli
~~~~~~~~~

Install Azure Command Line Interface.

Requirements
^^^^^^^^^^^^

To install specific versions (not *latest*), use ``pip3`` as follows
``--apt=python3-pip --pip3="azure-cli==<semantic versioning>"``

Options
^^^^^^^

``--with-azurecli=latest`` to install the latest version.

``--apt=python3-pip --pip3="azure-cli==2.2.0"`` *(example)* to install
specific versions.

See all versions available
`here <https://github.com/Azure/azure-cli/releases>`__.

Covered by automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

*You may install any version available. The commands bellow only
describes versions included in the automated testsß.*

::

   dugaire build --with-azurecli=latest
   dugaire build --from=ubuntu:20.04 --apt=python3-pip --pip3="azure-cli==2.14.2"

kubectl
~~~~~~~

Install kubectl.

.. _requirements-1:

Requirements
^^^^^^^^^^^^

No requirements.

.. _options-1:

Options
^^^^^^^

``--with-kubectl=latest`` to install the latest version.

``--with-kubectl=1.17.0`` *(example)* to install specific versions.

See all versions available
`here <https://github.com/kubernetes/kubectl/releases>`__.

.. _covered-by-automated-tests-1:

Covered by automated tests
^^^^^^^^^^^^^^^^^^^^^^^^^^

*You may install any version available. The commands bellow only
describes versions included in the automated testsß.*

::

   dugaire build --from=ubuntu:20.04 --with-kubectl=latest
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.18.0
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.17.0
   dugaire build --from=ubuntu:18.04 --with-kubectl=1.16.0
   dugaire build --from=ubuntu:18.04 --with-kubectl=1.15.0

velero
~~~~~~

Install velero.

.. _requirements-2:

Requirements
^^^^^^^^^^^^

``--with-velero`` requires ``--with-kubectl``.

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

*You may install any version available. The commands bellow only
describes versions included in the automated testsß.*

::

   dugaire build --from=ubuntu:20.04 --with-kubectl=latest --with-velero=latest
   dugaire build --from=ubuntu:20.04 --with-kubectl=1.17.0 --with-velero=1.5.2

Useful Docker commands
======================

List images created with dugaire
--------------------------------

::

   docker images -f label='builtwith=dugaire'

Delete all images created with dugaire
--------------------------------------

::

   docker rmi -f $(docker images -aq -f label='builtwith=dugaire')

Known issues
============

RuntimeError: Python 3 was configured to use ASCII as encoding for the environment
----------------------------------------------------------------------------------

If you get an error like this one:

::

   RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment. Consult https://click.palletsprojects.com/python3/ for mitigation steps.

It is because ``dugaire`` uses Python3 and
`Click <https://github.com/pallets/click>`__, and according to Click “in
Python 3, the encoding detection is done in the interpreter, and on
Linux and certain other operating systems, its encoding handling is
problematic”. `Read
more <https://click.palletsprojects.com/en/5.x/python3/#python-3-surrogate-handling>`__.

Solution
~~~~~~~~

Setup your locale correctly, for example if you want to use
``en_US.UTF-8``, run:

::

   apt update && apt-get -y install locales
   locale-gen --purge en_US.UTF-8

   export LC_ALL="en_US.UTF-8"
   export LC_CTYPE="en_US.UTF-8"

   # Alternatively you can run: 
   #sudo dpkg-reconfigure locales

Then you should be able to run ``dugaire``.

Development
===========

.. _requirements-3:

Requirements
------------

-  ``pandoc`` https://pandoc.org/installing.html

Create a virtualenv

make install-dev

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
