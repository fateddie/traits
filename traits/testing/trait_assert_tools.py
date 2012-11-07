#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in /LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------
""" Trait assert mixin class to simplify test implementation for Trait
Classes.

"""
import contextlib


class _AssertTraitChangesContext(object):
    """ A context manager used to implement the trait change assert methods.

    """

    def __init__(self, obj, xname, count, test_case):
        self.obj = obj
        self.xname = xname
        self.count = count
        self.event = None
        self.events = []
        self.failureException = test_case.failureException

    def _listener(self, obj, name, old, new):
        """ Dummy trait listener
        """
        self.event = (obj, name, old, new)
        self.events.append(self.event)

    def __enter__(self):
        """ Bind the trait listener
        """
        self.obj.on_trait_change(self._listener, self.xname)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """ Remove the trait listener
        """
        if exc_type is not None:
            return False

        self.obj.on_trait_change(self._listener, self.xname, remove=True)
        if self.event is None:
            msg = 'A change event was not fired for: {0}'.format(self.xname)
            raise self.failureException(msg)
        elif self.count is not None and len(self.events) != self.count:
            msg = 'Change event for {0} was fired {1} times instead of {2}'
            items = self.xname, len(self.events), self.count
            raise self.failureException(msg.format(*items))

        return False


@contextlib.contextmanager
def reverse_assertion(context, msg):
    context.__enter__()
    try:
        yield context
    finally:
        try:
            context.__exit__(None, None, None)
        except AssertionError:
            pass
        else:
            raise context.failureException(msg)


class TraitAssertTools(object):
    """ Mixin class to augment the unittest.TestCase class with useful trait
    related traits methods.

    See Also
    --------
    TraitAssertToolsTestCase

    """

    def assertTraitChanges(self, obj, trait, count=None):
        """ Assert that the class trait changes exactly n times.

        Used in a with statement to assert that a class trait has changed
        during the execution of the code inside the with context block
        (similar to the assertRaises method).

        Please note that the context manager returns itself and the user can
        introspect the information of:
        - The last event fired by accessing the ``event`` attribute of the
          returned object.
        - All the fired events by accessing the ``events`` attribute of the
          return object.

        Example
        -------
        class MyClass(HasTraits):
            number = Float(2.0)

        my_class = MyClass()

        with self.assertTraitChanges(my_class, 'number', count=1):
            my_class.number = 3.0

        Parameters
        ----------
        obj : HasTraits
            The HasTraits class instance who's class trait will change.

        xname : str
            The extended trait name of trait changes to listen too.

        count : int
            The expected number of times the event should be fired. When None
            (default value) there is no check for the number of times the
            change event was fired.

        ----
        - Checking if the provided xname corresponds to valid traits in
          the class is not implemented yet.

        """
        return _AssertTraitChangesContext(obj, trait, count, self)


    def assertTraitDoesNotChange(self, obj, xname):
        """ Assert that no trait event is fired.

        Used in a with statement to assert that a class trait has not changed
        during the execution of the code inside the with statement block.

        -------
        class MyClass(HasTraits):
            number = Float(2.0)
            name = String

        my_class = MyClass()

        with self.assertTraitDoesNotChange(my_class, 'name'):
             my_class.number = 3.0

        Parameters
        ----------
        obj : HasTraits
            The HasTraits class instance who's class trait will change.

        xname : str
            The extended trait name of trait changes to listen too.

        ----
        - Checking if the provided xname corresponds to valid traits in
          the class is not implemented yet.

        """
        msg = 'A change event was fired for: {0}'.format(xname)
        context = _AssertTraitChangesContext(obj, xname, None, self)
        return reverse_assertion(context, msg)