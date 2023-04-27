'''
CS 5920 Project
Homomorphic Encryption: What Is It and How Can It Help Secure Healthcare Systems
Spring 2023 - Date: 04/26/2023
Student: Carlos E. Torres
'''
import json
import random
from Crypto.Util.number import *
from Crypto import Random
import Crypto
import libnum
import requests

BITS = 512
HEALTH_API_URL = 'http://127.0.0.1:5051/calculate'
OUTPUT_LOG = ''

def get_generator(p: int):
    while True:
        # Find generator which doesn't share factor with p
        generator = random.randrange(3, p)
        if pow(generator, 2, p) == 1:
            continue
        if pow(generator, p, p) == 1:
            continue
        return generator


def print_log(text, value=''):
    global OUTPUT_LOG
    print(text, value)
    OUTPUT_LOG += f'{text} {value}\n'


def encrypt_send(weight, height):
    global OUTPUT_LOG
    OUTPUT_LOG = ''

    # Generate public and private key
    p = Crypto.Util.number.getPrime(BITS, randfunc=Crypto.Random.get_random_bytes)
    x = random.randrange(3, p) # private key
    g = get_generator(p)
    Y = pow(g, x, p)

    print_log(f'Security parameter = {BITS} bits')

    print_log(f"weight = {weight}\nheight = {height}\n")
    print_log(f"Public key\np = {p}\ng = {g}\nY = {Y}\n\nPrivate key\nx = {x}")

    # Encrypt weight and height
    k1 = random.randrange(3, p)
    a1 = pow(g, k1, p)
    b1 = (pow(Y, k1, p)*weight) % p

    k2 = random.randrange(3, p)
    a2 = pow(g, k2, p)
    b2 = (pow(Y, k2, p)*height) % p

    print_log(f"\nEncrypted (weight)\na = {a1}\nb = {b1}")
    print_log(f"\nEncrypted (height)\na = {a2}\nb = {b2}")

    # Request to Healthcare System API
    print_log('\n--------------------------------------------------------------------')
    print_log('\n-> Sending ciphertexts to Healthcare System API on ' + HEALTH_API_URL)
    payload = {
        'public_key': {
            'p': p,
            'g': g,
            'Y': Y
        },
        'weight': {
            'a1': a1, 
            'b1': b1
        },
        'height': {
            'a2': a2, 
            'b2': b2
        }
    }
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(HEALTH_API_URL, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            raise Exception(f'Could not request the server. Error: {response.status_code}')
        response_json = response.json()
    except Exception as err:
        print_log('>> Error on requesting the Healthcare System API:', err)
        return {
            'bmi': 0,
            'console': OUTPUT_LOG
        }
    r1 = response_json['r1']
    r2 = response_json['r2']
    r3 = response_json['r3']
    r4 = response_json['r4']

    print_log('\n-> Sent public key, weight, and height ciphertexts to Healthcare System API to be computed')
    print_log('\n-> Healthcare System API performed computation on ciphertexts and return results')
    print_log('\n--------------------------------------------------------------------')

    print_log('\nReceived computed ciphertexts from the Healthcare System API')
    print_log('result1')
    print_log('r1 =', r1)
    print_log('r2 =', r2)
    print_log('result2')
    print_log('r3 =', r3)
    print_log('r4 =', r4)

    # Decrypt ciphertext result
    result1 = ( r2 * libnum.invmod(pow(r1, x, p), p) ) % p
    result2 = ( r4 * libnum.invmod(pow(r3, x, p), p) ) % p
    result =  result1/result2

    print_log('\nDecrypted ciphertext to get plaintext results')
    print_log('result1 =', result1)
    print_log('result2 =', result2)

    print_log("\nFinal result (result1/result2):", result)

    return {
      'bmi': result,
      'console': OUTPUT_LOG
    }
