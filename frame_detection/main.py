import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def process_frame(frame, img):
    result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)

    if result >= 0.7:
        return 1
    return 0


def count_occurrences(video_path, image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    height, width, _ = img.shape

    cap = cv2.VideoCapture(video_path)

    count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames, desc="Processing Frames", unit="frame")

    with ThreadPoolExecutor() as executor:
        futures = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            future = executor.submit(process_frame, frame, img)
            futures += [future]

            pbar.update(1)

        for future in futures:
            count += future.result()

    pbar.close()
    cap.release()
    return count


if __name__ == "__main__":
    video_path = "files/output.avi"
    image_path = "files/Fedor_Kuznetsov.png"

    occurrences = count_occurrences(video_path, image_path)
    print(f"Number of images: {occurrences}")
