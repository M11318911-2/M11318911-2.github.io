# 個人網頁模板 (Student Personal Webpage Template)

這是一個專為學生設計的個人網頁模板，整合了個人作業展示、MediaPipe 互動 Demo 以及 AI 聊天機器人功能。

## 📁 目錄結構說明

### 1. `PPT`：前兩週用到的PPT投影片

### 2. `YoutubeLink`：作業影片自動顯示開關
此目錄決定作業頁面是否顯示 YouTube 說明影片。
* **使用方式**：若繳交作業時需附帶說明影片，請在此目錄建立對應單元的 `.txt` 檔案（例如 `unit1.txt`）。
* **內容格式**：檔案內僅需放入 YouTube 影片網址（例如：`https://youtu.be/OOUMgliIskU`）。
* **自動化邏輯**：系統偵測到該檔案後，會在對應單元（如 Unit 1）作業下方自動嵌入該影片。

### 3. `mp`：MediaPipe 展示程式
存放多個基於 **Google MediaPipe** 開發的 AI 偵測範例，供課程實作參考。

### 4. `n8n`：自動化流程前端
包含執行 n8n 工作流時的前端 HTML 網頁介面。
* **延伸參考**：更多 n8n 相關整合應用可參考 [n8nAll 專案庫](https://github.com/ntust2026/n8nAll)。

### 5. `pic`：圖檔資源管理
* **個人頭像**：首頁顯示的個人大頭照，請命名為 `mypic.jpg`上傳。
* **作業圖片**：每一單元作業需提供三張圖，請遵循以下命名規則上傳：
  * **第一單元**：`unit1_1.jpg`, `unit1_2.jpg`, `unit1_3.jpg`
  * **第二單元**：`unit2_1.jpg`, `unit2_2.jpg`, `unit2_3.jpg`
  * 依此類推，確保系統能正確抓取圖片。
 
### 6. `unit12345`：前5個單元用到的python程式碼

---

## 🤖 彈出式 AI 聊天機器人實作 (`chatbot.js`)

本模板內建一個可嵌入任何 HTML 頁面的彈出式對話框。目前預設連向講師的 n8n 服務。

### 如何自訂您的機器人：
1. **修改連結**：開啟 `chatbot.js` 檔案，在 **第 6 行** 將 Webhook 網址更換為您自己的 n8n 連結（目前預設為我的 `https://a3g.app.n8n.cloud/webhook/chat_webhook`）。
2. **嵌入網頁**：在您的 HTML 檔案（如 `index.html`）中的 `<body>` 標籤之前加入腳本引用：
   ```html
   ...
   </head>
   <script src="chatbot.js"></script>
   <body>
   ...
完成後，您的網頁即具備彈出式智慧聊天機器人功能。

## 🌐 核心程式檔案說明
### index.html：個人首頁。
### index2.html：利用 MediaPipe 手部偵測開發的互動展示程式。
### perception_demo.html：整合多種 MediaPipe 偵測功能（如人臉、姿勢等）的示範頁面。
### unit.html：作業展示專用網頁，具備左右巡航按鈕可切換不同單元。
### word_vector_3d_plotly_with_word2vec.html：展示詞向量化 (Word2Vec) 的 3D 視覺化模型。

## 💖 樣式表 (CSS)：
### style.css：定義 unit.html 的版面風格。
### style2.css：定義 index.html 的版面風格。

Prof. Luarn
