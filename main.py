from datetime import datetime


def ParkingTime(vehicle, now):
    parked_time = now - datetime.strptime(vehicle[1], "%H:%M")
    total_minutes = parked_time.seconds // 60
    hours_parked = parked_time.seconds // 3600
    minutes_parked = (parked_time.seconds % 3600) // 60
    if minutes_parked < 10:
        minutes_parked = f"0{minutes_parked}"

    return hours_parked, minutes_parked, total_minutes


def SearchByPlate(parking_spaces):
    while True:
        try:
            desired_plate = input("Vehicle plate: ")
            for i in range(len(parking_spaces)):
                if len(parking_spaces[i]) > 0 and parking_spaces[i][0] == desired_plate:
                    return parking_spaces[i]
            raise ValueError
        except ValueError:
            print("Error: Plate not found")


def SearchBySpace(parking_spaces):
    for i in range(len(parking_spaces)):
        try:
            space = int(input("Space number: "))
            if space <= 0 or space > len(parking_spaces) or len(parking_spaces[space - 1]) == 0:
                raise IndexError
            else:
                vehicle = parking_spaces[space - 1]
                return vehicle
        except IndexError:
            print("Error: Invalid space number")


def CheckIn(parking_spaces, now):
    while True:
        try:
            space_number = int(input("Space number: "))
            space_number -= 1
            if (space_number < 0) or (space_number >= len(parking_spaces)):
                raise IndexError
            else:
                break
        except ValueError:
            print("Error: You must enter an integer")
        except IndexError:
            print("Error: Invalid space number")

    plate = input("Vehicle plate: ")
    current_time = now.strftime("%H:%M")
    entry_time = input(f"Time [{current_time}]: ")
    if entry_time == "":
        entry_time = current_time
    parking_spaces[space_number] = [plate, entry_time]

    return parking_spaces


def CalculateCharge(vehicle, minutes):
    minutes = int(minutes)
    if minutes <= 15:
        charge = 0
    elif minutes > 15 and minutes < 540:
        charge = round(50 * (minutes // 15 - 1) + (minutes % 15) * 50 / 15)
    else:
        charge = 6500

    return charge


def Status(parking_spaces, now):
    for i in range(len(parking_spaces)):
        if len(parking_spaces[i]) != 0:
            hours_parked, minutes_parked, total_minutes = ParkingTime(
                parking_spaces[i], now)
            print(
                i + 1,
                parking_spaces[i][0],
                parking_spaces[i][1],
                f"({hours_parked}:{minutes_parked})",
                CalculateCharge(parking_spaces[i], total_minutes)
            )
        else:
            print(f"{i+1} ------")


def main():
    while True:
        try:
            available_spaces = int(input("Available spaces: "))
            if available_spaces <= 0:
                raise ValueError
        except ValueError:
            print("Error: You must enter a positive integer greater than zero")
        else:
            break

    parking_spaces = []
    for i in range(available_spaces):
        parking_spaces.append([])

    now = datetime.now()

    while True:
        try:
            option = input("Option [C]heck-in [P]ayment [S]tatus [Q]uit: ")
            if option in ["C", "c", "P", "p", "S", "s", "Q", "q"]:
                option = option.upper()
            else:
                raise ValueError
        except ValueError:
            print("Error: Invalid option")

        if option == "C":
            parking_spaces = CheckIn(parking_spaces, now)

        elif option == "P":
            try:
                search_method = input("Search by [P]late or [S]pace: ")
                if search_method in ["P", "p"]:
                    vehicle = SearchByPlate(parking_spaces)
                elif search_method in ["S", "s"]:
                    vehicle = SearchBySpace(parking_spaces)
                else:
                    raise ValueError
            except ValueError:
                print("Error: Invalid option")

            hours_parked, minutes_parked, total_minutes = ParkingTime(
                vehicle, now)
            charge = CalculateCharge(vehicle, total_minutes)

            print("Consumption details")
            print(f"Plate: {vehicle[0]}")
            print(f"Entry time: {vehicle[1]}")
            print(f"Exit time: {now.strftime('%H:%M')}")
            print(f"Time parked: {hours_parked}:{minutes_parked}")
            print(f"Amount to pay: {charge}")

            parking_spaces[parking_spaces.index(vehicle)] = []

        elif option == "S":
            Status(parking_spaces, now)

        elif option == "Q":
            return 0


if __name__ == "__main__":
    main()
