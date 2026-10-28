---
name: wedding-envelope-invitation
description: Build a mobile-first interactive wedding invitation web page (photo envelope with wax seal that opens, then scrolling sections, fade-in, petals) delivered as an Artifact. Use for 婚禮邀請函/開信動畫/電子喜帖.
---

# 互動式婚禮邀請函（信封開信 → 捲動內容）

成品：單頁 `index.html`，手機直式為主（`.app` 欄寬 ≤480px），可用 Artifact 發佈，或放 GitHub Pages。回覆使用者用繁體中文。

**專案資料夾分工**：網頁用到的圖片放 `images/`（會公開，HTML 路徑寫 `images/檔名`）；原始素材與 `index.pre-*.html` 備份放 `source/`（`.gitignore` 排除）。`AGENTS.md`、`skills/` 也不公開。改動前先備份、不覆蓋使用者原圖（衍生圖另存新檔）。

## 1. 先確認 / 預設做法
- 使用者通常會提供自己的 AI 生成素材（信封照片、水彩插圖、城堡照）。**優先使用使用者素材**，不要用程式硬畫（程式畫的信封被評為「太 2D」）。沒有素材才用程式替代，且要先說明。
- 新郎新娘名、日期、場地、時程、飯店、餐廳、匯款資訊若沒給，用佔位文字並在回覆中明講「範例，請替換」。不要在頁面外洩漏使用者 email 等資料。
- 語言：預設中文 + EN 切換（字典 + `setLang`），含音樂鈕（WebAudio 環境音，點擊才播）。

## 2. 頁面結構（由上到下）
intro 信封 → hero（城堡照背景 + 紗幔花拱 + 姓名/日期/場地）→ 時間與地點（水彩城堡 + 地圖鈕）→ 倒數計時（目標 ISO 時間）→ 服裝規範（扇子）→ 當日流程（蛋糕 + 時間列）→ 住宿（飯店卡片）→ 探索/餐廳 → 賀禮（穗飾 + 祝福文字；匯款資訊**不放頁面**，改放 QR Code / Line / Google 表單連結）→ RSVP（表單產生可複製文字，無後端）→ footer（封蠟 + 日期）。

## 2.5 目前採用:影片開場(優先使用)
- 開場是單一直式影片 `images/invite-intro.mp4`(720×1280、約 10 秒、靜音、約 1MB)＋封面圖 `images/invite-intro-poster.webp`(影片第一格)。影片內容:蝴蝶結解開 → 兩扇門打開 → 內頁卡片(卡片上的字是影片裡的,不用 HTML 疊字)。
- 結構:`.intro > .rig > <video muted playsinline preload="auto" poster>`,`fit()` 以 cover 置中。點擊 → `vid.play()`(蝴蝶結解開段用 `playbackRate = 1.8` 加快,播過約 6.9 秒——緞帶抽完、門還沒動——用 `requestAnimationFrame` 逐幀檢查後改回 1 倍,不要用 `timeupdate`,頻率太低會切過頭);`ended` 後約 0.9 秒呼叫 `swing()`(intro 淡出、解鎖捲動、加 `revealed`、啟動花瓣、最後 `display:none`)。`error`、`play()` 被拒、逾時(16 秒)都直接 `swing()` 當保險。
- 換影片流程:原檔放 `source/`;用 `ffmpeg -an -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p -movflags +faststart` 轉成 `images/invite-intro.mp4`;用 `ffmpeg -frames:v 1` 抽第一格存成 poster webp;`index.html` 裡影片 `src`、`poster`、預載路徑的 `?v=N` 加 1(檔名不變時瀏覽器會用舊快取,曾出現換了影片仍顯示舊畫面)。
- 檔名只用英文小寫、數字、連字號,不要中文與空格。
- 影片裡的文字(如「誠摯歡迎」)要改就得重產影片;不要用程式逐格修補影片,除非使用者要求。
- 提示字(「輕觸蝴蝶結　開啟喜帖」)放在底部(`bottom` 約 2.4svh),避免蓋到封面圖上印的字。

## 2.6 減少動態效果(iPhone 常開)
- **不要用倍率壓縮計時**(曾寫 `K = reduce ? 0.01 : 1`,導致遮罩瞬間消失)。reduce 用固定秒數:約 0.7 秒顯示頁面、1.4 秒移除開場。
- reduce 時只播影片的蝴蝶結解開段(到約 6.9 秒就 `pause()` 並淡出,不播兩扇門擺開的大位移),保留一點動畫;不要把 `<video>` 設成 `display:none`(會變成空白)。淡出約 0.6 秒。
- reduce 時花瓣不要整個關掉,改成少量(約 8 片)、速度與搖擺約 60%,讓畫面仍有氣氛。
- CSS reduce 區塊:`.fx`、`.art.fx`、`.art.fx.show` 設 `opacity:1; transform:none; scale:1; filter:none; translate:none; transition:none`(`.art.fx` 特異性較高,只寫 `.fx` 蓋不到);關掉循環動畫與 hero 文字上浮。
- 驗證:複製一份測試頁,把 `@media (prefers-reduced-motion:reduce)` 換成 `@media all`、`var reduce = ...` 設成 `true`,驗完刪除。iOS 模擬器與實體機的實際行為要另外實測,不能只靠這個模擬。

## 2.7 預覽與提交的注意事項
- 預覽窗格隱藏時,瀏覽器會暫停影片、不跑 CSS transition:影片用 `ffmpeg` 抽格看(`select='eq(n,…)',tile=`),後半段用 JS 觸發 `swing()`(把 `setTimeout` 換成立即執行)看主頁。
- `python3 -m http.server` 不支援影片 Range 請求:電腦瀏覽器正常,但 iPhone Safari 用區網連線時影片可能播不出來,上線(如 GitHub Pages)才正常。不要因此誤判影片壞了。
- 起伺服器前先用 `lsof -nP -iTCP:<埠> -sTCP:LISTEN` 確認埠沒被別的專案占用(曾載到別的專案頁面),被占用就換埠,不要殺別人的程序。
- 專案可能沒有 `.gitignore`:提交前先建,內容至少 `.DS_Store`、`source/`、`AGENTS.md`、`skills/`,否則原始素材與備份會被提交。提交前用 `git status` 看清楚會進哪些檔。
- 版本備份、素材與使用者原檔放 `source/`,不覆蓋、不刪除。

## 3. （舊版）程式拼接的開信動畫設計邏輯
以下是不用影片、用圖層組出信封開信的作法,目前已被 2.5 的影片開場取代,僅供沒有影片素材時參考。
目標是「實體信封」：封蓋掀開、露出內襯與裡面的卡片、鏡頭直直推進、轉場到主頁。使用者提供過參考錄影，以下是定案做法。

**rig 座標系**：固定尺寸容器（例如 1438×2576）、`fit()` 縮放置中。由後往前的圖層：
1. `.lin` 內襯：淡藍紫底（`#becbeb`）+ 天使/字樣浮水印圖（`liner.webp`，從參考錄影裁出）+ 上緣鉸鏈陰影 + 左上柔光。
2. `.ltr` 邀請卡片：**不透明**米白紙、金色雙層細框、`THE WEDDING OF / L&M / 誠摯邀請 / 日期`，四周大面積柔影。卡片底部被口袋 V 形壓住，才像「插在口袋裡」。
3. `.sh2` 口袋陰影：與口袋同形的深色塊 + `filter:blur(40px)`（模糊要放在外層、clip-path 放內層 `<i>`，否則陰影被裁掉）。
4. `.base` 信封前片（口袋）：`clip-path:path(evenodd,…)` 挖出**乾淨的 V 形**開口（`M0 0H1438V2576H0Z M0 0H1438V606L678 1360L0 509Z`）。
5. `.ve` V 形邊緣高光：SVG 細白線，開啟後才淡入，沿 V 邊往口袋內偏 2px。
6. `.fl` 封蓋（只含 V 形，用「已移除封蠟」的圖）。
7. `.sl` 封蠟獨立圖層：外層 `.sl` 做翻轉與 `drop-shadow`，內層 `i` 放透明封蠟圖並做 `seal-breathe`（用 `scale` 屬性，避免與 transform 衝突；轉換原點不同所以要分兩層）。

**時間軸（慢、順）**：
- 0–2.4s 封蓋以頂邊為軸「往前」翻：`transform:perspective(7000px) rotateX(0→96deg)`，`transform-origin:719px 0`，`backface-visibility:hidden`（弱透視讓封蠟略放大，符合「往前開」；強透視或負角度會變成往後倒）。封蠟 `drop-shadow` 從貼身小影變成 `0 60px 50px` 大影。
- 1.0s 起卡片從 `translate:0 130px` 升起（1.8s）。
- 2.6s 起鏡頭「正對中心直直推進」3.2s：`.base`/`.sh2`/`.ve` `scale:3.6` 並 `translate:0 2600px`（口袋滑出畫面）、`.lin` `scale:2`、`.ltr` `scale:2.1`；三層速度不同產生視差深度。用獨立屬性 `scale`/`translate`，transform-origin 設在畫面中心 `719px 1288px`。
- 5.1s 起 intro 淡出（0.9s）→ 5.0s 解除 scroll lock、加 `revealed`、啟動花瓣 → 6.2s `display:none`。
- 不要用半透明奶油色整層淡入蓋住信封（會有「透明」感）；改由不透明卡片填滿畫面再淡出。
- `prefers-reduced-motion`：關掉呼吸、推進，只做淡出。

**其他**：`.hint` 擴散白環（封蠟位置、`fit()` 設 CSS 變數）、底部「輕觸封蠟」提示、鍵盤 Enter/Space 與 `role=button`、`window.scrollTo(0,0)` 後才解鎖捲動。

## 4. 版面與可讀性規則（使用者兩度回報「字看不清楚」）
- **文字永遠在圖片上層**：插圖用獨立 class（如 `.art`）。**不要重用 intro 的 `.pic`（absolute; inset:0）**，這個 class 衝突曾讓插圖蓋住所有文字。
- hero 文字壓在紗幔/天空上時：深墨色（#3f3547 / 姓名 #46698f）、字重 500–600、字級 ≥13px、多層白色 text-shadow 光暈；倒數數字 ≥34px 並加底色光暈、標籤 ≥12px 深色；不要用 9–10px 淺灰小字。正文 ≥15px，顏色 #4d3340~#5a3f4b。
- 倒數 `.cd` 要收窄（約 min(66%,260px)）避免被兩側玫瑰遮住。
- 手機寬度驗證：390×844 截圖；不要有橫向捲動；全域 `img{height:auto}`，避免 width/height 屬性造成變形。

## 5. 圖片處理規則
- 白底水彩圖**直接轉成透明 WebP**（白色轉 alpha：先做色階白點 ≈240，alpha=(255−min(r,g,b))/255，再反推顏色），**不要依賴 `mix-blend-mode:multiply`** —— 一旦元素有 transform/opacity/will-change（淡入動畫）就會建立堆疊環境使 multiply 失效而露出白框。
- 封蠟/蕾絲摳圖可用 rembg（isnet-general-use，需 pip 安裝）；絲帶/蕾絲可用飽和度遮罩。弧形花拱用 color-to-alpha。
- 花拱頂部用高度限制的遮罩容器（`.archw`，底部漸層淡出），hero 上方留約 230px 漸層帶，避免花拱蓋到城堡與文字。穗飾放在賀禮區頂部，區塊 padding-top 要夠（約 268px）避免蓋到標題。
- **信封圖衍生處理（用 PIL + numpy，不需 cv2）**：
  - 白底印章（如 `wax-seal-lm-white.png`，常常副檔名是 png 但實為 JPEG、無透明）：從四邊 flood-fill `min(r,g,b)≥244` 得背景遮罩，再往內縮約 12px（MinFilter）並柔化 1.6px，輸出透明 WebP；在藍底預覽確認沒有白邊。
  - 移除信封照片上的舊封蠟：以封蠟圓（中心約 726,1298、半徑約 258）為遮罩，用周圍紙面的**平面擬合**（最小平方、迭代剔除蕾絲/壓紋離群值）填色，加上與原圖同強度的細顆粒（std≈6–8，輕微模糊），融合範圍放寬到半徑 +36 起 90px 漸層，避免出現圓盤邊緣。口袋圖與封蓋圖要分別補（取樣帶不同：口袋取下半、封蓋取上半）。另存 `env2_pocket.webp`、`env2_flap.webp`，**不覆蓋原圖**。
  - 從錄影擷取素材用 `ffmpeg -ss <秒> -frames:v 1` 抽幀再裁切；注意版權由使用者確認。
- 圖片換新時：換檔名發佈新檔（舊檔若被其他版本引用，不要用 null 刪除，會被發佈機制擋下），同時更新 `width/height` 屬性。
- 沙盒擋 Google Fonts，截圖會用後備字型；字型僅作 `<link>`（Cormorant Garamond、Noto Serif TC），請提醒真機字型可能略有差異。

## 6. 動畫規格
- **捲動淡入（雙向）**：給 `.sec .w > *`、卡片、時程列、footer 子元素加 `.fx`（opacity 0、translateY 22px、1.1s）；用 IntersectionObserver 對進出可視區 `toggle('show', isIntersecting)`（上滑下滑都淡入淡出，`threshold .15`、`rootMargin -4% 0 -8% 0`），同層元素以 index 做 0.12s 階梯延遲（最多 5 級）。JS 才加 `.fx`，無 IO 時內容保持可見。
- **圖片動畫**：用獨立 CSS 屬性（`scale`、`rotate`、`translate`）避免與 transform 的淡入衝突：hero 照片慢速 Ken Burns（26s alternate scale 1→1.09，hero 需 overflow:hidden）；紗幔花拱微搖（rotate ±0.5°）；水彩插圖進場由模糊/縮小→清晰，之後 `floaty` 上下漂浮；穗飾從頂端擺動 ±2.2°；頁尾封蠟光暈呼吸。
- **花瓣特效**：開信後啟動的全螢幕 `<canvas id=petals>`（fixed、`pointer-events:none`、z-index 40，低於音樂鈕 60）；手機約 22 片（桌機 34）；貝茲曲線花瓣、粉/白漸層、各自的下落速度、左右搖擺（sin）、旋轉、`cos` 翻面縮放；出界後重生；`dt` 上限 0.05s；DPR 上限 2；reduced-motion 不啟動。
- 金色閃爍 sparkle 要避開文字（曾疊字）。

## 7. 驗證流程（每次改完必做）
1. 預覽用本機靜態伺服器（`python3 -m http.server 8765 --bind 127.0.0.1`）開 `http://127.0.0.1:8765/index.html`；桌面 App 的瀏覽器窗格會把 `file://` 當靜態快照，相對路徑圖片會載入失敗。手機寬度用 viewport 390×844（或 mobile 預設）。有 playwright 時也可用 `/opt/npm-tools/node_modules/playwright`，並注入 `html{scroll-behavior:auto!important}`。
2. **逐格檢查動畫**：先 `window.setTimeout=()=>0`（避免 JS 計時器隱藏 intro），`intro.click()` 後 `document.getAnimations({subtree:true}).filter(a=>a.transitionProperty)` 全部 `pause()` 並設 `currentTime`（例如 500/1000/2500/4000ms）；截圖前 `wait 1s`，截兩次（第一次常是上一格的殘影）。可用 `getComputedStyle(el).transform` 確認真的到位。
3. 截圖：開信前、各時間點、hero、各區塊（滑到後等 ~2s 讓淡入完成）。看文字是否被遮、白框、橫向捲動、console 錯誤。
4. 回覆使用者：一句話說明改了什麼，**誠實說明只驗證了靜態截圖、動畫流暢度與真機字型未驗證**，請他在手機實測；不貼 URL（卡片已有）。Artifact 預設私人，要分享需使用者自己用 Share。

## 8. 常見坑速查
- `.w` 不要設 z-index（會建立堆疊環境）；只用 `position:relative`。
- CSS `display` 會蓋過 `hidden` 屬性（three.js 的 no-WebGL 提示曾因此誤顯示）→ 補 `[hidden]{display:none}`。
- 全域 `img{height:auto}`；遮罩 `-webkit-mask-image` 與 `mask-image` 都要寫。
- 開信後 `intro` 要 `pointer-events:none` 並最終 `display:none`，否則擋住捲動與點擊。
- **整層半透明淡入會讓信封顯得「透明」**：用不透明卡片填滿畫面再淡出。
- **封蓋 clip-path 不要多帶封蠟周圍的紙面/蕾絲**：翻開時那一圈會像多出的圖層。封蓋只含 V 形，封蠟另成圖層。
- `filter`（blur/drop-shadow）與 `clip-path` 放同一元素時，濾鏡效果會被 clip 裁掉；濾鏡放外層、clip 放內層。
- 呼吸/翻轉共用同一元素時 transform-origin 會衝突；拆成外層（翻轉）與內層（`scale` 呼吸）。
- 不要對縮放動畫的圖層加 `will-change:transform`（會以初始解析度柵格化，放大時變模糊）。
- 賀禮匯款資訊不要放在公開頁面；上 GitHub Pages 前加 `<meta name="robots" content="noindex">`、檢查沒有金鑰/個資。
- 使用者要求通常是漸進微調（拉遠、放大、改圖、補動畫）：每次只改被指的部分，保留備份（`index.pre-*.html`），改完立即截圖驗證再發佈。
