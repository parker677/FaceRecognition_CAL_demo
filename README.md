# 🐾 顔から分かる動物タイプ診断

顔画像から、あなたの動物タイプを診断するアプリです。
Streamlitで開発されており、Streamlit Cloudで無料ホスティング可能です。

## 機能

- 🖼️ 顔画像のアップロード
- 🎯 深層学習モデルによる動物タイプ診断
- 📊 診断結果の詳細表示
- 🔗 QRコード生成（アプリ共有用）

## 対応する動物タイプ

- リス (다람쥐)
- 猫 (고양이)
- 鹿 (사슴)
- 恐竜 (공룡)
- 犬 (강아지)
- 狐 (여우)
- 馬 (말)
- 兎 (토끼)
- 亀 (거북이)
- 狼 (늑대)

## ローカル実行

### 要件
- Python 3.8以上
- pip

### インストール

```bash
# 依存ライブラリをインストール
pip install -r requirements.txt
```

### 実行

```bash
streamlit run streamlit_app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

## Streamlit Cloudへの配置

### ステップ1: GitHubリポジトリを作成

```bash
# リポジトリを初期化
git init
git add .
git commit -m "Initial commit"

# GitHub上にリポジトリを作成してからプッシュ
git remote add origin https://github.com/YOUR_USERNAME/faceai.git
git push -u origin main
```

### ステップ2: Streamlit Cloudに接続

1. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
2. GitHubアカウントでログイン
3. 「New app」をクリック
4. 以下の情報を入力：
   - **Repository**: `YOUR_USERNAME/faceai`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. 「Deploy」をクリック

### ステップ3: デプロイ確認

デプロイが完了すると、Streamlit Cloudから一意のURLが割り当てられます。
例: `https://faceai-animal.streamlit.app`

## ファイル構成

```
faceai/
├── streamlit_app.py           # Streamlitアプリケーション
├── requirements.txt           # Python依存ライブラリ
├── .gitignore                # Gitが無視するファイル
├── models/
│   ├── animal_onlyface100_model.pkl          # 学習済みモデル
│   └── label_onlyface100_encoder.pkl         # ラベルエンコーダー
├── README.md                 # このファイル
└── app.py                   # 古いFlaskアプリ（参考用）
```

## トラブルシューティング

### OpenCVエラーが発生する場合
- Windows環境では`opencv-python-headless`が必要です
- `pip install opencv-python-headless==4.8.1.78`

### DeepFaceがエラーを出す場合
- 初回実行時に学習済みモデルをダウンロードします
- インターネット接続が必要です

### Streamlit Cloudでのメモリ不足
- 画像サイズが大きい場合、圧縮して試してください
- Streamlit CloudはRAM 1GBの制限があります

## 環境変数（オプション）

Streamlit Cloudで秘密情報が必要な場合：

1. Streamlit Cloudのアプリ設定（⚙️）を開く
2. 「Secrets」タブから環境変数を追加

## ライセンス

MIT License

## 作成者

Face AI Project Team

---

**注意**: 
- モデルファイル（`*.pkl`）がGitHubにプッシュされていることを確認してください
- 初回デプロイ時にモデルが読み込まれるまで時間がかかる場合があります
