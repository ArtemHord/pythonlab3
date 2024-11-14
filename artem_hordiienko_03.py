import os
import argparse
import random
import csv
import json
from pathlib import Path



def argparse():
    parser = argparse.ArgumentParser(prog="LAB3",description="Skrypt do tworzenia i odczytu danych w złożonej strukturze katalogów",epilog="Przykład odpalania:'nazwa_pliku.py -m styczeń luty -d pw-wt  pt -c r,w'")
    parser.add_argument("-t", "--tworzenie", action="store_true", help="flaga do tworzenia(bez flagi tryp czytania)")
    parser.add_argument("-c", "--czas", choices=["r", "w"], default="r",help = "czas dnia do wyboru")
    parser.add_argument("-m","--miesiac",nargs = "+", required=True, help="Miesiąc do wyboru, może być kilkanaście ")
    parser.add_argument("-d","--dni",nargs = "+", required=True, help="Dni tygodnia do wyboru")

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
    start, end = days_range.split('-')
    start_index = list(days_mapping.keys()).index(start)
    end_index = list(days_mapping.keys()).index(end)
    return list(days_mapping.values())[start_index:end_index + 1]

def parse_time_args(czas):


def create_directories_and_files(months, days, time, file_format):
    base_path = Path("Data_Files")
    base_path.mkdir(exist_ok=True)

    for month in months:
        for day in days:
            directory_path = base_path / month / day / time
            directory_path.mkdir(parents=True, exist_ok=True)

            if file_format == "csv":
                file_path = directory_path / "data.csv"
                with open(file_path, mode="w", newline="") as csv_file:
                    writer = csv.writer(csv_file, delimiter=";")
                    writer.writerow(["Model", "Wynik", "Czas"])
                    writer.writerow(["A", random.randint(0, 1000), f"{random.randint(0, 1000)}s"])
            elif file_format == "json":
                file_path = directory_path / "data.json"
                data = {
                    "Model": "A",
                    "Wynik": random.randint(0, 1000),
                    "Czas": f"{random.randint(0, 1000)}s"
                }
                with open(file_path, mode="w") as json_file:
                    json.dump(data, json_file, indent=4)

    print(f"pliki są stworzone w formacie {file_format}.")


def calculate_total_time(base_path, file_format):
    total_time = 0

    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = Path(root) / file

            if file_format == "csv" and file_path.suffix == ".csv":
                with open(file_path, mode="r") as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=";")
                    for row in reader:
                        if row["Model"] == "A":
                            time_value = int(row["Czas"].rstrip("s"))
                            total_time += time_value
            elif file_format == "json" and file_path.suffix == ".json":
                with open(file_path, mode="r") as json_file:
                    data = json.load(json_file)
                    if data["Model"] == "A":
                        time_value = int(data["Czas"].rstrip("s"))
                        total_time += time_value

    print(f"Suma dla modeli A: {total_time}s")
    return total_time





def main():
    args = argparse()


    days = parse_days_range(args.dni)
    time = parse_time_args(args.czas)


if __name__ == "__main__":
    main()