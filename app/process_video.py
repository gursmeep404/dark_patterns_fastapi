import uuid, os, shutil
from app.utils.frame_utils import extract_frames
from app.utils.image_utils import image_to_base64
from app.openai_vision import analyze_frame_with_gpt
from app.mappings.legal_mapping import map_laws

async def analyze_video_pipeline(file):
    uid = str(uuid.uuid4())
    video_path = f"temp_{uid}.mp4"
    frames_dir = "frames"

    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    frame_paths = extract_frames(video_path, frames_dir, every_n_frames=30)
    os.remove(video_path)

    results = []
    for frame in frame_paths:
        b64 = image_to_base64(os.path.join(frames_dir, frame))
        result = analyze_frame_with_gpt(b64)
        result["frame"] = frame
        result["mapped_violations"] = map_laws(result.get("pattern", ""))
        results.append(result)

    # Cleanup frames
    for frame in frame_paths:
        os.remove(os.path.join(frames_dir, frame))

    return results
