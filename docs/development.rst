.. _development:

Development
===========

The **UQAM Catalogue** is still under active development.

-----------
Source Code
-----------
The project source code is managed using git, and be be cloned using::
   $ git clone git://github.com/omad/uqam/


Tools
-----

Django, vim, postgresql, pip, virtualenv, 


.. _docs:

-------------
Documentation
-------------
The documentation is written in `reStructured Text`_ format.

Requires Sphinx_, which can be installed with::

   $ pip install sphinx

To view the documentation, build it to html by::

   $ cd docs
   $ make html

**Sphinx** will run and output the docs to ``docs/_build/html``.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org

