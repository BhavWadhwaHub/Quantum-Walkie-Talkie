# Quantum Walkie Talkie

A Python-based simulation of a **quantum-secure communication system** inspired by the **BB84 Quantum Key Distribution (QKD)** protocol using the Qiskit framework.

This project demonstrates how two users can securely establish a shared secret encryption key through quantum principles and then use that key to encrypt and decrypt messages using XOR-based symmetric encryption.

---

# Project Overview

Traditional communication systems rely on mathematical complexity for security. Quantum communication instead relies on the laws of quantum mechanics.

This project simulates a simplified quantum communication protocol where:

1. A sender generates random bits and random quantum bases.
2. A receiver independently chooses random measurement bases.
3. Qubits are encoded and measured using Qiskit quantum circuits.
4. Matching bases are used to establish a shared secret key.
5. The shared key is used for message encryption and decryption.

The system behaves similarly to a secure “walkie talkie” where both parties communicate using a quantum-generated secret key.

---

# Features

* BB84-style Quantum Key Distribution simulation
* Random quantum bit generation
* Quantum basis encoding and measurement
* Shared key establishment between sender and receiver
* XOR-based encryption and decryption
* Qiskit Aer simulator integration
* Iterative key generation until target key length is reached
* End-to-end communication testing

---

# Technologies Used

## Programming Language

* Python 3

## Libraries

* Qiskit
* Qiskit Aer
* Random

---

# Project Structure

```text
Quantum-Walkie-Talkie-main/
│
├── Project.py          # Main implementation of the quantum communication protocol
├── Tester.py           # Test script for running and validating the system
├── Report Code.pdf     # Supporting project documentation/report
└── README.md           # Project documentation
```

---

# How the System Works

## 1. Random Bit Generation

The sender generates:

* Random message bits
* Random encoding bases

The receiver generates:

* Random measurement bases

Example:

```python
sender_bits = [1,0,1,1]
sender_bases = [0,1,1,0]
receiver_bases = [0,1,0,0]
```

Where:

* `0` represents the standard computational basis
* `1` represents the Hadamard basis

---

# 2. Quantum Circuit Creation

A quantum circuit is created using Qiskit.

```python
QuantumCircuit(2,1)
```

The circuit contains:

* 2 qubits
* 1 classical bit

---

# 3. Sender Encoding

The sender encodes each bit into a qubit.

## Encoding Rules

### If bit = 1

Apply an X gate:

```python
circuit.x(qubit)
```

### If basis = 1

Apply a Hadamard gate:

```python
circuit.h(qubit)
```

This converts the qubit into the diagonal basis.

---

# 4. Receiver Measurement

The receiver measures the qubit using a randomly chosen basis.

If the receiver chooses the Hadamard basis:

```python
circuit.h(qubit)
```

Then the qubit is measured:

```python
circuit.measure(qubit, classical_bit)
```

---

# 5. Key Sifting

After transmission:

* Sender and receiver compare their chosen bases.
* Only positions where the bases match are kept.
* Matching bits form the shared secret key.

Example:

| Index | Sender Basis | Receiver Basis | Keep? |
| ----- | ------------ | -------------- | ----- |
| 0     | 0            | 0              | Yes   |
| 1     | 1            | 1              | Yes   |
| 2     | 0            | 1              | No    |
| 3     | 1            | 0              | No    |

Only matching positions contribute to the final key.

---

# 6. Encryption

The message is encrypted using XOR.

## Formula

```text
Encrypted Bit = Message Bit XOR Key Bit
```

## Implementation

```python
return [m ^ k for m, k in zip(message_bits, key_bits)]
```

---

# 7. Decryption

Decryption uses the same XOR operation.

```text
Original Message = Encrypted Bit XOR Key Bit
```

## Implementation

```python
return [e ^ k for e, k in zip(encrypted_bits, key_bits)]
```

Since XOR is reversible:

```text
(A XOR B) XOR B = A
```

The original message is recovered successfully.

---

# Main Classes and Functions

# QuantumWalkieTalkie Class

Located in:

```text
Project.py
```

This class manages the entire quantum communication workflow.

---

## Constructor

```python
__init__(self, bitlength=256)
```

Initializes:

* Key length
* Qiskit backend simulator

---

## generate_randomBitString()

```python
generate_randomBitString(length)
```

Generates random binary sequences.

### Example Output

```python
[1,0,1,1,0,0,1]
```

---

## create_circuit()

```python
create_circuit()
```

Creates a fresh quantum circuit.

---

## encode_sender_bit()

```python
encode_sender_bit(circuit, bit, basis)
```

Encodes a bit into a qubit using:

* X gate
* Hadamard gate

---

## encode_receiver_basis()

```python
encode_receiver_basis(circuit, basis)
```

Applies measurement basis selection and performs measurement.

---

## encryption()

```python
encryption(message_bits, key_bits)
```

Encrypts the message using XOR.

---

## decryption()

```python
decryption(encrypted_bits, key_bits)
```

Decrypts the encrypted message.

---

## run_key_exchange_iterative()

```python
run_key_exchange_iterative(target_key_length, batch_size)
```

Core implementation of the BB84-style key exchange.

### Responsibilities

* Generates random sender and receiver bases
* Runs quantum simulations
* Measures qubits
* Filters matching bases
* Builds final shared key
* Verifies sender and receiver keys match

---

# Example Execution Flow

## Step 1

Generate a random message.

```python
message = [0,1,1,0,1]
```

## Step 2

Run quantum key exchange.

```python
key_sender, key_receiver = qwt.run_key_exchange_iterative()
```

## Step 3

Encrypt the message.

```python
encrypted = qwt.encryption(message, key)
```

## Step 4

Decrypt the message.

```python
decrypted = qwt.decryption(encrypted, key)
```

## Step 5

Verify correctness.

```python
assert decrypted == message
```

---

# Running the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Quantum-Walkie-Talkie-main
```

---

## 2. Install Dependencies

Install Qiskit and Aer:

```bash
pip install qiskit qiskit-aer
```

---

## 3. Run the Test Program

```bash
python Tester.py
```

---

# Example Output

```text
Starting BB84-style key exchange...

---------- Iteration 1 ----------
Matched indices: [0, 2, 5]
Sender bits    : [1, 0, 1]
Receiver bits  : [1, 0, 1]

Shared key established successfully!

Shared Key: [1,0,1,1,...]
Message   : [0,1,1,0,...]
Encrypted : [1,1,0,1,...]
Decrypted : [0,1,1,0,...]

Success: Decrypted message matches original.
```

---

# Quantum Computing Concepts Used

## Qubit

A qubit is the quantum version of a classical bit.

Unlike classical bits:

* Classical bit → either 0 or 1
* Qubit → can exist in superposition

---

## Superposition

Using the Hadamard gate:

```text
|0⟩ → (|0⟩ + |1⟩)/√2
```

This allows quantum states to exist probabilistically.

---

## Quantum Measurement

Measuring a qubit collapses its state into either:

* 0
* 1

The result depends on the chosen measurement basis.

---

## BB84 Protocol

The BB84 protocol is one of the first quantum key distribution protocols.

It ensures:

* Secure key sharing
* Detection of eavesdropping
* Quantum-safe communication

This project implements a simplified simulation inspired by BB84.

---

# Security Perspective

This project demonstrates an important concept:

If an attacker measures a quantum state incorrectly:

* The state changes
* Errors are introduced
* Eavesdropping can potentially be detected

This is a major advantage of quantum cryptography compared to classical encryption.

---

# Limitations

This project is a simulation and not a production-ready quantum communication system.

Current limitations include:

* No real quantum hardware transmission
* No noise modeling
* No eavesdropper simulation
* No privacy amplification
* No error correction layer
* Uses classical XOR encryption after key generation

---

# Possible Future Improvements

Potential enhancements include:

* Add Eve (eavesdropper) simulation
* Implement error correction
* Add privacy amplification
* Support real IBM Quantum hardware
* Add GUI interface
* Real-time visualization of qubits
* Secure chat interface
* Networked communication between devices
* Noise and decoherence modeling
* Performance benchmarking

---

# Educational Value

This project is useful for learning:

* Quantum computing basics
* Quantum cryptography
* Qiskit programming
* BB84 protocol mechanics
* Quantum circuit simulation
* Secure communication concepts

It is suitable for:

* Computer science students
* Cybersecurity students
* Quantum computing beginners
* Research demonstrations
* Academic projects

---

# Dependencies

## Python Packages

```text
qiskit
qiskit-aer
```

---

# Author

Developed as a quantum communication simulation project using Python and Qiskit.

---

# License

This project is intended for educational and research purposes.
