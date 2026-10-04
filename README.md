# 淡水崁頂五路停車場網站

**網站用途**：淡水海岸旅遊 × 停車資訊 Landing Page（Google Ads 正式到達網頁）

純靜態網站：HTML + CSS，無前端框架，頁面不需要 JavaScript。

## 主要功能

- 停車費率（平日 $10/時、假日 $20/時、每日最高 $80、月租 $1,000、前 10 分鐘免費）
- Google Maps 導航（Hero、地圖區、手機底部 Sticky CTA）
- 淡水夕陽主題區
- 金色水岸／觀海長堤
- 自行車／YouBike
- 周邊景點
- FAQ（含 FAQPage 結構化資料）
- Mobile First（375–1440px 皆經自動測試）
- Local SEO（meta、Open Graph、ParkingFacility JSON-LD）

## 專案結構

```
src/index.html        唯一頁面（內嵌 CSS 與 JSON-LD）
src/assets/img/       WebP / AVIF 圖片（map-original.png 為原始素材，不會輸出）
build.py              src/ → dist/，處理 SITE_URL、robots.txt、sitemap.xml、_headers
tests/check_build.py  SITE_URL 建置測試
tests/check_site.py   Playwright 網站檢查（6 種寬度、Sticky CTA、費率、SEO、連結、console、axe）
```

## Local Development

需求：Node.js 20+（建議 22，見 `.nvmrc`）、Python 3（只用標準函式庫）。

```
npm install
npm run build
npm run serve        # http://localhost:8080
```

## Testing

```
npm run lint
npm test             # 需要 Python Playwright 與 Chromium：pip install playwright && playwright install chromium
```

## Build output

`dist/`

## Deployment

**Cloudflare Pages**（連結此 GitHub repo，自動 build / deploy）

| 設定 | 值 |
|---|---|
| Framework preset | None |
| Production branch | `main` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| 環境變數 `NODE_VERSION` | `22`（`.nvmrc` 亦已指定） |
| 環境變數 `SITE_URL` | 正式網址確定後填入，例如 `https://parking.example.com` |

### SITE_URL

正式網址目前尚未決定。

- 未設定 `SITE_URL`：不輸出 canonical、og:url、og:image、Schema url、sitemap.xml（避免錯誤網址）。
- 設定後（`SITE_URL=https://parking.example.com npm run build`）：自動產生以上全部，並在 robots.txt 加入 Sitemap。

設定好 `SITE_URL` 後，需在 Cloudflare Pages 重新部署一次。

> 實際停車費率、付款方式及相關規定，以現場最新公告為準。
