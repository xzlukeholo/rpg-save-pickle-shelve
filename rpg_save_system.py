import os
import pickle
import time
import sys
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
        for j in range(4):
            sys.stdout.write(f"\r{GREEN}{i}{'.' * j:<4}{RESET}")
            sys.stdout.flush()
            time.sleep(0.2)
    time.sleep(0.5)
    # 準備完畢提示
    print(f"\r{GREEN}✔ 傳送準備完畢！{RESET}\n")
    time.sleep(0.5)
    print(f"{BOLD}{GREEN}╔══════════════════════════════╗{RESET}")
    print(f"{BOLD}{GREEN}║   請選擇欲前往的戰鬥地點     ║{RESET}")
    print(f"{BOLD}{GREEN}╚══════════════════════════════╝{RESET}")
    time.sleep(1)
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


def battle_command(player):
    command_list = ["攻擊", "大招", "逃跑"]
    print(f"\n可選行動(請輸入數字):")
    for i, command in enumerate(command_list, start=1):
        print(f"{i}.{command} ", end="")
    player_action = input(
        f"\n{BOLD}{YELLOW}{player['name']}{RESET}要怎麼做?")


def battle(player, monsters, destinations):
    monster_select = select_destination(destinations) - 1
    enemy = monsters[monster_select]
    print(f"{BOLD}{RED}{enemy['display_name']}{RESET}出現了!")
    battle_command(player)


def use_potion(player):
    pass


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
            "gold": 10
        },
        {
            "name": "goblin",
            "display_name": "哥布林",
            "hp": 50,
            "attack": 8,
            "exp": 35,
            "gold": 18
        },
        {
            "name": "wolf",
            "display_name": "野狼",
            "hp": 680,
            "attack": 44,
            "exp": 1000,
            "gold": 500
        },
        {
            "name": "orange_mushroom",
            "display_name": "菇菇寶貝",
            "hp": 130,
            "attack": 12,
            "exp": 127,
            "gold": 188
        },
        {
            "name": "green_slime",
            "display_name": "綠水靈",
            "hp": 70,
            "attack": 12,
            "exp": 80,
            "gold": 77
        },
        {
            "name": "balrog",
            "display_name": "巴洛古",
            "hp": 9999,
            "attack": 999,
            "exp": 99999,
            "gold": 100000
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
            battle(player, monsters, destinations)

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


main()
