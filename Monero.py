# Импорт необходимых модулей
import os  # Модуль для взаимодействия с операционной системой
import subprocess  # Модуль для запуска внешних процессов
import json  # Модуль для работы с JSON-данными

# Получение ввода от пользователя для адреса кошелька Monero
wallet_address = input("Введите ваш адрес кошелька Monero: ")

# Отображение доступных пулов для майнинга для выбора пользователя
print("Пожалуйста, выберите пул из следующих вариантов:")
print("1. pool.minexmr.com:4444")
print("2. xmrpool.eu:9999")
print("3. monerohash.com:5555")
print("4. pool.supportxmr.com:5555")
pool_choice = input("Введите номер пула, на котором вы хотите майнить: ")
power_percent = input("Введите процент майнинговой мощности, которую вы хотите использовать (0-100): ")

# Преобразование power_percent в целое число и обработка неверного ввода
try:
    power_percent = int(power_percent)
except ValueError:
    print("Неверный ввод майнинговой мощности. Пожалуйста, введите целое число от 0 до 100.")
    exit()

# Проверка допустимости введенного значения для майнинговой мощности
if power_percent < 0 or power_percent > 100:
    print("Неверный ввод майнинговой мощности. Пожалуйста, введите целое число от 0 до 100.")
    exit()

# Настройка адреса пула в соответствии с выбором пользователя
if pool_choice == "1":
    pool_address = "pool.minexmr.com:4444"
elif pool_choice == "2":
    pool_address = "xmrpool.eu:9999"
elif pool_choice == "3":
    pool_address = "monerohash.com:5555"
elif pool_choice == "4":
    pool_address = "pool.supportxmr.com:5555"
else:
    print("Неверный ввод для выбора пула. Пожалуйста, введите число от 1 до 4.")
    exit()

# Получение пути к исполняемому файлу XMRig от пользователя
xmrig_path = input("Введите путь к исполняемому файлу XMRig (например, C:/xmrig/xmrig.exe): ")

# Автоматическая настройка XMRig на основе введенных пользователем данных
config_path = os.path.join(os.getcwd(), "config.json")

config = {
    "pools": [
        {
            "url": f"stratum+tcp://{pool_address}",
            "user": f"{wallet_address}",
            "pass": "x"
        }
    ],
    "cpu": {
        "enabled": True,
        "threads": 0,
        "priority": 5
    },
    "opencl": False,
    "cuda": False,
    "donate-level": 0,
    "log-file": "log.txt",
    "print-time": 60,
    "retry-pause": 5,
    "syslog": False,
    "threads": [
        {
            "index": 0,
            "mode": "auto",
            "intensity": power_percent
        }
    ]
}

# Запись настроек в файл конфигурации JSON
with open(config_path, "w") as f:
    f.write(json.dumps(config))

# Формирование команды для запуска XMRig
command = f"{xmrig_path} -c {config_path}"

# Запуск XMRig в новом процессе
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Открытие веб-сайта пула в браузере
pool_website = f"https://{pool_address.split(':')[0]}/"
os.system(f"start {pool_website}")

# Мониторинг вывода из XMRig
while True:
    output = process.stdout.readline().decode("utf-8").strip()
    if output == "":
        break
    print(output)
