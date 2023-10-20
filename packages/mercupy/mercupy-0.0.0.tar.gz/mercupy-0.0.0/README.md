# Mercupy

Python interface definition for Mercury.

Maps Mercury objects (manifests, filters, etc.) to Python native objects.

- Manifest elements maps to `manifest_elements.ManifestElement`.
- Filter elements maps to `filter_elements.FilterElement`.
- Condensed tags map to `tags.TagTokenTree`.
However, `tags.CondensedTag` and overriden operators (`*, /, +`)
should be used to construct condensed tags;
`tags._TagTokenTree` should not be used directly.
- Data passed to and received from deep learning models are mapped to `data_elements.DataElement`.

## Links

[Mercury Project Homepage](https://trent-fellbootman.github.io/mercury.io)

[Mercury GitHub Repository](https://github.com/Trent-Fellbootman/mercury)

[Mercury Documentation](https://mercurynn.readthedocs.io/en/latest/)
