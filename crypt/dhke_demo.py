#dhke_demo.py

# Pick g / Small prime for purposes of demo
g = 3
N = 10007

# Each participant "Alice" and "Bob" pick a number between g and N
# Demonstrator will be Alice
a = random.randint(g,N)

# We do not show the a value to the crowd for starters, only assign it at random

# Now "Bob" participant picks their number at random between g and N

# Now each of us takes 'g' to the power of our private number, and then mod N
# Remember, 'mod' is the mathematically way of saying "Divide by x and return the remainder"
# Example, 25 / 5 = 5 even, no remainder, so 25 mod 5 = 0
# Likewise, 25 / 6 = 4 with 1 remainder left over, so 25 mod 6 = 1

A = (g ** a) % N
A

# "Bob" participant now calculates:
#  ( g ** b ) mod N
# Do this in Windows Calculator:
#  Click "Scientific"
#  Type "( g ^ b ) " then click the 'mod' button, and enter N value
# Share your result (B)

# Now take Alice's A and do the same calculation only using A instead of g:
#  ( A ^ b ) mod N
# DON'T SHARE YOUR NUMBER YET!

# Alice will find our shared number as well now
B = # Bob's B value
Key = ( B ** a ) % N

Key

