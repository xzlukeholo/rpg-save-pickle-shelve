# RPG Save System

一個使用 Python 製作的命令列 RPG 存檔系統小專案。

這個專案主要練習 Python 的序列化、反序列化，以及物件持久化存儲。  
玩家可以進行簡單戰鬥、使用藥水、升級，並透過 `pickle` 和 `shelve` 儲存與讀取遊戲狀態。

---

## Features

- 顯示角色狀態
- 簡單戰鬥系統
- 經驗值與升級系統
- HP 與藥水使用
- 任務進度紀錄
- 使用 `pickle` 儲存完整遊戲資料
- 使用 `pickle` 讀取完整遊戲資料
- 使用 `shelve` 製作多存檔槽
- 顯示所有 shelve 存檔槽
- 基本錯誤處理，例如：
  - 找不到 pickle 存檔
  - 找不到 shelve 存檔槽
  - 選單輸入錯誤
  - 藥水不足
  - 滿血時不使用藥水

---

## Project Goal

本專案的目標是練習 Python 中的資料持久化概念。

程式執行時，玩家資料原本只存在記憶體中。  
如果程式關閉，資料就會消失。

透過 `pickle` 和 `shelve`，可以把 Python 物件保存到檔案中，讓程式下次啟動時能重新讀取資料。

---

## What I Practiced

這次專案練習到：

1. 使用 `dict` 和 `list` 設計遊戲資料。
2. 使用巢狀 dictionary 儲存角色、道具、任務資料。
3. 使用 function 拆分程式功能。
4. 使用 `pickle.dump()` 將 Python 物件序列化並存入檔案。
5. 使用 `pickle.load()` 從檔案反序列化並還原 Python 物件。
6. 使用 `shelve.open()` 建立 key-value 型態的存檔系統。
7. 使用 shelve 製作多個存檔槽，例如 `slot1`、`slot2`、`slot3`。
8. 處理檔案不存在、key 不存在等錯誤情況。
9. 練習讓遊戲狀態在程式關閉後仍然可以保存。

---

## Game Data

遊戲資料包含：

- 玩家名稱
- 等級
- 經驗值
- HP / 最大 HP
- 攻擊力
- 金幣
- 道具
- 任務進度
- 遊戲天數
- 目前地點
- 怪物資料

---

## Menu

程式啟動後會顯示選單：

```text
=== RPG Save System ===
1. 顯示角色狀態
2. 戰鬥一次
3. 使用藥水
4. pickle 儲存完整存檔
5. pickle 讀取完整存檔
6. shelve 儲存到存檔槽
7. shelve 從存檔槽讀取
8. 顯示所有 shelve 存檔槽
9. 離開遊戲