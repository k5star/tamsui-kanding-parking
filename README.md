# 淡水崁頂五路停車場 官方網站

純靜態網站（HTML + CSS，無框架、無 JavaScript 執行期依賴）。

## 結構
- `src/index.html`：唯一頁面（內嵌 CSS、JSON-LD）
- `src/assets/img/`：圖片（WebP / AVIF；`map-original.png` 為原始素材，不會輸出）
- `build.py`：`src/` → `dist/`，處理 SITE_URL、robots.txt、sitemap.xml、Netlify `_headers`
- `tests/check_site.py`：Playwright 自動檢查（6 種寬度、Sticky CTA、費率、SEO、連結、console、axe 無障礙）

## 本機啟動
    npm install          # 只需第一次（htmlhint、axe-core 供檢查用）
    npm run build
    npm run serve        # http://localhost:8080

## 檢查
    npm run lint && npm test

## 部署（Netlify Drop）
1. 取得網址後重新建置：`SITE_URL=https://你的網址 npm run build`（會加入 canonical、og:url、og:image、sitemap）
2. 把 `dist/` 資料夾拖到 https://app.netlify.com/drop
3. Google Ads 最終到達網址與顯示網址都改成這個網域
