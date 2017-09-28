Security CTF Challenges
=======================

In this repository you can find challenges from previous _capture-the-flag_ security competitions organized by the [Probe.ly](https://probely.com) team. For now we're only adding challenges that were both opened and successfully solved by some team during a public event.

Feel free to use these in your own competitions either _as-is_ or as starting points for your own custom challenges, perhaps together with our [competition dashboard](https://github.com/Probely/CTF-Game).

Challenges are organized by category. Each challenge has a level of difficulty, indicated in each challenge folder name, and range from 100 to 400, where 100 is the easiest and 400 the hardest.

Each challenge has its own `README.md` file with the challenge context and installation instructions. The solution is in a separate `SOLUTION.md` file to avoid spoilers.

There is also a `Vagrantfile` available in the repository's root. To have an environment similar to the one where we test the challenges, install [Vagrant](https://www.vagrantup.com/) with [VirtualBox](https://www.virtualbox.org/) and run `vagrant up`. This sets up a base environment, so make sure to check each challenges' `README.md` for challenge-specific dependencies.

Disclaimer
==========

This **isn't** production code. All of these challenges have **vulnerabilities** built into them **on purpose**. As they're one-off programs, they may also contain other random issues we didn't account for (if a team happens to discover one of these, it becomes part of the competition too).

Also, they're mostly using development-grade services and we recommend you run them behind a reverse proxy such as [nginx](https://nginx.org/). Check the `nginx` directory in the repository for configuration examples.

Contributing
============

We encourage you to fork this repository and add your own challenges. If you'd be kind enough to submit a pull request, we would surely appreciate it.

--
team@probely.com
