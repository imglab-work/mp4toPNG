import cv2
import os
import glob

# ==========================================
# 設定
# ==========================================
image_dir = "./output_painted"  # ペンキ塗りされた画像があるフォルダ
output_video_path = "./output_painted_video.mp4"
fps = 30  # 元の動画に合わせたフレームレート（約30fps）

# 1. フォルダ内の全PNG画像を取得
image_paths = glob.glob(os.path.join(image_dir, "*.png"))

if not image_paths:
    print(f"エラー: {image_dir} に画像が見つかりません。")
    exit()

# 2. 【重要】ファイル名の「秒数（数値）」で正しくソート
# 例: "3.636969.png" -> 3.636969 という float に変換して並び替える
image_paths.sort(key=lambda x: float(os.path.splitext(os.path.basename(x))[0]))

print(f"合計 {len(image_paths)} 枚の画像を時系列順にソートしました。")
print(f"最初のフレーム: {os.path.basename(image_paths[0])}")
print(f"最後のフレーム: {os.path.basename(image_paths[-1])}")

# 3. 最初の画像から動画の解像度（サイズ）を取得
first_img = cv2.imread(image_paths[0])
height, width, layers = first_img.shape
size = (width, height)

# 4. VideoWriterの初期化 (H.264 / MP4 形式)
# Windows環境で最も汎用性が高く軽量な 'mp4v' コーデックを使用します
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(output_video_path, fourcc, fps, size)

print("動画の書き込みを開始します...")
for idx, path in enumerate(image_paths):
    img = cv2.imread(path)
    video.write(img)
    
    # 100フレームごとに進捗を表示
    if idx % 100 == 0:
        print(f"進捗: {idx}/{len(image_paths)} フレーム書き込み完了")

# 5. 後片付け
video.release()
print(f"すべて完了しました！ 動画はここに保存されました: {output_video_path}")