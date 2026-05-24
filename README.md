# Template for C / C++ programs on profanOS

A little template for my C / C++ programs on [profanOS](<https://github.com/elydre/profanOS>) :D
  
## Cloning this repository 

Basically :
```
git clone https://github.com/tetram2674562/profan-CPP-Template.git 
cd profan-CPP-Template
git submodule update --init
```

## Compiling the program

```
mkdir build && cd build
cmake ..
make
```

And then you got your executable file in your build directory, ready to be ran on profanOS !

## About std library

Some of those library files has been provided to me by pf4, thanks to him !
However, they're still very unstable so careful ! (for example iostream header may not really work as intended)


## Libraries

This isn't very reliable (I'm bad at python) but It allows you to gather libs from libatron pf4 repository

For that just use the dependencies.py file.

#### List the libraries

To list the available libraries :

```
python3 dependencies.py list
```

#### Download the libraries
Just run :
```
python3 dependencies.py
```

#### Adding dependencies

Just add a new line to the `dependencies.txt` file with the name found on the list of libraries

## Licensing

This template is allowed to use for everyone.
But remember that profanOS is licensed under the GPLv3 license.
