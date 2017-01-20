Synopsis

The AnimalBreedingDB project aims at supporting animal breeding activities. The first step allows analyzing pedigree information to estimate relatedness between animals.
The relatedness information is used to predict best crosses to manage genetic diversity.
The next step will be handling database for storing animal information, cross informations, relatedness information.

Right now, only first phase is functional.

The application uses Qt graphical interface for user experience.



Motivation

This project has been initiated to support familial hare breeding activity. It is personal project I use to train on Python programming.



Installation

To launch the application:
>python LievreDB.py

Uses "Lievre_Odile_16.csv" as input example

Code can be freeze for Windows using pyinstaller code:
pyinstaller --noconfirm ^
    --onedir --noconsole ^
    --icon=iconexe.ico ^
    LievreDB.spec



Tests

>python LievreDB.py
Uses "Lievre_Odile_16.csv" as input example



Contributors

Please contact ranc.nicolas@gmail.com for any comment/need.



License

GNU General Public License V3 (LICENCE file)
