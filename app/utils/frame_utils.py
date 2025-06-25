import cv2, os

def extract_frames(video_path, output_folder, every_n_frames=30):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_id, count = 0, 0
    filenames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % every_n_frames == 0:
            filename = f"frame_{frame_id}.jpg"
            path = os.path.join(output_folder, filename)
            cv2.imwrite(path, frame)
            filenames.append(filename)
            frame_id += 1
        count += 1

    cap.release()
    return filenames
