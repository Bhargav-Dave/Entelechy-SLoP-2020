# FAQs

## What are we aiming for in this project?
There are three main things that we want to achieve through this project.
1. Retrieving the old data from the old website and storing it in a structured filesystem.
2. Minimizing the processing in the backend and making the load times as short as possible, doing that through a rest API.
3. Making the website accessible by adding service workers and essentially building the front-end in the form of an installable PWA in standalone mode, and possibly adding other PWA features.

## Why are we using a structured filesystem instead of a database?
- Ease of migration
- Simplicity in adding new features
- Even if the website isn't maintained regularly in the future, the servers shouldn't become slower as the data scales up

## What should you have in your setup?
Access to bash, as the server we are going to use in the end is going to be running linux and we may end up utilizing the command line utilities. If you're on Windows, check out [Windows Subsytem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Just installing version 1 would be sufficient for this project. Checkout the other technologies mentioned in the [README](./README.md).

## Whom should I contact in case of other doubts?
Contact Mit or Bhargav or just drop a text on the WhatsApp group or the Gitter channel.