# shilaycow

給 Claude Code(桌面 app 加雲端 session)用的開發 harness:

- 一組**可以單獨使用的 skill**,每個對應開發流程中的一個做法。
- 一個把它們組合起來的 **Chief 模式**(`shilaycow-chief`),讓 agent 把一個任務從需求做到一個可以合併的 PR。
- 一條放在 **GitHub 伺服器端的邊界**:無論 agent 做了什麼,`main` 只有 Owner 能改。

想法是:盡可能放寬對 agent 的限制,harness 只負責在 agent 失誤時保護 repo。品質靠檢查結果(獨立驗收、讀程式碼、把行為改壞看測試會不會失敗),不靠規定過程。

不適用於有正式環境、真實使用者或真實資料的專案。

## 怎麼裝

Skill 不需要放進你的專案。它們裝在 Claude 讀取使用者層級 skill 的位置(`~/.claude/skills/`),用同一段指令:

```bash
git clone -q --depth 1 https://github.com/pitaya943/shilaycow.git /tmp/shilaycow-src && mkdir -p ~/.claude/skills && cp -r /tmp/shilaycow-src/plugin/skills/. ~/.claude/skills/
```

### 雲端 session(主要的用法)

1. 在 Claude Code 建立一個雲端環境,把 [`plugin/skills/shilaycow-setup/install-skills.sh`](plugin/skills/shilaycow-setup/install-skills.sh) 的內容貼進它的 **Setup script**。網路要能連到 `github.com`。
2. 之後這個專案的 session 都在這個環境裡開。每個新的 session 一啟動就有全部的 skill;它再開出去的 session(builder、verifier)預設用同一個環境,所以也有。專案自己的 `.claude/skills/`(例如 `try-<app>`)同時照常載入。

每次開 session 拿到的是當時最新的版本。想固定版本,在 script 的 `git clone` 加上 `--branch <tag>`,例如 `--branch v0.3.0`;所有版本列在這個 repo 的 tag。

### 自己的電腦

只在你想在本機的 session 使用這些 skill 時才需要:在終端機執行上面那段指令一次,要更新時再執行一次。每個 skill 的名稱都以 `shilaycow-` 開頭,所以不會覆蓋你原有的個人 skill。這段指令只複製、不刪除:新版本拿掉或改名的 skill,舊的資料夾要自己刪掉。

### 不能用的做法

在專案的 `.claude/settings.json` 宣告 plugin marketplace(`extraKnownMarketplaces`、`enabledPlugins`):雲端 session 不會載入,也不會顯示任何錯誤。這是 Claude Code 文件明載的行為。

在自己的電腦用 `/plugin install` 安裝:只有本機的 session 能用,雲端的容器裡沒有。要小心的是,桌面 app 的選單仍然會在雲端 session 裡顯示它(名稱帶冒號,例如 `shilaycow:chief`),但選了會找不到。雲端裡真正能用的是 setup script 裝的那一套,名稱是連字號的(`shilaycow-chief`)。兩種都裝過的話,把本機的 plugin 移除比較不會選錯。

另一個可行但不建議的做法是把 `plugin/skills/` 複製進專案的 `.claude/skills/` 並 commit:能用,但每個專案各有一份複本,更新後要手動同步。

## 開始一個專案

**只用幾個 skill(Level 1):** 裝好之後直接叫用,例如 `shilaycow-sharpen`、`shilaycow-how`、`shilaycow-why`、`shilaycow-prove`、`shilaycow-principles`。不需要其他設定。

**讓 agent 自己完成整個任務(Level 2 到 4):** 全部可以在瀏覽器與 Claude Code 桌面 app 裡做完,不需要終端機。

1. 準備一個 bot 的 GitHub 帳號,把 claude.ai 的 GitHub 連線接到它,並在你的 repo 安裝 Claude GitHub App。之後的 session 都以 bot 的身分工作;不要在 session 進行中切換連線。
2. 在裝好 skill 的雲端環境,對你的 repo 開一個 session,叫用 `shilaycow-setup`。它會帶你在 GitHub 網頁做兩件只有你能做的事(邀請 bot 為 Write 的 collaborator、匯入保護 `main` 的 ruleset),其餘由它完成:寫設定檔、開一個設定的 PR、檢查規則是否生效。
3. 合併那個設定的 PR。
4. 開一個 session 叫用 `shilaycow-chief`,說明任務。它會先複述並寫任務簡述;你核准並說開始之後,它才進入無人值守的部分。
5. 讀最終的 PR、照「怎麼試」試用、合併。合併後發現不對的地方,在追蹤 issue 留一則留言。

那兩件事一定要你親手做,因為 agent 的帳號不能有改 repo 設定的權限:這正是保護 `main` 的那條邊界。

如果你的電腦有 `gh` 而且用你自己的帳號登入,也可以在本機的 session 叫用 `shilaycow-setup`,它會把那兩件事一起做完。

## 十八個 skill

| 階段 | Skill | 一句話 |
|---|---|---|
| 前期 | `shilaycow-sharpen` | 先複述,再把目標寫成 Owner 核准的任務簡述 |
| 前期 | `shilaycow-how` | 說明某個部分現在怎麼運作 |
| 前期 | `shilaycow-why` | 從紀錄回答為什麼是現在這樣 |
| 全程 | `shilaycow-spec` | 維持 `docs/spec/`:依領域描述整個系統現在的行為 |
| 中期 | `shilaycow-design` | 從情境倒推出系統的形狀 |
| 中期 | `shilaycow-plan` | 切成 ticket,標出依賴與可以平行的 |
| 中期 | `shilaycow-prove` | 決定每個行為怎麼被證明;沒有不會失敗的測試 |
| 後期 | `shilaycow-verify` | 沒參與建置的 session 做六項檢查,判 PASS 或 FAIL |
| 後期 | `shilaycow-try-it` | 為專案產生「怎麼啟動並操作成品」的專屬 skill |
| 後期 | `shilaycow-blast-radius` | 找出變更在別處會弄壞什麼,並實際執行來證明 |
| 後期 | `shilaycow-trail` | 每個決定留一列 |
| 後期 | `shilaycow-report` | 寫給決定要不要合併的人看的報告 |
| 循環結尾 | `shilaycow-retro` | 找出這次踩到、而且會再踩的坑 |
| 循環結尾 | `shilaycow-correct` | 同一類錯誤發生兩次時,改 repo 讓它做不出來 |
| 組合 | `shilaycow-chief` | Chief 模式:六條邊界,其餘由 agent 判斷 |
| 設定 | `shilaycow-setup` | 每個 repo 做一次:bot、ruleset、設定檔 |
| 設定 | `shilaycow-status` | 唯讀:任務在哪、在等誰、下一步 |
| 全程 | `shilaycow-principles` | 七條判斷標準;是知識,不是規定 |

每個 skill 的完整說明在 `plugin/skills/<name>/SKILL.md`。

## 想法的來源

所有內容都是重新寫的,沒有複製其他專案的文字。部分想法來自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)(MIT)與 [Matt Pocock 的 skills](https://github.com/mattpocock/skills)(MIT)。

## 授權

MIT,見 [LICENSE](LICENSE)。
