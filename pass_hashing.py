# an example of creating an attacking script to attack all active directory users
import os 
import subprocess 

def get_active_directory_users() -> list:
    """Get a list of active directory users using 'net user /domain' command."""

    try:
        result = subprocess.run(['net', 'user', '/domain'], capture_output=True, text=True, check=True)
        output = result.stdout
        users = []
        capture = False
        for line in output.splitlines():
            if '---' in line:
                capture = not capture 
                continue
            if capture and line.strip():
                users.extend(line.split())
                return users
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving users: {e}")
        return []
    if __name__ == "__main__":
        users = get_active_directory_users()
        print("Active Directory Users:")
        for user in users:
            print(user)
            # This code is for attacking script educational purposes only. Unauthorized use is illegal and and unethical. written by SIPHE-LAN@

