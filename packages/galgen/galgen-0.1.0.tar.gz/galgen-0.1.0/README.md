# GalGen

Simple gallery generator.

## Features

- Simple
- Reliable
- Customizable

## Demo

Sample gallery can be found [here](https://filedn.com/ls8U70bX0lASS65WlPE8h3j).

## Installing

```sh
pip install galgen
```

## Getting Started

Let's say we have the following file structure:

```
holidays/
  day1/
    pic1.jpg
    pic2.jpg
    pic3.jpg
    thumnails/
      pic1.jpg
      pic2.jpg
      pic3.jpg
  day2/
    pic1.jpg
    pic2.jpg
    pic3.jpg
    thumnails/
      pic1.jpg
      pic2.jpg
      pic3.jpg

```

To generate and open your gallery invoke the following:
```sh
$ galgen init path/to/holidays
$ galgen build --open path/to/holidays
```

- One or more directories with the pictures are required.
- Define content of your gallery in gengal-config.yml
- Customize layout in index.html.j2

Rebuild your gallery whenever pictures are added/removed or other changes applied.
```sh
$ galgen build --force path/to/holidays
```

# Thumnails

- Thumnails are optional. Skip them (for simplicity) or generate manually (for performance).
- Size of the thumnails is of your choice.
- Filenames of the thumnails must correspond to the filenames of the full-scale pictures.
