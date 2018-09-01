# Scripts to work with the POSIX specification

This repository includes scripts to parse a POSIX specification given in HTML format and gather statistics of a C/C++ GIT repository regarding occurrences of these functions.

## Parsing the POSIX specification

**A finished `posix_functions` file ships with this repository, so you have to follow this steps only if you want to parse a newer standard!**

Please execute `./setup.sh`, which will download the POSIX specification in HTML format. **Please note, that the standard is shipped under its own license and our `LICENSE` file does not apply.**

The script `parse_posix_standard.py` will parse all specification files from the previous step and output a table listing all POSIX functions, their corresponding includes and a regular expression to find occurrences of this function in source code. You may want to call it like that:
```
./parse_posix_standard.py | tee posix_functions
```

## Scripts

The folder `repository_lists` contains a list of repositories from Github which are either on the first two pages sorted by *most forks* or *most stars* and contain C or C++ code, at least at the time the lists were created.

You can either use these files or create a new TXT file containing the URL to your own GIT repository.

The script `checkout_all_repositories.sh` will clone all GIT repositories listed in files given as parameters. You can call it for example like (**this will download ~20 GB of data**):
```
./checkout_all_repositories.sh repository_lists/*
```
**Obviously these repositories also ship with their own independent license.**

Alternatively, only pass your newly created TXT file to checkout only your repository.

The script `compute_all_repositories.sh` will compute statistics about the used POSIX functions for all repositories, for the current HEAD, for the first commit, which is older than 5 years, and for the first commit, which is older than 10 years (if they exist). Just call it like (**takes a lot of time**):
```
./compute_all_repositories.sh
```

The script `generate_statistics_per_function.py` will add the corresponding include to the previously generated statistics of a repository. Call it like:
```
cd statistics && ../generate_statistics_per_function.py --verbose --posix_function_list ../posix_functions <repository>.posix
```
The script `generate_statistics_per_file.py` will generate an aggregated statistic by include header, so all POSIX function which are included by one header are summed up. Call it like:
```
cd statistics && ../generate_statistics_per_file.py --verbose --posix_function_list ../posix_functions <repository>.posix
```

The script `generate_statistics_for_all_per_file.sh` will aggregate statistics for all repositories. Call it like:
```
./generate_statistics_for_all_per_file.sh
```
