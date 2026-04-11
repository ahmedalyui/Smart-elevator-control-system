print("🚀 Smart Elevator System Starting...")

# Import modules
import hand_detection_and_tracking as hand
import face_recognition as face
import keypad_and_servomotor as keypad
import encoder as motor
import speech_recognition as speech

print("✔ Modules Loaded Successfully")

print("\n📌 System Status:")
print("- Hand Detection Ready")
print("- Face Recognition Ready")
print("- Keypad System Ready")
print("- Motor Control Ready")
print("- Speech Recognition Ready")

print("\n✅ SYSTEM READY - ELEVATOR ONLINE 🔥")


# ===== MAIN CONTROL LOOP =====
while True:

    print("\nChoose Mode:")
    print("1 - Hand Detection")
    print("2 - Face Recognition")
    print("3 - Keypad System")
    print("4 - Motor Test")
    print("5 - Speech Command")
    print("0 - Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        hand.run_hand_detection()

    elif choice == "2":
        face.run_face_recognition()

    elif choice == "3":
        keypad.main()

    elif choice == "4":
        motor.motor_forward(1)
        motor.motor_backward(1)

    elif choice == "5":
        speech.run_speech_recognition()

    elif choice == "0":
        print("Shutting down system...")
        break

    else:
        print("Invalid choice!")