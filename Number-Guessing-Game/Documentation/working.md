\# Number Guessing Game - Working Principle



\## 1. Overview



The Number Guessing Game is a simple Python console application where the computer generates a random number between 1 and 100.



The player has to guess the number. The program provides hints after every guess until the correct number is found.



\## 2. Random Number Generation



The `random` module is used to generate the secret number.



```python

number = random.randint(1, 100)

This generates a random integer between 1 and 100.



3\. User Input



The player enters a guess using:



guess = int(input("Enter your guess: "))



The input is converted into an integer.



4\. Guess Comparison



The player's guess is compared with the randomly generated number.



Too Low



If:



guess < number



The program displays:



Too low! Try again.

Too High



If:



guess > number



The program displays:



Too high! Try again.

Correct Guess



If:



guess == number



The player wins and the program displays the number of attempts.



5\. Attempts Counter



The number of attempts is stored using a variable:



attempts = 0



After every valid guess:



attempts += 1



When the correct number is guessed, the total attempts are displayed.



6\. Error Handling



The program handles invalid input using try-except.



try:

&#x20;   guess = int(input("Enter your guess: "))

except ValueError:

&#x20;   print("Please enter a valid number.")



This prevents the program from crashing when the user enters text instead of a number.



7\. Program Flow

START

&#x20; |

&#x20; v

Generate Random Number

&#x20; |

&#x20; v

Ask User for Guess

&#x20; |

&#x20; v

Validate Input

&#x20; |

&#x20; +---- Invalid ----> Ask Again

&#x20; |

&#x20; v

Increase Attempts

&#x20; |

&#x20; v

Compare Guess

&#x20; |

&#x20; +---- Too Low ----> Try Again

&#x20; |

&#x20; +---- Too High ---> Try Again

&#x20; |

&#x20; +---- Correct ----> Display Attempts

&#x20;                        |

&#x20;                        v

&#x20;                       END

8\. Technologies Used

Python

Random module

Conditional statements

While loop

Exception handling

User input

9\. Future Improvements

Add difficulty levels

Add a scoring system

Add replay functionality

Add maximum attempts

Create a Tkinter GUI

Add high-score tracking

