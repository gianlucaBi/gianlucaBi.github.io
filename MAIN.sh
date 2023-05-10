#!/bin/bash 
jemdoc index 																			# This line compiles the main file
python2.7 PUBLICATIONS/format_bibtex.py 1 												# This line converts the bib file into a jemdoc file
jemdoc publications.jemdoc 															# This line compiles the publications jemdoc file
jemdoc researchTopics.jemdoc 														# This line compiles the research topics jemdoc file
jemdoc software.jemdoc 																# This line compiles the software jemdoc  file
jemdoc teaching.jemdoc 																# This line compiles the teaching jemdoc  file
jemdoc LINMA1510.jemdoc 																
jemdoc LINMA2875.jemdoc 																