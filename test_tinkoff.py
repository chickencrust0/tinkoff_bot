import os

start_path = './tinkoff'
for root, dirs, files in os.walk(start_path):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                if "class CandleInterval" in f.read():
                    relative_path = os.path.join(root, file).replace(".py", "").replace("\\", ".").replace("/", ".")
                    print(f"Попробуйте импорт: from {relative_path[2:]} import Client")