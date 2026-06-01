import cv2
import os

def extract_frames_for_slam(video_path, output_dir):
    """
    MP4動画を連番画像(PNG)に分解し、タイムスタンプをファイル名にして保存する
    """
    # 出力先フォルダの作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"フォルダを作成しました: {output_dir}")

    # 動画の読み込み
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"エラー: 動画ファイル '{video_path}' が開けません。パスを確認してください。")
        return

    # 動画情報の取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"--- 動画情報 ---")
    print(f"FPS: {fps:.2f}")
    print(f"総フレーム数: {total_frames}")
    print(f"----------------")

    frame_count = 0
    
    print("画像の抽出を開始します...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 動画の最後まで到達したら終了

        # ==========================================
        # タイムスタンプの計算 (ここがSLAMにおいて超重要)
        # ==========================================
        # フレーム番号とFPSから、正確な経過時間(秒)を計算する
        # ※cv2.CAP_PROP_POS_MSECを使う方法もありますが、
        # SLAMではコマ間の時間が完全に等間隔(CFR)であることが好まれるため、計算で割り出します。
        timestamp_sec = frame_count / fps

        # ファイル名を「秒数.png」にする（小数点以下6桁 = マイクロ秒精度）
        # 例: 0.000000.png, 0.033333.png
        filename = f"{timestamp_sec:.6f}.png"
        filepath = os.path.join(output_dir, filename)

        # 画像の保存 (PNG形式は劣化がないためSLAMに最適ですが、容量は大きくなります)
        cv2.imwrite(filepath, frame)
        
        frame_count += 1

        # 進行状況の表示 (100フレームごと)
        if frame_count % 100 == 0:
            progress = (frame_count / total_frames) * 100
            print(f"抽出中... {frame_count}/{total_frames} 枚完了 ({progress:.1f}%)")

    # メモリの解放
    cap.release()
    print(f"\n完了！ 合計 {frame_count} 枚の画像を '{output_dir}' に保存しました。")

if __name__ == "__main__":
    # 読み込むMP4動画のパスを指定
    VIDEO_FILE = "input/VID_20260531_084459_026_Liner.mp4"  # ← ここをご自身の動画パスに変更してください
    
    # 画像を保存するフォルダのパスを指定
    # ※SLAMの標準データセット(EuRoC形式)に合わせるため、「cam0/data」という階層にするのがおすすめです
    OUTPUT_FOLDER = "output" 
    
    extract_frames_for_slam(VIDEO_FILE, OUTPUT_FOLDER)