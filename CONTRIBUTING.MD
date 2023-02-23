## Contributor guide

In this guide you will get an overview of the contribution workflow from creating a PR, reviewing, and merging the PR.

---

## Getting started

### Branches

The following are the branch naming conventions to be followed.

#### feature

convention: feature/
convention: feature/{directory}/

#### fix

convention: fix/
convention: fix/{directory}/

#### documentation

convention: documentation/
convention: documentation/{directory}

#### release

convention: release/v{X}.{Y}.{Z}<br/>

X - Major
Y - Minor
Z - Patch

#### PR process

This repo adopts the [rebase](https://www.atlassian.com/git/tutorials/merging-vs-rebasing#:~:text=The%20Rebase%20Option&text=But%2C%20instead%20of%20using%20a,commits%20required%20by%20git%20merge%20.) process for merge. 

1. Rebase from main
2. If you run into any merge issues, checkout this [git tutorial](https://github.com/skills/resolve-merge-conflicts) to help you resolve merge conflicts and other issues.
3. Create [Pull Request](#pull-requests) in order to merge to main

#### Pointers for Pull Requests and Merging

1. Please clearly define the changes made into your pull requests and highlight the thinking process.

2. Value readability over cleverness.
