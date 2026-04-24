import cv2
import mediapipe as mp
import serial
import time
import random

# ==============================
# Initialize MediaPipe Hand Detector
# ==============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# ==============================
# Initialize Serial Communication with Arduino
# ==============================
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("✅ Arduino connected successfully")
except Exception as e:
    print(f"❌ Error connecting to Arduino: {e}")
    arduino = None

# ==============================
# Helper functions
# ==============================
def get_finger_status(hand_landmarks):
    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]
    thumb_open = 1 if thumb_tip.x < thumb_ip.x else 0

    fingers = [
        {'tip': 8, 'mcp': 5},   # index
        {'tip': 12, 'mcp': 9},  # middle
        {'tip': 16, 'mcp': 13}, # ring
        {'tip': 20, 'mcp': 17}  # little
    ]

    finger_status = [thumb_open]
    for finger in fingers:
        tip_y = hand_landmarks[finger['tip']].y
        mcp_y = hand_landmarks[finger['mcp']].y
        finger_status.append(1 if mcp_y - tip_y > 0.05 else 0)
    return finger_status

def classify_gesture(finger_status):
    thumb, index, middle, ring, little = finger_status
    # Rock: All closed
    if sum(finger_status) == 0:
        return "rock", [135,135,135,135,0]
    # Paper: All open
    elif sum(finger_status) == 5:
        return "paper", [0,0,0,0,135]
    # Scissors: Only index & middle open
    elif index == 1 and middle == 1 and ring == 0 and little == 0:
        return "scissors", [135,0,0,135,]
    else:
        return "unknown", None

def send_to_arduino(angles):
    if arduino and arduino.is_open and angles:
        command = f"CH8:{angles[0]},CH15:{angles[1]},CH5:{angles[2]},CH3:{angles[3]},CH12:{angles[4]}\n"
        try:
            arduino.write(command.encode())
        except Exception as e:
            print(f"❌ Error sending to Arduino: {e}")

def decide_winner(user, robot):
    if user == robot:
        return "Draw", 0, 0
    elif (user == "rock" and robot == "scissors") or \
         (user == "scissors" and robot == "paper") or \
         (user == "paper" and robot == "rock"):
        return "You Win", 1, 0
    else:
        return "Robot Wins", 0, 1

def draw_countdown(frame, text, color=(255, 255, 255)):
    """Draw large centered countdown text"""
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 3
    thickness = 5
    
    # Get text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Calculate center position
    height, width = frame.shape[:2]
    x = (width - text_width) // 2
    y = (height + text_height) // 2
    
    # Draw text with black outline
    cv2.putText(frame, text, (x, y), font, font_scale, (0, 0, 0), thickness + 3)
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)

# ==============================
# Game State Variables
# ==============================
TOTAL_ROUNDS = 5
current_round = 1
user_score = 0
robot_score = 0

# Game states
STATE_COUNTDOWN = "countdown"
STATE_SHOW = "show"
STATE_RESULT = "result"
STATE_NEXT_ROUND = "next_round"
STATE_GAME_OVER = "game_over"

game_state = STATE_COUNTDOWN
countdown_start_time = None
countdown_value = 3
robot_choice = None
robot_angles = None
user_move = None
result_text = ""

# ==============================
# Main Loop
# ==============================
cap = cv2.VideoCapture(0)

print(f"\n🎮 Starting Rock Paper Scissors - {TOTAL_ROUNDS} Rounds!")
print("Show your gesture when the countdown reaches SHOOT!\n")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # ==============================
    # STATE: COUNTDOWN (3...2...1...SHOOT!)
    # ==============================
    if game_state == STATE_COUNTDOWN:
        if countdown_start_time is None:
            countdown_start_time = time.time()
            countdown_value = 3
        
        elapsed = time.time() - countdown_start_time
        
        if elapsed < 1:
            draw_countdown(frame, "3", (0, 255, 255))
        elif elapsed < 2:
            draw_countdown(frame, "2", (0, 165, 255))
        elif elapsed < 3:
            draw_countdown(frame, "1", (0, 100, 255))
        elif elapsed < 4:
            draw_countdown(frame, "SHOOT!", (0, 255, 0))
        else:
            # Move to SHOW state
            game_state = STATE_SHOW
            countdown_start_time = None
            # Robot makes random choice
            robot_choice = random.choice(["rock", "paper", "scissors"])
            
            # Get robot angles
            if robot_choice == "rock":
                robot_angles = [135, 135, 135, 135, 0]
            elif robot_choice == "paper":
                robot_angles = [0, 0, 0, 0, 135]
            else:  # scissors
                robot_angles = [135, 0, 0, 135, 0]
            
            send_to_arduino(robot_angles)
            print(f"🤖 Robot chose: {robot_choice}")

    # ==============================
    # STATE: SHOW (Capture user gesture)
    # ==============================
    elif game_state == STATE_SHOW:
        user_move = "unknown"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_status = get_finger_status(hand_landmarks.landmark)
                user_move, _ = classify_gesture(finger_status)
        
        # Check if user made a valid move
        if user_move in ["rock", "paper", "scissors"]:
            # Calculate result
            result_text, user_point, robot_point = decide_winner(user_move, robot_choice)
            user_score += user_point
            robot_score += robot_point
            
            print(f"👤 You chose: {user_move}")
            print(f"📊 Result: {result_text}")
            print(f"🏆 Score - You: {user_score} | Robot: {robot_score}\n")
            
            game_state = STATE_RESULT
            countdown_start_time = time.time()
        
        # Display instructions
        cv2.putText(frame, "Show your gesture!", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    # ==============================
    # STATE: RESULT (Show result for 3 seconds)
    # ==============================
    elif game_state == STATE_RESULT:
        elapsed = time.time() - countdown_start_time
        
        if elapsed > 3:  # Show result for 3 seconds
            if current_round < TOTAL_ROUNDS:
                current_round += 1
                game_state = STATE_NEXT_ROUND
                countdown_start_time = time.time()
            else:
                game_state = STATE_GAME_OVER
        
        # Display result
        cv2.putText(frame, f"Your Move: {user_move}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Robot Move: {robot_choice}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"{result_text}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # ==============================
    # STATE: NEXT ROUND (Transition message)
    # ==============================
    elif game_state == STATE_NEXT_ROUND:
        elapsed = time.time() - countdown_start_time
        
        if elapsed > 2:  # Show "Next Round" for 2 seconds
            game_state = STATE_COUNTDOWN
            countdown_start_time = None
        
        draw_countdown(frame, f"Round {current_round}", (255, 255, 0))

    # ==============================
    # STATE: GAME OVER (Final scores)
    # ==============================
    elif game_state == STATE_GAME_OVER:
        # Determine overall winner
        if user_score > robot_score:
            final_result = "🏆 YOU WIN THE GAME! 🏆"
            color = (0, 255, 0)
        elif robot_score > user_score:
            final_result = "🤖 ROBOT WINS THE GAME! 🤖"
            color = (0, 0, 255)
        else:
            final_result = "🤝 IT'S A TIE! 🤝"
            color = (255, 255, 0)
        
        cv2.putText(frame, final_result, (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame, f"Final Score - You: {user_score} | Robot: {robot_score}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'Q' to exit", (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        print(f"\n{final_result}")
        print(f"Final Score - You: {user_score} | Robot: {robot_score}")
        
        # Wait for 5 seconds then exit
        time.sleep(5)
        break

    # ==============================
    # Display persistent info (Round & Score)
    # ==============================
    if game_state != STATE_GAME_OVER:
        cv2.putText(frame, f"Round: {current_round}/{TOTAL_ROUNDS}", (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Score - You: {user_score} | Robot: {robot_score}", (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("✊✋✌ Rock Paper Scissors - 5 Rounds", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==============================
# Clean up
# ==============================
cap.release()
cv2.destroyAllWindows()
if arduino and arduino.is_open:
    arduino.close()
    print("🔌 Arduino connection closed")