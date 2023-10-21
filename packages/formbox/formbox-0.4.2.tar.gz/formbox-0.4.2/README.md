# formbox

This tiny script formats an [mbox] as HTML or XML.  It is intended
for rendering email replies on websites and their [RSS] feed.

## Prerequisites

This Python package depends on [nh3] for HTML sanitization
and [mistune] for rendering Markdown to HTML.  It is, however,
not designed to work with HTML emails with all those CSS and Java scripts.

## Installation

It is recommended to install this package from a downstream repository,
such as [nixpkgs].

## Usage

```console
$ formbox --help
usage: formbox [-h] mbox id template

format mbox as HTML/XML

positional arguments:
  mbox        path to mbox file
  id          root message ID
  template    path to template

optional arguments:
  -h, --help  show this help message and exit
```

## Copying

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[mbox]: https://en.wikipedia.org/wiki/Mbox
[RSS]: https://www.rssboard.org
[nh3]: https://nh3.readthedocs.io
[mistune]: https://mistune.lepture.com
[nixpkgs]: https://search.nixos.org/packages?query=formbox
