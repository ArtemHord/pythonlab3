import os
import argparse
import random
import json
from pathlib import Path



def parse_args():
    parser = argparse.ArgumentParser(
        prog="LAB3",
        description="Skrypt do tworzenia i odczytu danych w złożonej strukturze katalogów",
        epilog="Przykład odpalania: 'nazwa_pliku.py -m styczeń luty -d pn-wt pt -c r w -t'"
    )
    parser.add_argument("-t", "--tworzenie", action="store_true", help="flaga do tworzenia (bez flagi - tryb czytania)")
    parser.add_argument("-c", "--czas", choices=["r", "w"], nargs="+", default=["r"], help="czas dnia do wyboru")
    parser.add_argument("-m", "--miesiac", nargs="+", required=True, help="Miesiąc do wyboru, może być kilka")
    parser.add_argument("-d", "--dni", nargs="+", required=True, help="Dni tygodnia lub zakresy, np. 'pn-wt pt'")
    return parser.parse_args()


def parse_days_range(days_range):
    days_mapping = {
        "pn": "poniedziałek",
        "wt": "wtorek",
        "śr": "środa",
        "cz": "czwartek",
        "pt": "piątek",
        "sb": "sobota",
        "nd": "niedziela"
    }
    if "-" in days_range:
        start, end = days_range.split('-')
        start_index = list(days_mapping.keys()).index(start)
        end_index = list(days_mapping.keys()).index(end)
        return list(days_mapping.values())[start_index:end_index + 1]
    else:
        return [days_mapping[days_range]]


def parse_time_args(czas, count):
    time_mapping = {"r": "rano", "w": "wieczór"}
    times = [time_mapping.get(c, "rano") for c in czas]

    while len(times) < count:
        times.append("rano")

    return times[:count]



def create_directories_and_files(months, days_args, times):
    base_path = Path("Data_Files")
    base_path.mkdir(exist_ok=True)

    models = ["A", "B", "C"]
    time_index = 0

    for month, days_range in zip(months, days_args):

        days = parse_days_range(days_range)

        for day in days:

            if time_index < len(times):
                time = times[time_index]
                time_index += 1
            else:
                time = "rano"


            directory_path = base_path / month / day / time
            directory_path.mkdir(parents=True, exist_ok=True)


            file_path = directory_path / "data.json"
            data = {
                "Model": random.choice(models),
                "Wynik": random.randint(0, 1000),
                "Czas": f"{random.randint(0, 1000)}s"
            }
            with open(file_path, mode="w") as json_file:
                json.dump(data, json_file, indent=4)

    print("Pliki JSON zostały utworzone.")



def calculate_total_time(base_path):
    total_time = 0

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = Path(root) / file

            if file_path.suffix == ".json":
                with open(file_path, mode="r") as json_file:
                    data = json.load(json_file)
                    time_value = int(data["Czas"].rstrip("s"))
                    total_time += time_value

    print(f"Suma czasu dla wszystkich modeli: {total_time}s")
    return total_time



def main():
    args = parse_args()


    times = parse_time_args(args.czas, sum(len(parse_days_range(d)) for d in args.dni))

    if args.tworzenie:
        create_directories_and_files(args.miesiac, args.dni, times)
    else:
        calculate_total_time("Data_Files")


if __name__ == "__main__":
    main()
