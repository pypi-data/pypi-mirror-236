# Gitlab source control repository

This project is hosted on gitlab.com and the gitlab provided features are used in the development process. People who already have a github account can also use that account to log in to gitlab. The git repository is public and can be cloned with `git` so all regular git development can be used for PDKMaster development.

[Gitlab Issues](https://docs.gitlab.com/ee/user/project/issues/) are used in this project for bug tracking and feature requests. If you have problems using PDKMaster or think about possible improvements or extensions to the project anyone is free to create a new issue. No project specific policies are in place (yet) on how bugs or feature requests need to be reported.

Code contributions need to de done through the [gitlab merge request feature](https://docs.gitlab.com/ee/user/project/merge_requests/). Anyone can create a merge request. Creation of the merge request will also run the [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/) on the request. Requests can only be accepted when this [CI pipeline](https://docs.gitlab.com/ee/ci/pipelines/) is passing.
New requests will also be reviewed by a project maintainer. They will optionally propose some improvements to the code. After the proposed improvements are implemented a project maintainer can then merge the request into the main branch.
If a merge request is considered out of scope or not in line with existing code base, a merge request may be closed without merging. For bigger code changes it does then make sense to first discuss the proposed changes in a feature request issue before actually starting the development work.  
Currently merge requests can only be handled by the project maintainers on a best effort basis.

# Code style

For code style [PEP 8](https://pep8.org/) is mainly followed but not strictly. Line lengths above 80 are accepted; it is more around 100.

There is a strong preference for multi-line brace statements to put the opening brace as last character on a line followed by the lines indented one level and then the closing brace on a separate line unindented.

So:

```python
val = [
    "one", "two", "four",
    "sixteen",
]
```

not:

```python
val = ["one", "two", "four",
       "sixteen"]
```

or:

```python
val = [
    "one", "two", "four",
    "sixteen",
    ]
```

For method definitions `self` and optionally `*` may be left after the opening `(`; e.g.:

```python
class C:
    ...

    def method(self, *,
        param1: int, param2: int,
        param3: str,
    )
```

Typically formatting only merge requests are not accepted and the formatting of the code as first committed will be retained. Project maintainers may add a code reformatting commit before merging a merge request.

For method and functions definitions normally argument passing by name is enforced by using the '*' construct. One accepted exception is when the function/method name is a verb and the parameter is the direct object of the verb; e.g.:

```python
class _Layout:
    ...

    def place(self, object: "_Layout"):
        ...
```

[Type annotations](https://docs.python.org/3/library/typing.html) are used to define the types of function & method parameters and object attributes. No run-time code is added to check types of annotated parameters and attributes; people need to rely on type checkers for conformance. Additional run-time type checks may be added if they can't be easily added using type annotations.

As is discussed in [PEP 8]() non-public attributes start with a `_`. So in general no classes, functions, methods, attributes starting with a `_` should be used in user code.
Some corner cases are not fully worked out yet and are further discussed in [#73](https://gitlab.com/Chips4Makers/PDKMaster/-/issues/73)

# Minimal supported python version

Currently, minimal supported python version is v3.6. This means that the CI pipeline runs with that version and that all commits requested to be merged have to be compatible with it. Investigation is ongoing to switch to [v3.8 as minimal version](https://gitlab.com/Chips4Makers/PDKMaster/-/issues/45).

# License

Contributors are allowing their code to be multi-licensed as specified in
[LICENSE.md](LICENSE.md). This also means they have to fullfil the patent clauses included
in any of the listed licenses. The rationale behind the multi-licensing is given in
[README.md](README.md)

All source files in this repository need to contain a proper `SPDX-License-Identifier` annotation; no other SPDX headers are added to the files.  
For example for python files this is:

```python
# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
```

# Sign your work - the Developer’s Certificate of Origin

In order for patches to be accepted in the repository of this project committers will need to certify the code by signing off their code. The commonly used 
[Developer's Certificate of Origin](https://developercertificate.org/) is used for this purpose.

The sign-off is a simple line at the end of the commit message for the patch, which certifies that you wrote it or otherwise have the right to pass it on as an open-source patch. The rules are pretty simple: if you can certify the below:

__Developer’s Certificate of Origin 1.1__

> By making a contribution to this project, I certify that:
>
> (a) The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or
>
> (b) The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or
>
> (c) The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.
>
> (d) I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

then you just add a line saying:

    Signed-off-by: Random J Developer <random@developer.example.org>

using your name with which you are readily known in the community; anonymous signing of the code will not be accepted.
