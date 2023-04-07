# Library-CLI-App

## About

This is Library Command-line application.
Developed as part of Data Science in Fenyx academy. 

In the code we use '''psycopg2, typer, typing, rich''' modules.

## Getting started

The application works from the command line. 
In addition to the obvious library methods that allow you to borrow and return books, you can also view rankings of the most-read authors, books and genres. 


The methods are divided into two groups: those available without registration and those available only to registered users.
You can see all available methods using
'''
python main.py --help
'''
![screenshot main menu](/img/mainmenu.png)

In addition to discrete operation using commands, we have added threading. So there are two kinds of main menus: for unregistered users (only part of the functions) and for registered users (full set of functions)

![add_book method](/img/addbook.png)

The project uses Postgresql to handle the database. The ERD is presented below.
![ERD in the repository](/img/ERD.png)
## Team

Authors of project with github-links

1. [Danil Melnikov](https://github.com/meldanil)
2. [Ammar Esam](https://github.com/AmmarEsam)
3. [Osman Bahadir Yilmaz](https://github.com/OsmanBahadirYlmz)
4. [Kemal](https://github.com/Kemal919191)
5. [Abdullah Ali](https://github.com/AbdullahBetl)

Our heartfelt thanks to our mentor [Ceren Ugurlu](https://www.linkedin.com/in/ceren-ugurlu-b22883190/?originalSubdomain=nl)
and all members of [FENYX Academy](https://www.fenyx.academy/)



