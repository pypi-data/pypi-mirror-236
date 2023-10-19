DBasTable
---------

Handle SQLite database tables just as if they were `Numpy structured arrays <https://numpy.org/doc/stable/user/basics.rec.html>`_, `~astropy.table.Table` or `~pandas.DataFrame`. This package is intended to be a simple interface to SQLite databases, so you can interact with them without know SQL commands.

.. code-block:: python

    >>> from dbastable import SQLDatabase
    >>> db = SQLDatabase('test.db', autocommit=True)
    >>> db.add_table('table1')
    >>> db['table1']['col1'] = [1, 2, 3, 4]
    >>> db['table1']['col2'] = ['a', 'b', 'c', 'd']
    >>> print(db['table1'][2].values)
    (3, 'c')

Its design is based mainly in the way you interact with `Numpy structured arrays <https://numpy.org/doc/stable/user/basics.rec.html>`_, while keep the possibility of non-volatile and in-disk data storage.

What is it for?
===============

The design of this package was made for *very simple interactions* with Python's sqlite implementation, so you can interact with sqlite databases without know SQL commands. So, if you need to work with simple tables, composed by columns of data in standard python formats and don't want to perform SQL queries manually, may be this package is for you.

What is it *NOT* for?
=====================

As menioned above, we intended to perform only simple operations with this package. So, *we intentionally limited the functionality*. Do not expect perform complex queries here. This package is for simplicity. There are several alternatives that are more feature-complete.

Do not use in large production
==============================

I'm not a SQL master, nor a digital security guru. I'm an astrophysicist that do some python. So, if you want to use it, use with care.

Installation
------------

The easiest way to install dbastable is via `pip <https://pip.pypa.io/en/stable/>`_::

    pip install dbastable

Alternatively, you can clone the repository and install it manually::

    git clone
    cd dbastable
    pip install -U .

or::

    pip install -U git+https://github.com/juliotux/dbastable

Development version is also available at pip::

    pip install -U --pre dbastable

Documentation
-------------

The documentation is available at https://dbastable.readthedocs.io/en/latest/

Usage
-----

For a general usage guide, see the following sections:

.. toctree::
   :maxdepth: 1

   general_usage
   viewer_classes
   where_statements
   nonconformant

License
-------

`dbastable` is licensed under the terms of the `MIT license <https://opensource.org/license/mit/>`_. See the file "LICENSE" for information on the history of this software, terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

API Reference
-------------

.. toctree::
   :maxdepth: 1

   api
