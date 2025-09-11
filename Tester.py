from Project import QuantumWalkieTalkie
import random

def test_qwt_protocol():
    message = [random.randint(0, 1) for _ in range(128)]
    qwt = QuantumWalkieTalkie()

    print("\n Starting BB84-style key exchange...")
    key_sender, key_receiver = qwt.run_key_exchange_iterative(target_key_length=128)

    print("\n Verifying key agreement...")
    assert key_sender == key_receiver, "❌ Keys do not match — QKD failed!"
    key = key_sender

    print("\n Shared Key:", key)
    print(" Message   :", message)

    encrypted = qwt.encryption(message, key)
    print("\n Encrypted:", encrypted)

    decrypted = qwt.decryption(encrypted, key)
    print(" Decrypted:", decrypted)

    assert decrypted == message, "❌ Decryption failed!"
    print(" Success: Decrypted message matches original.")

if __name__ == "__main__":
    test_qwt_protocol()
    