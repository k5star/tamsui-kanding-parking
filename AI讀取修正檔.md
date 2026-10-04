# AI 讀取修正檔（請 AI 在修改前完整讀完）

> 給 AI 的指示：你正在協助修改「淡水崁頂五路停車場」網站。
> 在動手修改任何檔案之前，請先完整讀完本檔案，並遵守其中的規則。
> 讀完後，請先用 3–5 句話回覆你理解的專案重點與本次要修改的範圍，等使用者確認後再開始修改。

---

## 1. 專案基本資料

| 項目 | 內容 |
|---|---|
| 網站名稱 | 淡水崁頂五路停車場 |
| 網站用途 | 淡水海岸旅遊 × 停車資訊 Landing Page，同時是 Google Ads 的正式到達網頁 |
| 本機工作資料夾 | `D:\github上傳夾\tamsui-kanding-parking` |
| GitHub | https://github.com/k5star/tamsui-kanding-parking （Private） |
| 正式分支 | `main`（push 到 main 會觸發 Cloudflare Pages 自動部署） |
| 技術 | 純靜態 HTML + CSS，無框架，頁面不需要 JavaScript |
| 建置 | `npm run build` → 執行 `python3 build.py` → 輸出 `dist/` |
| 主要使用者 | 開車到淡水遊玩的旅客，**手機優先（Mobile First）** |

---

## 2. 已確認的停車場資料（唯一可信來源）

以下是使用者提供、已確認的資料。網站內容只能使用這些資料：

| 項目 | 內容 |
|---|---|
| 名稱 | 淡水崁頂五路停車場 |
| 地址 | 新北市淡水區崁頂五路（淡海新市鎮） |
| 平日 | 每小時 10 元 |
| 假日 | 每小時 20 元 |
| 每日最高 | 80 元 |
| 月租 | 1,000 元 |
| 免費時間 | 前 10 分鐘免費 |
| 付款方式 | LINE Pay / ATM 等 |
| 進出方式 | 免柵欄，不需取票 |
| Google Maps 導航連結 | `https://maps.app.goo.gl/ASsbAQvR1QARp5GZ9?g_st=ac` |
| 周邊 | 金色水岸觀海長堤、淡水海岸、自行車道、海尾仔沙灘、YouBike 2.0、水管公園、淡江教會淡海堂 |

**尚未確認（不可自行填寫）**：電話、經緯度、營業時間、評分、評論數、精確步行距離或分鐘數。

> 規則：任何不在上表的停車場資料，**不要自行杜撰**。若使用者要求加入新資料，請以使用者提供的內容為準，並在本表同步更新。

---

## 3. 檔案結構

```
src/index.html          ← 唯一頁面，所有內容、CSS、JSON-LD 都在這裡（主要修改這個檔案）
src/assets/img/         ← 圖片（WebP / AVIF）；map-original.png 是原始素材，不會輸出
build.py                ← 建置腳本：src/ → dist/，處理 SITE_URL、robots.txt、sitemap.xml、_headers
tests/check_build.py    ← SITE_URL 建置測試（9 項）
tests/check_site.py     ← Playwright 網站檢查（55 項）
package.json            ← npm 指令（build / lint / test / serve）
.nvmrc                  ← Node 版本 22
README.md               ← 一般說明
AI讀取修正檔.md          ← 本檔案
```

**絕對不要修改 `dist/`**：它是建置產物，每次 build 都會被覆蓋，也不會上傳到 GitHub。

---

## 4. 首頁區塊與位置（src/index.html）

| 順序 | 區塊 | HTML 標記 |
|---|---|---|
| — | 頂部選單 | `<header class="site-header">` |
| 01 | Hero 主視覺（名稱、副標、費率重點、地址、導航按鈕） | `<section class="hero" id="top">` |
| 02 | 停車場特色（5 張卡片） | `<section id="features">` |
| 03 | 停車費率（價格卡） | `<section id="pricing">` |
| 04 | 周邊景點（6 張圖片卡片） | `<section id="spots">` |
| 05 | 夕陽主題區 | `<section class="sunset" id="sunset">` |
| 06 | 停車＋騎車流程 | `<section id="bike">` |
| 07 | 地圖與導航 | `<section id="map">` |
| 08 | FAQ 常見問題 | `<section id="faq">` |
| 09 | Footer | `<footer>` |
| — | 手機底部 Sticky 導航列 | `<nav class="mbar">`（1024px 以下顯示） |

CSS 寫在 `<head>` 的 `<style>` 中，顏色使用 `:root` 的 CSS 變數（例如 `--sea`、`--sun`），並有深色模式設定。

---

## 5. 重要：同一資料出現在多個位置

修改以下資料時，**所有位置都要一起改**，否則網頁會前後矛盾（Google Ads 也可能因此拒登）。

### 改「費率」時，要檢查這些地方
1. `<meta name="description">`
2. `<meta property="og:description">`
3. JSON-LD（ParkingFacility）的 `priceRange`
4. JSON-LD（FAQPage）的「停車費多少？」「有免費時間嗎？」答案
5. Hero 的費率重點 `<ul class="quick">`
6. 停車場特色卡片 `#features`
7. 停車費率價格卡 `#pricing`
8. FAQ 區塊 `#faq` 中看得到的答案
9. `tests/check_site.py` 中的 `PRICES` 清單與費率文字檢查
10. 本檔案第 2 節的資料表

建議做法：先用搜尋找出所有出現處，例如搜尋 `10 元`、`NT$10`、`$10`、`80`。

### 改「Google Maps 連結」時
連結出現在 7 個地方：JSON-LD 的 `hasMap`、頂部選單按鈕、Hero 按鈕、夕陽區按鈕、地圖區按鈕、Footer、手機 Sticky 導航列。請用「全部取代」一次改完，並同步更新 `tests/check_site.py` 的 `MAPS` 變數與本檔案第 2 節。

### FAQ 規則
看得到的 FAQ（`#faq`）和 JSON-LD 的 FAQPage 內容**必須一字不差地一致**。新增、刪除或修改問答時兩邊都要改，並更新測試中的 FAQ 題數（目前 5 題）。

---

## 6. 修改規則

### 必須遵守
- 只改使用者要求的部分，**不要重寫整個網站**，不要刪除既有功能。
- 保持 **Mobile First**：手機開啟後第一個畫面要看得到「停車場名稱、價格、地址、立即導航按鈕」。
- 「立即導航」必須維持是最明顯的按鈕（橘色 `btn-primary`）。
- 費率附近要保留「實際收費及付款方式仍以現場公告為準」，Footer 也要保留免責聲明。
- 頁面只能有一個 `<h1>`。
- 不要新增 JavaScript，除非使用者明確要求而且有必要。
- 文字使用繁體中文（台灣用語）。

### 不可以做
- 不可杜撰電話、營業時間、經緯度、評分、評論、距離或分鐘數。
- 不可加入 `noindex`，也不可在 robots.txt 禁止搜尋引擎。
- 不可加入彈出視窗或會擋住主要內容的元素（Google Ads 政策）。
- 不可修改 `dist/`。
- 不可 `git push --force`，不可刪除 branch 或 tag（`v2-baseline`、`v3.0.0`）。
- 不可把 API Key、Token、密碼或 `.env` 寫進任何檔案或 commit。

### SEO 原則
- Title：`淡水崁頂五路停車場｜淡水夕陽・觀海長堤附近停車`（如需修改請先問使用者）。
- 關鍵字要自然地出現在標題、段落、FAQ、圖片 alt 中，**不要堆砌關鍵字**。
- 主要關鍵字：淡水停車場、淡水夕陽停車、觀海長堤停車、金色水岸停車、淡水海邊停車、淡水自行車道停車、淡海新市鎮停車場、淡水平價停車場。

### 圖片規則
- 新圖片放在 `src/assets/img/`，使用 WebP（大圖可加 AVIF），寬度建議不超過 1600px。
- `<img>` 必須有：有意義的 `alt`（可自然帶入關鍵字）、`width`、`height`、`loading="lazy"`、`decoding="async"`。
- Hero 首屏不要放超大背景圖。
- 目前景點圖片是從 AI 繪製的周邊景點地圖裁切而來，解析度偏低，**建議換成實拍照片**。

---

## 7. 修改後必做的檢查

依序執行，**全部通過才可以 commit / push**：

```
npm install          # 第一次或 package.json 變動時
npm run build        # 必須成功產生 dist/
npm run lint         # 必須 0 錯誤
npm test             # 必須全部通過（目前 9 + 55 項）
npm run serve        # 開 http://localhost:8080 目視確認
```

`npm test` 需要 Python Playwright：`pip install playwright` 與 `playwright install chromium`。

若是合理的內容變更造成測試失敗（例如使用者改了價格），請**同步更新測試的預期值**，並在回報中說明；不要為了通過測試而刪除檢查項目。

測試會產生 `screenshots/`（不會上傳 GitHub），可用來檢查 375 / 390 / 430 / 768 / 1024 / 1440px 的畫面。

---

## 8. Git 與部署流程

```
git pull                                  # 先同步最新版本
（修改檔案）
npm run build && npm run lint && npm test # 檢查
git add .
git commit -m "簡短說明這次改了什麼"
git push                                  # push 到 main 後 Cloudflare Pages 自動部署
```

- Commit 前先看 `git status`，確認沒有 `node_modules/`、`dist/`、`screenshots/`、`.env`。
- 較大的改版建議先開分支（例如 `git checkout -b update/xxx`），確認沒問題再合併到 main。

### Cloudflare Pages 設定
| 設定 | 值 |
|---|---|
| Framework preset | None |
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| 環境變數 | `NODE_VERSION=22`；正式網域確定後加 `SITE_URL=https://正式網域` |

### SITE_URL
- 未設定：不輸出 canonical、og:url、og:image、Schema url、sitemap.xml（避免錯誤網址）。
- 已設定：`build.py` 自動產生上述全部內容，並在 robots.txt 加入 Sitemap。
- 本機測試：`SITE_URL=https://parking.example.com npm run build`（Windows PowerShell：`$env:SITE_URL="https://parking.example.com"; npm run build`）。

---

## 9. 目前待辦（TODO）

- [ ] 在 Cloudflare Pages 連結 GitHub repo 並完成第一次部署
- [ ] 綁定正式網域，設定 `SITE_URL` 後重新部署
- [ ] Google Ads 到達網頁與顯示網址改為正式網域，重新送審
- [ ] 確認電話、經緯度、營業時間後，加入 JSON-LD 與頁面
- [ ] 景點圖片換成實拍照片
- [ ] 與現場公告核對月租與 ATM 付款資訊
- [ ] 上線後確認嵌入的 Google 地圖標記位置正確
- [ ] 如需追蹤廣告成效，加入 GA4 / Google Ads 轉換追蹤（需使用者提供 ID）

完成任何一項後，請在這裡打勾並更新說明。

---

## 10. 回報格式（修改完成後請 AI 依此回報）

1. 這次修改了哪些內容（白話說明）
2. 修改的檔案清單
3. build / lint / test 結果
4. 是否已 commit / push（commit SHA）
5. 需要使用者確認或尚未完成的事項

---

## 11. 使用者請 AI 修改時可用的範本

```
請先讀取專案根目錄的「AI讀取修正檔.md」，讀完後回覆你理解的重點。
這次要修改的是：＿＿＿＿＿＿＿＿
修改完成後依照檔案第 7 節執行檢查，並依第 10 節格式回報；確認後再 push。
```
