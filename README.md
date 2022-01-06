Wordle solver run instruction:

python3.7 comb.py

The script outputs the first word to enter into wordle.
It then waits for the output. Please enter the output as 5 digits 
separated by commas, where 0 - gray (mistake), 1 - yellow (wrong placement),
2 - green (correct). 
For example, if the true word is 'siege' and you entered 'mania', 
wordle will show:
gray,yellow,gray,gray,gray

and you should write in the terminal:
0,1,0,0,0

The script will then output the next word to give to wordle and so on.

Good luck!

