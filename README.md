# Java for GNOME-Builder

This plugin uses the Eclipse-JDT-Languageserver and requires [a patched GNOME-Builder](https://gitlab.gnome.org/JCWasmx86/gnome-builder/-/tree/lsp_fix_jdtls) to have working code-actions.

## Installation

```
./install.sh
```


## Known issues

- Sometimes reopening a session seems to fail (GNOME-Builder simply freezes)
- Sometimes the JDT-Server is shutdown while it is used, without too much investigation it seems to be a client-side problem.