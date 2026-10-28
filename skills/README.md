# Skills 資料夾

這個資料夾集中存放本專案(婚禮邀請函網頁)所有可重複使用的 **Skill**。
任何 AI(Claude、ChatGPT、Gemini、Cursor、Copilot 等)都可以讀取這些純 Markdown 檔案,作為工作時的共同準則。

## 給 AI 的讀取規則

1. 開始任務前,先瀏覽下方「Skill 索引」,判斷是否有適用的 Skill。
2. 有適用的 Skill → 讀取該資料夾內的 `SKILL.md`,並照步驟執行。
3. 沒有適用的 Skill → 依一般方式處理;若發現值得重複使用的流程,建議使用者新增 Skill。
4. 不要修改 `_template/`;新增 Skill 時複製它。

## 資料夾結構

```
skills/
├── README.md            ← 本檔:索引與規則(所有 AI 先讀這個)
├── _template/
│   └── SKILL.md         ← 新增 Skill 時複製的範本
└── <skill-name>/        ← 每個 Skill 一個資料夾(英文小寫、用 - 連接)
    ├── SKILL.md         ← 必要:Skill 說明與步驟
    └── ...              ← 選用:參考資料、範例、素材
```

## Skill 索引

| Skill | 用途 | 觸發時機 |
|-------|------|----------|
| [wedding-envelope-invitation](./wedding-envelope-invitation/SKILL.md) | 製作手機優先的互動式婚禮邀請函(實體信封開信動畫:封蓋翻開、內藏卡片、鏡頭推進 → 捲動內容、淡入、花瓣),含素材處理、逐格驗證與上線安全注意 | 婚禮邀請函、開信動畫、電子喜帖、信封、火漆印章 |

## 新增 Skill 的方式

1. 複製 `_template/` 並改成新的資料夾名稱,例如 `wedding-envelope-invitation/`。
2. 編輯其中的 `SKILL.md`:填好開頭的 `name` 與 `description`,再寫步驟。
3. 回到本檔,在「Skill 索引」表格新增一列。

## 撰寫原則

- **description 要寫清楚「何時使用」**:AI 靠這一句判斷要不要載入,寫具體比寫籠統有效。
- **一個 Skill 只做一件事**,太大就拆開。
- **用純 Markdown**,不依賴特定 AI 的語法,才能跨工具共用。
- **步驟要可執行**:寫「做什麼、用什麼、做到什麼算完成」,避免空泛原則。
- 較長的參考資料放在同資料夾的獨立檔案,並在 `SKILL.md` 內以相對路徑連結。
