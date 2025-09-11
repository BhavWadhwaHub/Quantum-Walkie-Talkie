from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random

class QuantumWalkieTalkie:

    def __init__(self, bitlength=256):
        self.n = bitlength
        self.backend = Aer.get_backend('qasm_simulator')

    def generate_randomBitString(self, length):
        return [random.randint(0, 1) for _ in range(length)]

    def create_circuit(self):
        return QuantumCircuit(2, 1)

    def encode_sender_bit(self, circuit, bit, basis, Qbit_index=0):
        if bit == 1:
            circuit.x(Qbit_index)
        if basis == 1:
            circuit.h(Qbit_index)

    def encode_receiver_basis(self, circuit, basis, Qbit_index=1):
        if basis == 1:
            circuit.h(Qbit_index)
        circuit.measure(Qbit_index, 0)

    def encryption(self, message_bits, key_bits):
        return [m ^ k for m, k in zip(message_bits, key_bits)]

    def decryption(self, encrypted_bits, key_bits):
        return [e ^ k for e, k in zip(encrypted_bits, key_bits)]

    def run_key_exchange_iterative(self, target_key_length=128, batch_size=16):
        sender_final_key = []
        receiver_final_key = []
        attempt = 1

        while len(sender_final_key) < target_key_length:
            print(f"\n---------- Iteration {attempt} ----------")
            sender_bits = self.generate_randomBitString(batch_size)
            sender_bases = self.generate_randomBitString(batch_size)
            receiver_bases = self.generate_randomBitString(batch_size)
            receiver_measurements = []

            for i in range(batch_size):
                circuit = self.create_circuit()
                self.encode_sender_bit(circuit, sender_bits[i], sender_bases[i])
                self.encode_receiver_basis(circuit, receiver_bases[i])

                compiled = transpile(circuit, backend=self.backend)
                job = self.backend.run(compiled, shots=1)
                result = job.result().get_counts()
                outcome = list(result.keys())[0]
                measured_bit = int(outcome)
                receiver_measurements.append(measured_bit)

            matched_indices = [i for i in range(batch_size) if sender_bases[i] == receiver_bases[i]]
            matched_sender_bits = [sender_bits[i] for i in matched_indices]
            matched_receiver_bits = [receiver_measurements[i] for i in matched_indices]

            print(f"Matched indices: {matched_indices}")
            print(f"Sender bits    : {matched_sender_bits}")
            print(f"Receiver bits  : {matched_receiver_bits}")

            for s_bit, r_bit in zip(matched_sender_bits, matched_receiver_bits):
                if s_bit == r_bit:
                    sender_final_key.append(s_bit)
                    receiver_final_key.append(r_bit)

            print(f"Accumulated key length: {len(sender_final_key)}")
            attempt += 1

        if sender_final_key[:target_key_length] != receiver_final_key[:target_key_length]:
            raise ValueError("Sender and receiver keys do not match! QKD failed.")
        
        print("\n Shared key established successfully!")
        return sender_final_key[:target_key_length], receiver_final_key[:target_key_length]
