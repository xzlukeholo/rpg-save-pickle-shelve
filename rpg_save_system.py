import os
import pickle
import time
import sys
import random
os.system('color')  # 啟動 Windows 顏色支援

# 定義顏色與樣式變數
BOLD = '\033[1m'      # 加粗
GREEN = '\033[92m'     # 綠色 (適合 "Add" 或 "Success")
YELLOW = '\033[93m'    # 黃色 (適合 "Menu" 或 "Warning")
RED = '\033[91m'       # 紅色 (適合 "Delete" 或 "Exit")
CYAN = '\033[96m'      # 青色 (適合選單標題)
RESET = '\033[0m'      # 重置 (一定要加，不然之後的字都會變色)


# 顯示選單
def show_menu():
    print()
    print(f"{BOLD}{GREEN}=== RPG System ===")
    print(f"1. 顯示角色狀態")
    print(f"2. 戰鬥")
    print(f"3. 使用藥水")
    print(f"4. pickle 儲存完整存檔")
    print(f"5. pickle 讀取完整存檔")
    print(f"6. shelve 儲存到存檔槽")
    print(f"7. shelve 從存檔槽讀取")
    print(f"8. 顯示所有 shelve 存檔槽")
    print(f"9. 離開遊戲")
    print(f"=== RPG System ==={RESET}")
    print()


# 給玩家選單並取得玩家的選擇
def get_menu_choice():
    show_menu()

    while True:
        try:
            choice = int(input("請輸入您的選擇："))
            if 10 > choice > 0:
                return choice
            else:
                print(f"{BOLD}{YELLOW}請輸入1~9之中的數字喔!{RESET}")
        except ValueError:
            print(f"{BOLD}{YELLOW}輸入錯誤，請重新輸入。{RESET}")


# 顯示角色狀態
def show_status(player):
    print()
    print(f"{BOLD}{YELLOW}=== 角色狀態 ===")
    print(f"名字:{player['name']}")
    print(f"等級:{player['level']}")
    print(f"經驗值:{player['exp']}")
    print(f"HP:{player['hp']} / {player['max_hp']}")
    print(f"攻擊力:{player['attack']}")
    print(f"金幣:{player['gold']}{RESET}")
    print()
    print("=== 道具 ===")
    items = player['items']
    for item in items:
        print(item)
    print()
    print("=== 任務 ===")
    quests = player['quests']
    for key in quests:
        quest = quests[key]
        completed = quest['completed']
        if completed:
            print(
                f"{quest['name']}:討伐{quest['target']},已完成")
        else:
            print(
                f"{quest['name']}:討伐{quest['target']}  {quest['current']} / {quest['required']},未完成")


# 顯示可選戰鬥地點
def show_destination(destinations):
    loading_steps = ["準備冒險", "確認地圖", "前往傳送點"]
    print("\n" + "─" * 40)
    for i in loading_steps:
        for j in range(5):
            sys.stdout.write(f"\r{GREEN}{i}{'.' * j:<4}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    time.sleep(0.2)
    # 準備完畢提示
    print(f"\r{GREEN}✔ 傳送準備完畢！{RESET}\n")
    time.sleep(0.3)
    print(f"{BOLD}{GREEN}╔══════════════════════════════╗{RESET}")
    print(f"{BOLD}{GREEN}║   請選擇欲前往的戰鬥地點     ║{RESET}")
    print(f"{BOLD}{GREEN}╚══════════════════════════════╝{RESET}")
    time.sleep(0.4)
    for index, destination in enumerate(destinations, start=1):
        print(f"{BOLD}{GREEN}地點{index}:{destination}{RESET}")


# 讓玩家選擇戰鬥地點
def select_destination(destinations):
    show_destination(destinations)
    num_destination = len(destinations)
    while True:
        try:
            user_select = int(input(f"請選擇前往狩獵的地點(請輸入數字1~{num_destination}):"))
            if num_destination >= user_select > 0:
                return user_select
            else:
                print("請輸入範圍內的數字喔")
        except ValueError:
            print("請輸入地點的數字喔!")


# 顯示戰鬥選單並取得玩家的戰鬥選擇
def battle_command(player):
    command_list = ["攻擊", "使用藥水", "大招", "逃跑"]
    print(f"可選行動(請輸入數字):")
    for i, command in enumerate(command_list, start=1):
        print(f"{i}.{command} ", end="")
    while True:
        try:
            player_action = int(input(
                f"\n{BOLD}{YELLOW}{player['name']}{RESET}要怎麼做?"))
            if 0 < player_action <= 4:
                return player_action
            else:
                print(f"{BOLD}{RED}請輸入範圍內的數字喔{RESET}")
        except ValueError:
            print(f"{BOLD}{RED}請輸入整數數字喔!{RESET}")


# 戰鬥流程控制
def battle(player, monsters, destinations):
    monster_select = select_destination(destinations) - 1
    enemy = monsters[monster_select]
    print(f"{BOLD}{RED}{enemy['display_name']}{RESET}出現了!")

    # 怪物數值
    enemy_hp = enemy['hp']
    enemy_at = enemy['attack']

    while enemy_hp > 0:
        # 顯示敵人狀態
        print("\n" + "─" * 40)
        print(f"敵人:{BOLD}{RED}{enemy['display_name']}{RESET} 血量:{enemy_hp}")
        print("─" * 40)
        time.sleep(0.2)

        player_action = battle_command(player)

        # 基本攻擊
        if player_action == 1:
            print()
            print(
                f"{BOLD}{YELLOW}{player['name']}{RESET}對{BOLD}{RED}{enemy['display_name']}{RESET}發起了攻擊!")
            damage = attack(player, enemy)
            time.sleep(0.4)
            print(
                f"對{BOLD}{RED}{enemy['display_name']}{RESET}造成了{damage}點的傷害!")
            enemy_hp = enemy_hp - damage
            print()
            time.sleep(0.6)

        # 使用藥水
        elif player_action == 2:
            print(f"{BOLD}{YELLOW}{player['name']}{RESET}準備使用藥水!")
            continue

        # 使用大招流程
        elif player_action == 3:
            print(f"{BOLD}{YELLOW}{player['name']}{RESET}開始詠唱,準備使用終結技!")
            continue

        # 逃跑流程
        elif player_action == 4:
            print(f"{BOLD}{YELLOW}{player['name']}{RESET}選擇逃跑!")
            time.sleep(0.2)
            player_flee = player_run(player, enemy)
            print("逃跑中")
            time.sleep(1.5)
            if player_flee:
                print(
                    f"{BOLD}{YELLOW}{player['name']}{RESET}成功逃離{BOLD}{RED}{enemy['display_name']}{RESET}了!")
                return
            else:
                print("逃跑失敗")
                continue
    print(f"怪物被打倒,戰鬥結束!")
    print(f"獲得經驗值:{enemy['exp']}點")
    return enemy['exp']


# 攻擊傷害計算
def attack(player, enemy):
    crit_rate = 0.06 + player['level'] * 0.01
    base_damage = player['attack'] - enemy['defense']

    if base_damage < 0:
        print(f"{BOLD}{YELLOW}{player['name']}{RESET}打出了MISS")
        time.sleep(0.1)
        options = [f"{BOLD}{RED}{enemy['display_name']}{RESET}失望地搖頭：『戰鬥力只有 5 的渣滓。』", f"{BOLD}{RED}{enemy['display_name']}{RESET}懷疑你是不是在幫他做免費的全身按摩", f"{BOLD}{RED}{enemy['display_name']}{RESET}歪著頭看著你，眼神裡充滿了對弱勢族群的關懷",
                   f"{BOLD}{RED}{enemy['display_name']}{RESET}甚至想幫你的課金進度點根菸", f"{BOLD}{RED}{enemy['display_name']}{RESET}表示：『左邊肩膀再大力一點，對對對，就是那裡。』", f"{BOLD}{RED}{enemy['display_name']}{RESET}的系统提示響起：『檢測到刮痧傷害，已自動判定為無效防衛。』", f"{BOLD}{RED}{enemy['display_name']}{RESET}受到 0 點傷害，並順手塞給了你一本《基礎重訓指南》。", f"{BOLD}{RED}{enemy['display_name']}{RESET}毫髮無傷，並遞給你一條士力架：『我阿嬤踢的都比你好』", f"{BOLD}{RED}{enemy['display_name']}{RESET}覺得力道剛剛好，並打賞了你 5 塊小費。"]
        hurt_text = random.choice(options)
        print(hurt_text)
        if hurt_text == f"{BOLD}{RED}{enemy['display_name']}{RESET}覺得力道剛剛好，並打賞了你 5 塊小費。":
            print("你拿到了5元怪物幣")
        time.sleep(1)
        return 0

    # 爆擊判斷,一樣先運氣影響
    if random.random() > 0.9:
        print(
            f"{BOLD}{YELLOW}{player['name']}{RESET}{BOLD}{CYAN}打出了爆擊!{RESET}")
        damage = int(base_damage * 1.6)
        time.sleep(0.8)
        return damage
    elif random.random() < 0.09:
        damage = base_damage
        return damage
    else:
        if random.random() < crit_rate:
            print(
                f"{BOLD}{YELLOW}{player['name']}{RESET}{BOLD}{CYAN}打出了爆擊!{RESET}")
            damage = int(base_damage * 1.6)
            time.sleep(0.8)
            return damage
        else:
            damage = base_damage
            return damage


def use_potion(player):
    pass


# 逃跑控制,回傳是否逃跑成功
def player_run(player, enemy):
    player_hp = int(player['hp'])
    enemy_hp = int(enemy['hp'])
    if player_hp - enemy_hp >= 0:
        print('逃跑成功!')
        return True
    else:
        success_rate = player_hp / enemy_hp

        # 模擬運氣影響逃跑成功失敗 10~15%左右 運氣判斷完才會依據兩邊的狀態去判斷
        if random.random() > 0.85:
            return True
        elif random.random() < 0.1:
            return False
        else:
            if random.random() < success_rate:
                return True
            else:
                return False


def save_pickle(player, monsters, item_data):

    data = {"player": player, "monsters": monsters, "item_data": item_data}

    with open("rpg_save", "wb") as pickle_save:
        pickle.dump(data, pickle_save)
    for i in range(4):
        for j in range(4):
            sys.stdout.write(f"\r存檔中{'.' * j:<6}")
            sys.stdout.flush()
            time.sleep(0.1)
    print()


def load_pickle():
    try:
        with open("rpg_save", "rb") as p_load:
            rpg_save = pickle.load(p_load)
            return rpg_save
    except FileNotFoundError:
        print(f"{BOLD}{RED}您還沒有存檔喔!請先存檔後再來{RESET}")
        return


def main():

    player = {
        "name": "Mia",
        "level": 1,
        "exp": 0,
        "hp": 100,
        "max_hp": 100,
        "attack": 15,
        "gold": 50,
        "items": {
            "potion": 3,
            "iron_sword": 1
        },
        "quests": {
            "slime_hunter": {
                "name": "史萊姆獵人",
                "target": "slime",
                "required": 3,
                "current": 0,
                "completed": False
            }
        }
    }

    monsters = [
        {
            "name": "slime",
            "display_name": "史萊姆",
            "hp": 30,
            "attack": 5,
            "exp": 20,
            "gold": 10,
            "defense": 1
        },
        {
            "name": "goblin",
            "display_name": "哥布林",
            "hp": 50,
            "attack": 8,
            "exp": 35,
            "gold": 18,
            "defense": 4
        },
        {
            "name": "wolf",
            "display_name": "野狼",
            "hp": 680,
            "attack": 44,
            "exp": 1000,
            "gold": 500,
            "defense": 16
        },
        {
            "name": "orange_mushroom",
            "display_name": "菇菇寶貝",
            "hp": 130,
            "attack": 12,
            "exp": 127,
            "gold": 188,
            "defense": 8
        },
        {
            "name": "green_slime",
            "display_name": "綠水靈",
            "hp": 70,
            "attack": 12,
            "exp": 80,
            "gold": 77,
            "defense": 6
        },
        {
            "name": "balrog",
            "display_name": "巴洛古",
            "hp": 9999,
            "attack": 999,
            "exp": 99999,
            "gold": 100000,
            "defense": 100
        }
    ]

    item_data = {
        "potion": {
            "name": "藥水",
            "heal": 30,
            "description": "恢復 30 HP"
        },
        "iron_sword": {
            "name": "鐵劍",
            "attack_bonus": 5,
            "description": "普通的鐵製長劍"
        }
    }

    game_state = {
        "day": 1,
        "location": "初心者村",
        "difficulty": "normal"
    }

    # 戰鬥時選擇的地點
    destinations = ["史萊姆森林", "哥布林山洞", "狼之平原",
                    "菇菇寶貝棲息地", "綠水靈森林", "被詛咒的寺院"]

    while True:
        user_choice = get_menu_choice()

        if user_choice == 1:
            print("讀取資料中")
            time.sleep(1.2)
            print("讀取成功!")
            time.sleep(0.8)
            show_status(player)

        elif user_choice == 2:
            stage_clear_data = battle(player, monsters, destinations)
            if stage_clear_data == None:
                continue
            player['exp'] += stage_clear_data

        elif user_choice == 3:
            use_potion(player)

        elif user_choice == 4:
            save_pickle(player, monsters, item_data)
            print()
            print(f"{BOLD}{GREEN}存檔成功{RESET}")
            time.sleep(1.2)

        elif user_choice == 5:
            rpg_save = load_pickle()

            if not rpg_save:
                continue

            player = rpg_save["player"]
            monsters = rpg_save["monsters"]
            item_data = rpg_save["item_data"]
            print("讀取檔案成功")

        elif user_choice == 9:
            print(f"{BOLD}{YELLOW}{player['name']}{RESET}離開遊戲。")
            print("感謝遊玩")
            break


if __name__ == '__main__':
    main()
