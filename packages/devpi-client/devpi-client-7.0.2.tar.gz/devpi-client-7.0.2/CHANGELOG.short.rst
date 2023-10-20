

=========
Changelog
=========




.. towncrier release notes start

7.0.2 (2023-10-19)
==================

Bug Fixes
---------

- Fix #992: Fix error added in 6.0.4 when old authentication data from before 6.x exists.


7.0.1 (2023-10-15)
==================

Bug Fixes
---------

- Fix #1005: use ``shutil.move`` instead of ``Path.rename`` to move distribution after building to prevent cross-device link errors.

- Fix #1008: pass ``--no-isolation`` option to ``build`` when determining name/version for documentation.


7.0.0 (2023-10-11)
==================

Deprecations and Removals
-------------------------

- Use ``build`` instead of deprecated ``pep517`` package.

- Removed dependency on py package.
  Plugins which expect py.path.local need to be adjusted to work with pathlib.Path.

- Dropped support for Python <= 3.6.



Other Changes
-------------

- .. note::
      Potentially breaking fix #939: devpi-common 4.x now has custom legacy version parsing (non PEP 440) after packaging >= 22.0 removed support. This might affect commands like ``devpi remove`` if used with version ranges. Legacy versions were always and still are sorted before PEP 440 compliant versions, but the ordering between legacy versions might be affected.

- Fix #946: output ``name==version`` instead of ``name-version`` for ``devpi list -v``.


6.0.6 (2023-10-11)
==================

Bug Fixes
---------

- Fix #997: Directly use ``BDist``, ``SDist`` and ``Wheel`` from ``pkginfo`` based on file extension instead of ``get_metadata``, as the latter does auto-detection on content which fails in some cases.

- Fix #1002: cleanup ``build`` directory before running Sphinx to prevent build artifacts from being added to documentation zip.


6.0.5 (2023-07-02)
==================

Bug Fixes
---------

- Remember URL when ``devpi use`` causes a 403, so one can use ``devpi login`` afterwards.

- Fix #978: Quote username and password when adding to URL.

- Fix #980: Remove long deprecated backward compatibility for old pluggy versions to fix error with pluggy 1.1.0.

