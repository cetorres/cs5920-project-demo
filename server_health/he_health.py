'''
CS 5920 Project
Homomorphic Encryption: What Is It and How Can It Help Secure Healthcare Systems
Spring 2023 - Date: 04/26/2023
Student: Carlos E. Torres
'''
import random

BMI_CONST = 703

def receive_calculate(data):
    # Public key
    p = int(data['public_key']['p'])
    g = int(data['public_key']['g'])
    Y = int(data['public_key']['Y'])

    # Ciphertext weight and height
    a1 = int(data['weight']['a1'])
    b1 = int(data['weight']['b1'])
    a2 = int(data['height']['a2'])
    b2 = int(data['height']['b2'])

    # Encrypt BMI_CONST with public key to be able to multiply
    k3 = random.randrange(3, p)
    a3 = pow(g, k3, p)
    b3 = (pow(Y, k3, p)*BMI_CONST) % p

    # Multiplication
    # a = (a1*a2) % p
    # b = (b1*b2) % p

    # Division
    # a = (a1 * libnum.invmod(a2,p)) % p
    # b = (b1 * libnum.invmod(b2,p)) % p

    # BMI = BMI_CONST * weight/height**2 = (BMI_CONST * weight) / (height * height)
    # BMI_CONST * weight
    r1 = (a1*a3) % p
    r2 = (b1*b3) % p
    # height * height
    r3 = (a2*a2) % p
    r4 = (b2*b2) % p

    return {
      'r1': r1,
      'r2': r2,
      'r3': r3,
      'r4': r4
    }