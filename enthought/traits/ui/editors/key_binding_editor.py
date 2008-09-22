#------------------------------------------------------------------------------
#
#  Copyright (c) 2008, Enthought, Inc.
#  All rights reserved.
#  
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#  
#  Author: David C. Morrill
#  Date:   10/21/2004
#
#------------------------------------------------------------------------------
""" Defines the key binding editor for use with the KeyBinding class. This is a 
specialized editor used to associate a particular key with a control (i.e., the
key binding editor).
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

# FIXME: Import from the api.py file when it has been added.
from enthought.traits.ui.basic_editor_factory \
    import BasicEditorFactory
                                      
from enthought.traits.ui.toolkit \
    import toolkit_object

# Callable which returns the editor to use in the ui.
def key_binding_editor():
    return toolkit_object('key_binding_editor:KeyBindingEditor')       
    
#-------------------------------------------------------------------------------
#  Create the editor factory object:
#-------------------------------------------------------------------------------         
KeyBindingEditor = BasicEditorFactory(klass = key_binding_editor)

### EOF ------------------------------------------------------------------------