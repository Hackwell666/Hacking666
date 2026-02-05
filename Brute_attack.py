# an example of a brute-force attack script for educational purposes only 

import itertools
import string 
import time 
# Function to stimulate password checking 

def check_password(attempt: str, actual_password: str) -> bool:
    return attempt == actual_password
# Main brute-force function 

def brute_force_password(actual_password: str, max_length: int =4):
    characters = string.ascii_letters + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_str = ''.join(attempt)
            print(f"Trying password: {attempt_str}")
            if check_password(attempt_str, actual_password=actual_password):
                print(f"password found: {attempt_str}")
                return attempt_str
            print("Password not found yet...")
            print("Password attempt took 0.1 seconds")
            time.sleep(0,1) # stimulate time delay for each attempt 

            if __name__ == "__main__":
                # Example actual password to crack 
                actual_password = "B@1!"
                brute_force_password(actual_password=actual_password, max_length=4)
                
                # This code is for educational purposes only. Unauthorized use of brute-force attacks is illegal and unethical. written by SIPHE-LAN
                