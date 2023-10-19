Web Retriever
=============

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

.. image:: https://img.shields.io/pypi/v/web-retriever
   :alt: PyPI
   :target: https://pypi.org/project/web-retriever/

.. image:: ./resources/logo.png
   :alt: Web Retriever
   :align: center
   :width: 400px


Web Retriever is a robust Python-based API, designed to fetch and retrieve web resources on behalf of clients. It
provides an effective solution when direct internet access is not available to the client or when external resources
need to be explicitly defined, like in Envoy configurations.

#####
About
#####

Web Retriever is a robust API designed to facilitate the interaction between machine workloads and the Internet, acting
as an intermediary that handles requests and fetches the necessary online resources.

Web Retriever is built upon the concept of Plugin Oriented Programming, allowing it to be highly extensible and
customizable. It accepts one or more web resource locations to retrieve, serving as an intermediary that grants indirect
access to the web resources. This makes it an ideal solution in various scenarios, especially in environments where
clients have restricted or no direct internet access.

Furthermore, Web Retriever is particularly helpful in the context of Envoy configurations. In such settings, every
external web resource has to be manually defined within a configuration file. Web Retriever can simplify this process by
acting as a single point of reference for multiple web resources, thus reducing the complexity of the configuration.

A significant feature of Web Retriever is its Rule Engine, a powerful component that evaluates each request. It
determines whether to allow or deny requests based on specific, predefined criteria, enhancing the security and efficacy
of the interactions between machine workloads and the Internet.

Moreover, the Rule Engine is adept at manipulating request headers. It can dynamically insert essential elements, such
as API tokens, into the headers, eliminating the need to distribute sensitive information across various workloads,
thereby bolstering security protocols. Additionally, it can remove particular header information to prevent the
unintentional disclosure of internal or sensitive data to external sources. In essence, Web Retriever aims to optimize
the communication process between machine workloads and the Internet, ensuring it is secure, efficient, and effectively
managed.

Whether you need to fetch a single web page or retrieve multiple resources concurrently, Web Retriever offers a
reliable, efficient, and scalable solution. Its flexibility and adaptability make it a valuable tool in any
organization's toolkit.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`_, a Python-based implementation of *Plugin Oriented
Programming (POP)*. POP seeks to bring together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`_
* `pop-awesome <https://gitlab.com/vmware/pop/pop-awesome>`_
* `pop-create <https://gitlab.com/vmware/pop/pop-create/>`_

###############
Getting Started
###############

Prerequisites
-------------

* Python 3.8+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``web-retriever``, you can do so by either installing from
PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

   pip install web-retriever

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com/hoprco/web-retriever.git
   cd web-retriever

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install .

#####
Usage
#####

.. code-block:: text

   $ web-retriever -h

   usage: web-retriever [-h] [--config CONFIG] [--config-template] [--log-datefmt LOG_DATEFMT] [--log-file LOG_FILE] [--log-fmt-console LOG_FMT_CONSOLE]
                        [--log-fmt-logfile LOG_FMT_LOGFILE] [--log-handler-options [LOG_HANDLER_OPTIONS ...]] [--log-level LOG_LEVEL]
                        [--log-plugin {basic,datagram,null,rotating,socket,timed_rotating}] [--version] [--versions-report]

   options:
     -h, --help            show this help message and exit
     --config CONFIG, -c CONFIG
                           Load extra options from a configuration file onto hub.OPT.web_retriever
     --config-template     Output a config template for this command
     --version             Display version information
     --versions-report     Output a version report for reporting bugs

   Logging Options:
     --log-datefmt LOG_DATEFMT
                           The date format to display in the logs
     --log-file LOG_FILE   The location of the log file
     --log-fmt-console LOG_FMT_CONSOLE
                           The log formatting used in the console
     --log-fmt-logfile LOG_FMT_LOGFILE
                           The format to be given to log file messages
     --log-handler-options [LOG_HANDLER_OPTIONS ...]
                           kwargs that should be passed to the logging handler used by the log_plugin
     --log-level LOG_LEVEL
                           Set the log level, either quiet, info, warning, debug or error
     --log-plugin {basic,datagram,null,rotating,socket,timed_rotating}
                           The logging plugin to use

Examples
--------

Web Retriever, like all POP applications, can accept configuration files in YAML format. Configuration
parameters can be passed to POP plugins inside the application via this configuration file. Rulesets
are established in the configuration file and used by Web Retriever to enforce any defined rules. The
following configuration file sets the application logging to ``DEBUG`` level and puts a simple rule in
place to enforce access to the API only by clients residing on localhost.

.. code-block:: yaml

   pop_config:
     log_level: DEBUG

   web_retriever:
     rules:
       - rule_type: "deny"
         rule_string: "remote != '127.0.0.1' or remote != '::1'"

The configuration file path is then passed to the application on the command line:

.. code-block:: text

   $ web-retriever -c config.yaml

   ======== Running on http://0.0.0.0:8080 ========
   (Press CTRL+C to quit)

#######
Roadmap
#######

Reference the `open issues <https://gitlab.com/hoprco/web-retriever>`_ for a list of
proposed features (and known issues).

################
Acknowledgements
################

* `Img Shields <https://shields.io>`_ for making repository badges easy.
