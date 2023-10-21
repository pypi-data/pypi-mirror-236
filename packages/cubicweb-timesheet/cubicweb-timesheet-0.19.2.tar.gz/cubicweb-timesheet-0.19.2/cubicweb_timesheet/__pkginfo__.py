# pylint: disable-msg=W0622
"""cubicweb-timesheet application packaging information"""

modname = 'timesheet'
distname = 'cubicweb-%s' % modname

numversion = (0, 19, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = 'record who did what and when for the CubicWeb framework'
web = 'http://www.cubicweb.org/project/%s' % distname
author = 'Logilab'
author_email = 'contact@logilab.fr'
classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
           ]

__depends__ = {'cubicweb': '>= 3.38.0, < 3.39.0',
               'cubicweb-calendar':  '>= 0.7.0',
               'cubicweb-workorder': '>= 0.9.0',
               'cubicweb-rqlcontroller': None,
               }
