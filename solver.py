import requests
import os
import random
from base64 import b64encode
from base64 import b64decode
BLOCK_SIZE=16



padding_prefix = bytes([random.randrange(0,256) for i in range(BLOCK_SIZE - 1)])
HOST="localhost"
PORT=80
BASE_URL="http://"+HOST+":"+str(PORT)

B_SIZE = 128
BYTE_NB = B_SIZE // 8
cookie = b64decode(requests.get(BASE_URL+"/cookie").text.split(":")[1].strip())
print(cookie)
IV ='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def oracle_attack(encrypted):
    block_number = len(encrypted)//BYTE_NB
    decrypted = bytes()
    for i in range(block_number, 0, -1):
        current_encrypted_block = encrypted[(i-1)*BYTE_NB:(i)*BYTE_NB]

        # At the first encrypted block, use the initialization vector if it is known
        if(i == 1):
            previous_encrypted_block = bytearray(IV.encode("ascii"))
        else:
            previous_encrypted_block = encrypted[(i-2)*BYTE_NB:(i-1)*BYTE_NB]
        bruteforce_block = previous_encrypted_block
        current_decrypted_block = bytearray(IV.encode("ascii"))
        padding = 0
        for j in range(BYTE_NB, 0, -1):
            padding += 1
            for value in range(0,256):
                bruteforce_block = bytearray(bruteforce_block)
                bruteforce_block[j-1] = (bruteforce_block[j-1] + 1) % 256
                joined_encrypted_block = bytes(bruteforce_block) + current_encrypted_block
                oracle = requests.get(BASE_URL+"/feed", headers={"Cookie": b64encode(joined_encrypted_block).decode('utf-8')})
                print(oracle.text)
                if(oracle.status_code==200):
                    print("valid!")
                    current_decrypted_block[-padding] = bruteforce_block[-padding] ^ previous_encrypted_block[-padding] ^ padding
                    for k in range(1, padding+1):
                        bruteforce_block[-k] = padding+1 ^ current_decrypted_block[-k] ^ previous_encrypted_block[-k]
                    break
        decrypted = bytes(current_decrypted_block) + bytes(decrypted)
    return decrypted[:-decrypted[-1]]


print(oracle_attack(cookie))
