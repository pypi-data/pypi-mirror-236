.. DeepDiff documentation master file, created by
   sphinx-quickstart on Mon Jul 20 06:06:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


DeepDiff 6.6.1 documentation!
=============================

*******
Modules
*******

The DeepDiff library includes the following modules:

- **DeepDiff** For Deep Difference of 2 objects. :doc:`/diff`

    It return the deep Difference of python objects. It can also be used to take the distance between objects. :doc:`/deep_distance`

- **DeepSearch** Search for objects within other objects. :doc:`/dsearch`

- **DeepHash** Hash any object based on their content even if they are not "hashable" in Python's eyes.  :doc:`/deephash`

- **Delta** Delta of objects that can be applied to other objects. Imagine git commits but for structured data.  :doc:`/delta`

- **Extract** For extracting a path from an object  :doc:`/extract`

- **Commandline** Most of the above functionality is also available via the commandline module  :doc:`/commandline`

***********
What Is New
***********

DeepDiff 6-6-1
--------------

    -  Fix for `DeepDiff raises decimal exception when using significant
       digits <https://github.com/seperman/deepdiff/issues/426>`__
    -  Introducing group_by_sort_key
    -  Adding group_by 2D. For example
       ``group_by=['last_name', 'zip_code']``

DeepDiff 6-6-0
--------------
    
    - :ref:`delta_to_flat_dicts_label` can be used to serialize delta objects into a flat list of dictionaries.
    - `NumPy 2.0 compatibility <https://github.com/seperman/deepdiff/pull/422>`__ by `William Jamieson <https://github.com/WilliamJamieson>`__

DeepDiff 6-5-0
--------------

    -  `parse_path <https://zepworks.com/deepdiff/current/faq.html#q-how-do-i-parse-deepdiff-result-paths>`__

DeepDiff 6-4-0
--------------

   -  `Add Ignore List Order Option to
      DeepHash <https://github.com/seperman/deepdiff/pull/403>`__ by
      `Bobby Morck <https://github.com/bmorck>`__
   -  `pyyaml to 6.0.1 to fix cython build
      problems <https://github.com/seperman/deepdiff/pull/406>`__ by
      `Robert Bo Davis <https://github.com/robert-bo-davis>`__
   -  `Precompiled regex simple
      diff <https://github.com/seperman/deepdiff/pull/413>`__ by
      `cohml <https://github.com/cohml>`__
   -  New flag: ``zip_ordered_iterables`` for forcing iterable items to
      be compared one by one.


*********
Tutorials
*********

Tutorials can be found on `Zepworks blog <https://zepworks.com/tags/deepdiff/>`_
                                                                                                                                                                                                          

************
Installation
************

Install from PyPi::

    pip install deepdiff

If you want to use DeepDiff from commandline::

    pip install "deepdiff[cli]"

If you want to improve the performance of DeepDiff with certain processes such as json serialization::

    pip install "deepdiff[optimize]"

Read about DeepDiff optimizations at :ref:`optimizations_label`

Importing
~~~~~~~~~

.. code:: python

    >>> from deepdiff import DeepDiff  # For Deep Difference of 2 objects
    >>> from deepdiff import grep, DeepSearch  # For finding if item exists in an object
    >>> from deepdiff import DeepHash  # For hashing objects based on their contents
    >>> from deepdiff import Delta  # For creating delta of objects that can be applied later to other objects.
    >>> from deepdiff import extract  # For extracting a path from an object


.. note:: if you want to use DeepDiff via commandline, make sure to run:: 
    pip install "deepdiff[cli]"

Then you can access the commands via:

- DeepDiff

.. code:: bash

    $ deep diff --help

- Delta

.. code:: bash

    $ deep patch --help

- grep

.. code:: bash

    $ deep grep --help
- extract

.. code:: bash

    $ deep extract --help


Supported data types
~~~~~~~~~~~~~~~~~~~~

int, string, unicode, dictionary, list, tuple, set, frozenset, OrderedDict, NamedTuple, Numpy, custom objects and more!


References
==========

.. toctree::
   :maxdepth: 4

   diff
   dsearch
   deephash
   delta
   extract
   commandline
   changelog
   authors
   faq
   support


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
