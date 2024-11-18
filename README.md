# FlappyBird-Evolution

## 專案簡介

**FlappyBird-Evolution** 是一款基於經典遊戲 Flappy Bird 開發的 2D 遊戲，結合 Python 和 Pygame 實現，並新增兩種遊戲模式與 AI 操作功能。透過此專案，我們展示了遊戲開發與強化學習的結合應用。

### 功能特色
1. **多樣化遊戲模式**：
   - **經典模式 (Original Mode)**：控制小鳥躲避水管並持續累計分數。
   - **射擊模式 (Shooting Mode)**：小鳥可射擊星星，獲得額外分數，同時避開障礙物。
2. **AI 操作彩蛋**：
   - 按下 `A` 鍵啟用 AI 操控，讓小鳥自動遊玩（僅限經典模式）。
3. **動態遊戲難度**：
   - 水管的行為會隨分數增長變化，提供更具挑戰性的遊戲體驗。
4. **自製視聽資源**：
   - 包括音效與美術設計，增強遊戲的視覺和聽覺效果。

---

## 安裝與運行

### 環境需求
- **Python 版本**：3.8 或更高
- **所需套件**：
  - `pygame`
  - `stable-baselines3`
  - `gym`
  - `numpy`

### 安裝步驟
1. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
2. 啟動遊戲：
   ```bash
    python main.py
   ```

---

## 操作說明

### 選擇模式
- **按鍵 1** 或點擊「Mode 1」進入經典模式。
- **按鍵 2** 或點擊「Mode 2」進入射擊模式。
- 按 `R` 查看規則，按 `B` 返回首頁。

### 遊戲控制
- **跳躍**：按空白鍵 (Space)。
- **射擊**：按 `S` 鍵（僅限射擊模式）。
- **AI 操作**：按 `A` 鍵啟用或關閉 AI 操控。

### 重新開始
- 遊戲結束後，按空白鍵重新開始，或按 `M` 鍵返回主選單。

---

## 專案結構
- `main.py`：遊戲邏輯，包括經典模式與射擊模式的實現。
- `ai_bird.py`：AI 模型的訓練與評估腳本，基於 PPO 算法。
- `best_ppo_flappybird.zip`：已訓練完成的最佳 AI 模型。
- `ppo_flappybird.zip`：最新訓練的 AI 模型。

---

## AI 模型使用說明
1. 確保預訓練的模型檔案 `best_ppo_flappybird.zip` 位於專案根目錄。
2. 若未提供模型檔案，程式將自動訓練新模型（耗時較長）。
3. 手動訓練模型：
   ```bash
   python ai_bird.py

---

## 遊戲展示影片

觀看遊戲演示影片：[FlappyBird-Evolution 遊戲展示](https://youtu.be/Vb-z0siDLlw?si=4xciKY3SYUyinpOA)

