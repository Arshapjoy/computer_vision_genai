import cv2

def calculate_brightness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2].mean() 
    return brightness

def classify_frame(brightness, thresholds):
    if brightness > thresholds['day']:
        return 'Day'
    elif thresholds['evening'] < brightness <= thresholds['day']:
        return 'Evening'
    else:
        return 'Night'

def annotate_video(input_path, output_path, thresholds):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return

   
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_index = 0
    frame_counts = {'Day': 0, 'Evening': 0, 'Night': 0}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        brightness = calculate_brightness(frame)
        classification = classify_frame(brightness, thresholds)
        frame_counts[classification] += 1

        
        text = f"Frame: {frame_index}, Time: {classification}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        
        out.write(frame)
        frame_index += 1

    cap.release()
    out.release()

   
    total_frames = sum(frame_counts.values())
    percentages = {key: (count / total_frames) * 100 for key, count in frame_counts.items()}
    
    print(f"Annotated video saved to {output_path}")
    print(f"Frame Classification Percentages:")
    print(f"Day: {percentages['Day']:.2f}%")
    print(f"Evening: {percentages['Evening']:.2f}%")
    print(f"Night: {percentages['Night']:.2f}%")


thresholds = {
    'day': 120,      
    'evening': 70,   
    'night': 0       
}


input_video_path = r"E:\cv_genai\Day-3\data\timelapse.mp4"  
output_video_path = r"E:\cv_genai\Day-3\data\annotated_timelapse.avi"  


annotate_video(input_video_path, output_video_path, thresholds)
