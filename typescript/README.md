# Demo Typescript Script for CATCH API

## Intro

This is a demo script written in typescript to retrieve data for target objects from the CATCH API.

## Quickstart (on Mac/Linux)

You need to have node installed. If you are new to node and typescript then see below.

```bash
npm install
./_run_main_script
```

## Node, NPM, NVM and Typescript

### Overview

The dominant language of all modern browsers is javascript (JS). If you want to use JS on the command line, then you need to install a command-line interpreter for JS called node (aka nodejs). Using node is similar to using python. For example, to execute a node script, you'd simply run the node executable with the script as first argument from the command line: `node main.js`.

Node benefits from a massive eco-system of community-developed packages (aka libraries). To use a package from the community, you need to have a separate executable -- the 'node package manager' (npm) -- installed.

### Installation

#### Simple (but not recommended)

To install both node and npm together, you can download an installer from [nodejs.org](https://nodejs.org/en/download/), or use your system package manager (`brew install node` on a Mac, `apt install nodejs` on Debian, etc.)

#### Recommended

Node/npm are being constantly improved, and certain programs written in node may require specific versions of node. For that reason, I recommend that you ONLY install node by means of a third executable -- the 'node version manager' (nvm). You can install `nvm` following instructions [here](https://github.com/nvm-sh/nvm).

Once `nvm` is installed, you can run e.g. `nvm install 10` to install the latest version of node 10 (as of this moment that's version `10.19.0`). You can then switch between major versions of node using e.g. `nvm use 10`, `nvm use 12`, etc.

### Typescript

Typescript is a language that transpiles to JS. It allows you to assign types to variables and, when combined with a modern code editor (I highly recommend Visual Studio Code), it provides fantastic intellisense. In short, it is much easier and more enjoyable to program in typescript (though, of course, it takes slightly more setup to transpile first to JS).

To run a typescript script, you can either first transpile using the `tsc` executable and then run the output JS using node. Or, you can use the executable `ts-node`, though in practice you will often require a fair configuration flags which are normally handled with a specialized `tsconfig.json` file.
