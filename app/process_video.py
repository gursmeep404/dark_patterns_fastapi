import uuid, os, shutil, cv2
from app.utils.image_utils import image_to_base64
# from app.openai_vision import analyze_frame_with_gpt
from app.openai_vision import analyze_frame_with_gemini

def extract_frames_one_per_second(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    current_time = 0  # milliseconds
    index = 0
    frame_paths = []

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time)
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = f"frame_{index:04d}.jpg"
        frame_path = os.path.join(output_dir, frame_filename)
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_filename)

        index += 1
        current_time += 1000  # 1000 ms = 1 second

    cap.release()
    return frame_paths

async def analyze_video_pipeline(file):
    uid = str(uuid.uuid4())
    video_path = f"temp_{uid}.mp4"
    frames_dir = f"frames_{uid}"

    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    frame_paths = extract_frames_one_per_second(video_path, frames_dir)
    os.remove(video_path)

    results = []

    for frame_index, frame in enumerate(frame_paths):
        image_path = os.path.join(frames_dir, frame)
        b64_image = image_to_base64(image_path)

        # frame_results = analyze_frame_with_gpt(b64_image)
        frame_results = analyze_frame_with_gemini(b64_image)

        if not isinstance(frame_results, list):
            frame_results = [frame_results]

        for result in frame_results:
            result["frame_id"] = frame_index + 1  
            result["frame"] = frame
            result["image"] = b64_image  
            results.append(result)

    # Cleanup frame folder
    shutil.rmtree(frames_dir)

    return results
