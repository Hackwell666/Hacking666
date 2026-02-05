#an example of BRUTE FORCE ATTACK IN PYTHON CODES
# Yes a brute force attack may take longer but it does help sometimes . 

#DICTIONARY ATTACKS
from string import ascii_letters
from string import digits
from string import ascii_letters, digits, punctuation
import winsound
# this a brute force to crack the for digit password in any devices 
# the brute force below is for 4 digits passcode if the passcode is more than for 4 numbers you have to extend your code the same way you did but adding another letter :............:
#alarming_attack = str(winsound )

for a in digits :
    for b in digits :
        for c in digits :
          for d in digits :
             print(a,b,c,d)

# we will use letters to perform the brute force attack other than numbers 3
#for i in ascii_letters:
  #for j in ascii_letters:
    #for k in ascii_letters:
      #for l in ascii_letters:
        #for m in ascii_letters:
          #print(i,j,k,l,m)

# now we are going to perform the brute force attack in 3 methods to carry on and make it easier
for i in ascii_letters + digits + punctuation:
  for j in ascii_letters + digits + punctuation:
    for k in ascii_letters + digits + punctuation:
      for l in ascii_letters + digits + punctuation:
       print(i,j,k,l )
 