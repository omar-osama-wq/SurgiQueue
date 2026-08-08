from surgery_management import surgery_mangment

hospital = surgery_mangment()

while True:

    print("\n===== Surgery Management =====")

    print("1. Add Surgery")

    print("2. Show Surgeries")

    print("3. Delete Surgery")

    print("4. Complete Surgery")

    print("5. Show Available Rooms")

    print("6. Change Number Of Rooms")

    print("7. Exit")

    choice = input("Choose: ")

    if choice == "1":

        hospital.add_surgery()

    elif choice == "2":

        hospital.show_surgeries()

    elif choice == "3":

        hospital.delete_surgery()

    elif choice == "4":

        hospital.complete_surgery()

    elif choice == "5":

        hospital.free_rooms()

    elif choice == "6":

        hospital.change_rooms()

    elif choice == "7":

        print("Good Bye")

        break

    else:

        print("Invalid Choice")
