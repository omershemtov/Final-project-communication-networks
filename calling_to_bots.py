import subprocess
import threading
import time


def run_client_script():
    try:
        # Run the clientnotworking.py script using subprocess
        subprocess.run(['python', 'bot_client.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running client.py: {e}")

if __name__ == "__main__":
    bots_number = 3
    for i in range(bots_number):
        bot_thread = threading.Thread(target=run_client_script)
        bot_thread.start()
        time.sleep(0.2)