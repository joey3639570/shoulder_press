# shoulder_press
A simple Python script using MediaPipe and OpenCV to calculate shoulder and arm angles from video input and visualize the results in real-time.

肩部與手臂角度偵測工具（使用 MediaPipe）
本專案使用 MediaPipe Pose 與 OpenCV，從影片中偵測人體關鍵點，計算左/右手臂與肩膀的夾角，並即時將資訊與骨架線條疊加於畫面中。

🔧 功能特色
使用 MediaPipe Pose 偵測人體 33 個關鍵點

計算以下兩類角度：

手臂角度（手腕－手肘－肩膀）

身體角度（手肘－肩膀－髖部）

實時在畫面上繪製：

骨架連接線

各角度的數值

手臂與身體關節間的連線

將處理後結果輸出為影片 front_processed_video.mp4

📁 檔案說明
shoulder_detection.py：主程式

front.mp4：輸入影片（使用者需自備）

front_processed_video.mp4：輸出影片（包含骨架與角度資訊）

▶️ 執行方式
請先安裝所需套件：

bash
複製
編輯
pip install opencv-python mediapipe
執行主程式：

bash
複製
編輯
python shoulder_detection.py
執行時會開啟影片畫面，可即時觀察角度變化，按下 q 可中止處理。

🎯 適用情境
姿勢與動作分析

運動訓練姿勢評估

人體工學姿勢調整觀察

⚠️ 注意事項
請確保輸入影片 front.mp4 已放置於與腳本相同資料夾中。

若未偵測到人體骨架，畫面上不會顯示角度資訊。
