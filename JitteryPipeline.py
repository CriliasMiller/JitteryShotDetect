from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
import os

def detect_jittery_motion_SceneDetect(video_path, threshold=20, scene_threshold=3, min_scene_len=15, window_duration=1):
    video_stream = open_video(video_path)
    scene_manager = SceneManager()
    
    
    video_duration = video_stream.duration.get_seconds()
    video_fps = video_stream.frame_rate
    
    window_frame_count = int(window_duration * video_fps)
    min_scene_len = window_frame_count // 10
    scene_manager.add_detector(ContentDetector(threshold, min_scene_len))
    scene_manager.detect_scenes(video=video_stream)
    
    scene_list = scene_manager.get_scene_list()
    print(f"{video_path} : {len(scene_list)} scenes detected")
    
    jitter_detected = False
    
    for start_time in range(0, int(video_duration), window_duration):
        end_time = min(start_time + window_duration, video_duration)
        window_scenes = [scene for scene in scene_list if scene[0].get_seconds() >= start_time and scene[1].get_seconds() <= end_time]
        
        shots_per_second = len(window_scenes) / window_duration
        print(f"Time window {start_time}s - {end_time}s: {shots_per_second:.2f} shots per second")
        if shots_per_second >= scene_threshold:
            jitter_detected = True
            
            break
    
    return jitter_detected
    
if __name__ == '__main__':
    files_path = 'Your video path'

    files = [ f for f in os.listdir(files_path) if f.endswith('mp4')]
    print(len(files))
    jittert_file = []
    for file in files:
        video_path = os.path.join(files_path, file)
        jittery = detect_jittery_motion_SceneDetect(video_path, window_duration=1)
        if jittery:
            jittert_file.append(video_path)
            print(video_path)
        # else:
            # print(f"{file} is not jittery")
    with open('jittery.txt', 'w') as f:
        for file in jittert_file:
            f.write(file + '\n')
    print(f'Jittery videos: {jittert_file}')
    print(f"Number of jittery videos: {len(jittert_file)}")
    
