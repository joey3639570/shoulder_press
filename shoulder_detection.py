import cv2
import mediapipe as mp
import math

# 初始化 MediaPipe 的相關物件
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """
    計算三點之間的夾角
    """
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# 讀取影片
video = cv2.VideoCapture('front.mp4')

# 取得影片資訊
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# 設定影片寫入器
output_video = cv2.VideoWriter('front_processed_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))


# 初始化 MediaPipe Pose 物件
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while video.isOpened():
        # 讀取影格
        ret, frame = video.read()
        if not ret:
            break

        # 轉換影格的色彩空間
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 進行人體骨架偵測
        results = pose.process(image)

        # 繪製人體骨架
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 計算角度
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 計算前臂與上臂的夾角
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_arm_angle = calculate_angle(left_wrist, left_elbow, left_shoulder)
             # 計算右手臂夾角
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            right_arm_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)


            # 計算上臂與身體的夾角
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_body_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
            # 計算右臂與身體夾角
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
            right_body_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
            
            # 顯示角度結果
            cv2.rectangle(image, (40, 20), (440, 90), (255,255,255), -1)
            cv2.rectangle(image, (image.shape[1] - 430, 20), (image.shape[1]-15, 90), (255,255,255), -1)
            cv2.putText(image, f"Left Arm Angle: {round(left_arm_angle, 2)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(image, f"Right Arm Angle: {round(right_arm_angle, 2)}", (image.shape[1] - 420, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(image, f"Left Body Angle: {round(left_body_angle, 2)}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(image, f"Right Body Angle: {round(right_body_angle, 2)}", (image.shape[1] - 420, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            # 繪製前臂和上臂直線
            cv2.line(image, (int(left_wrist[0] * image.shape[1]), int(left_wrist[1] * image.shape[0])),
                     (int(left_elbow[0] * image.shape[1]), int(left_elbow[1] * image.shape[0])), (255, 0, 0), 2)
            cv2.line(image, (int(left_elbow[0] * image.shape[1]), int(left_elbow[1] * image.shape[0])),
                     (int(left_shoulder[0] * image.shape[1]), int(left_shoulder[1] * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(left_shoulder[0] * image.shape[1]), int(left_shoulder[1] * image.shape[0])),
                     (int(left_hip[0] * image.shape[1]), int(left_hip[1] * image.shape[0])), (0, 0, 255), 2)
            cv2.line(image, (int(right_wrist[0] * image.shape[1]), int(right_wrist[1] * image.shape[0])),
                     (int(right_elbow[0] * image.shape[1]), int(right_elbow[1] * image.shape[0])), (255, 0, 0), 2)
            cv2.line(image, (int(right_elbow[0] * image.shape[1]), int(right_elbow[1] * image.shape[0])),
                     (int(right_shoulder[0] * image.shape[1]), int(right_shoulder[1] * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(right_shoulder[0] * image.shape[1]), int(right_shoulder[1] * image.shape[0])),
                     (int(right_hip[0] * image.shape[1]), int(right_hip[1] * image.shape[0])), (0, 0, 255), 2)

        # 將處理後的影格寫入影片
        output_video.write(image)

        # 顯示影像
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    video.release()
    output_video.release()
    cv2.destroyAllWindows()