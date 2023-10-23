#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
# Check if commit message if signed off by author or committer.
# Currently only checks the last commit log
from typing import Dict, Optional
from subprocess import run, PIPE

r = run(("git", "log", "-n", "1", "--pretty=fuller"), stdout=PIPE)
ids: Dict[str, Optional[str]] = {
    "Author:": None,
    "Commit:": None,
    "Signed-off-by:": None,
}
for line in r.stdout.decode().split("\n"):
    for key in ids.keys():
        if key in line:
            idx = line.index(key)
            ids[key] = line[(idx + len(key)):].strip()
author = ids["Author:"]
committer = ids["Commit:"]
signer = ids["Signed-off-by:"]

assert author is not None
assert committer is not None
signer = ids["Signed-off-by:"]
if signer is None:
    raise ValueError("'Signed-off-by:' line not found in commit message")
if signer not in (author, committer):
    raise ValueError(
        f"Signer '{signer}' differs from author '{author}' and committer '{committer}'",
    )
