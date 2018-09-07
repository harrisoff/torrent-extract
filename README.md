# Torrent Resolver

Convert torrent file(s) to magnet link(s).

Get total file sizes by the way.

## Requirement

- [bencodepy](https://github.com/eweast/BencodePy)
- hashlib
- base64

## Usage

- For single torrent file:

 `resolveFile('file.torrent')`

- For multiple files in a directory:

 `iterateDir('torrent/files/directory')`

 > only matches torrent files

Alternatively, write functions to operate the results such as saving into database.