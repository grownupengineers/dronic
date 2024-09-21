# Dronic

_in elvish_

This is a proof of context on a retake of _dronic_ using
[elvish](https://elv.sh) as the pipeline language.

There are three main features that make elvish an appealing candidate for the
pipeline language:

- **It's a shell language with complex types.**
   This mixes the best of both worlds -- an easy integration with external
   programs (shell) and the use of complex types (lists and maps) without
   external programs.
- **Passing code to functions (or _closures_).**
   In elvish, blocks of code are "first class citizens" (_citation needed_) and
   the ability to pass them around to functions as arguments should make it
   easier to control where and when the code is executed.
   _Disclaimer: this is heavily influenced by Jenkins usage_.
- **Extensible (_up to a point_).**
   Being implemented in Golang, with a documented API, it is possible to add new
   (native) builtins, functions and namespaces to tailer the pipeline to our
   needs.

And there are, of course, a couple of _cons_:

- **No sandboxing**
   Well, it's a shell ...
- **Unfamiliar syntax**
   Up to a certain point, it is just another shell, but pipeline
   developers/users may not yet be familiar with the full language, limiting
   adoption and initial productivity.

