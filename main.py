def readPatientsFromFile(fileName):
    """
    Reads patient data from a plaintext file.

    fileName: The name of the file to read patient data from.
    Returns a dictionary of patient IDs, where each patient has a list of visits.
    The dictionary has the following structure:
    {
        patientId (int): [
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            ...
        ],
        patientId (int): [
            [date (str), temperature (float), heart rate (int), respiratory rate (int), systolic blood pressure (int), diastolic blood pressure (int), oxygen saturation (int)],
            ...
        ],
        ...
    }
    """
    patients = {}
    #Opens patient file
    try:
        patientFile = open(fileName, "r")
    except FileNotFoundError:
        print(f"The file {fileName} could not be found.")
        exit()

    #Iterates through and splits up all the patient info
    for line in patientFile:
        try:
            line = line.split(",")
            if not len(line) == 8:
                print(f"Invalid number of fields ({len(line)}) in line: {line}")
                continue

            # Assigns all the data variables to the file info, and checks if it's within a credible range
            patientId = int(line[0].strip())
            date = str(line[1].strip())
            temperature = float(line[2].strip())
            heartRate = int(line[3].strip())
            respRate = int(line[4].strip())
            sysBP = int(line[5].strip())
            diaBP = int(line[6].strip())
            oxySat = int(line[7].strip())

            if not 35 < temperature < 42:
                print(f"Invalid temperature value ({temperature}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue
            if not 30 < heartRate < 180:
                print(f"Invalid heart rate value ({heartRate}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue
            if not 5 < respRate < 40:
                print(f"Invalid respiratory rate value ({respRate}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue
            if not 70 < sysBP < 200:
                print(f"Invalid systolic blood pressure value ({sysBP}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue
            if not 40 < diaBP < 120:
                print(f"Invalid diastolic blood pressure value ({diaBP}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue
            if not 70 < oxySat < 100:
                print(f"Invalid oxygen saturation value ({oxySat}) in line: {patientId},{date},{temperature},{heartRate},{respRate},{sysBP},{diaBP},{oxySat}")
                continue

            # Adds the patient to the dictionary
            if patientId in patients:
                patients[patientId].append([date, temperature, heartRate, respRate, sysBP, diaBP, oxySat])
            else:
                patients.update({  patientId:[ [date, temperature, heartRate, respRate, sysBP, diaBP, oxySat] ]  })

        except ValueError:
            print(f"Invalid data type in line: {line}")
        except:
            print("An unexpected error occurred while reading the file.")


    patientFile.close()
    return patients

def displayPatientData(patients, patientId=0):
    """
    Displays patient data for a given patient ID.

    patients: A dictionary of patient dictionaries, where each patient has a list of visits.
    patientId: The ID of the patient to display data for. If 0, data for all patients will be displayed.
    """
    #If no patient ID, loops through the function again with each individual patient ID
    if patientId == 0:
        for patientNum in patients:
            displayPatientData(patients,patientNum)
    # Error if patientID doesnt exist
    elif patientId not in patients:
        print(f"Patient with ID {patientId} not found.")
    #Prints out the information of a singular patient
    else:
        print(f"Patient ID: {patientId}")
        for visit in patients[patientId]:
            print(" Visit Date:", visit[0])
            print(f"  Temperature: " "%.2f" % (visit[1]), "C")
            print(f"  Heart Rate: {visit[2]} bpm")
            print(f"  Respiratory Rate: {visit[3]} bpm")
            print(f"  Systolic Blood Pressure: {visit[4]} mmHg")
            print(f"  Diastolic Blood Pressure: {visit[5]} mmHg")
            print(f"  Oxygen Saturation: {visit[6]} %")

def displayStats(patients, patientId=0):
    """
    Prints the average of each vital sign for all patients or for the specified patient.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    patientId: The ID of the patient to display vital signs for. If 0, vital signs will be displayed for all patients.
    """
    visitCount, temperatureSum, heartRateSum, respiratoryRateSum, sysBPSum, diaBPSum, oxySatSum = 0,0,0,0,0,0,0

    # Error Catching:
    try:
        patientId = int(patientId)
    except:
        print("Error: 'patientID' should be an integer.")
        return
    try:
        patients = dict(patients)
    except:
        print("Error: 'patients' should be a dictionary.")
        return
    if patientId not in patients and not patientId == 0:
        print(f"No data found for patient with ID {patientId}.")
        return

    # Loops through all patient IDs if 0 is input, summing up all the info in the database
    if patientId == 0:
        print("Vital Signs for all Patients:")
        for patientnum in patients:
            for visit in patients[patientnum]:
                visitCount += 1
                temperatureSum += visit[1]
                heartRateSum += visit[2]
                respiratoryRateSum += visit[3]
                sysBPSum += visit[4]
                diaBPSum += visit[5]
                oxySatSum += visit[6]
    #Adds up just the information for a single person
    else:
        print(f"Vital Sign for Patient: {patientId}:")
        for visit in patients[patientId]:
            visitCount += 1
            temperatureSum += visit[1]
            heartRateSum += visit[2]
            respiratoryRateSum += visit[3]
            sysBPSum += visit[4]
            diaBPSum += visit[5]
            oxySatSum += visit[6]

    #Prints averages and does the average calculations within the statements
    print("  Average temperature: ", "%.2f" % (temperatureSum / visitCount), "C")
    print("  Average heart rate: ", "%.2f" % (heartRateSum / visitCount), "bpm")
    print("  Average respiratory rate: ", "%.2f" % (respiratoryRateSum / visitCount), "bpm")
    print("  Average systolic blood pressure:", "%.2f" % (sysBPSum / visitCount), "mmHg")
    print("  Average diastolic blood pressure:", "%.2f" % (diaBPSum / visitCount), "mmHg")
    print("  Average oxygen saturation:", "%.2f" % (oxySatSum / visitCount), "%")

def addPatientData(patients, patientId, date, temp, hr, rr, sbp, dbp, spo2, fileName):
    """
    Adds new patient data to the patient list.

    patients: The dictionary of patient IDs, where each patient has a list of visits, to add data to.
    patientId: The ID of the patient to add data for.
    date: The date of the patient visit in the format 'yyyy-mm-dd'.
    temp: The patient's body temperature.
    hr: The patient's heart rate.
    rr: The patient's respiratory rate.
    sbp: The patient's systolic blood pressure.
    dbp: The patient's diastolic blood pressure.
    spo2: The patient's oxygen saturation level.
    fileName: The name of the file to append new data to.
    """
    #Error checking
    try:
        temperature = float(temp)
        heartRate = int(hr)
        respRate = int(rr)
        sysBP = int(sbp)
        diaBP = int(dbp)
        oxySat = int(spo2)

        # Date Error Checking
        try:
            dateList = date.split("-")
            if not 0 < int(dateList[0]) < 9999 or not 1 <= int(dateList[1]) <= 12 or not 0 < int(dateList[2]) <= 31:
                print("Invalid date. Please enter a valid date.")
                return
        except:
            print("Invalid date format. Please enter date in the format 'yyyy-mm-dd'")

        # Medical Information Error Checking
        if not 35 < temp < 42:
            print("Invalid temperature. Please enter a temperature between 35.0 and 42.0 Celsius")
            return
        if not 30 < heartRate < 180:
            print("Invalid heart rate. Please enter a heart rate between 30 and 180 bpm")
            return
        if not 5 < respRate < 40:
            print("Invalid respiratory rate. Please enter a respiratory rate between 5 and 40 bpm")
            return
        if not 70 < sysBP < 200:
            print("Invalid systolic blood pressure. Please enter a systolic blood pressure between 70 and 200 mmHg")
            return
        if not 40 < diaBP < 120:
            print("Invalid diastolic blood pressure. Please enter a diastolic blood pressure between 40 and 120 mmHg")
            return
        if not 70 < oxySat < 100:
            print("Invalid oxygen saturation. Please enter an oxygen saturation between 70 and 100%")
            return




        # Adding information to the end of the file
        try:
            patientFile = open(fileName, "a")
            patientFile.write(f"\n{patientId},{date},{temp},{hr},{rr},{sbp},{dbp},{spo2}")
            patientFile.close()
        except FileNotFoundError:
            print(f"The file {fileName} could not be found.")
            return

        # Adding information to the patients dictionary
        if patientId in patients:
            patients[patientId].append([date, temperature, heartRate, respRate, sysBP, diaBP, oxySat])
        else:
            patients.update({patientId: [[date, temperature, heartRate, respRate, sysBP, diaBP, oxySat]]})
    except:
        print("An unexpected error occurred while adding new data")
        return

    print(f"Visit saved Patient #{patientId}")

def findVisitsByDate(patients, year=None, month=None):
    """
    Find visits by year, month, or both.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    year: The year to filter by.
    month: The month to filter by.
    return: A list of tuples containing patient ID and visit that match the filter.
    """
    visits = []

    # Error checking for invalid year and month inputs


    if not month == None:
        if not 1 <= month <= 12:
            return visits


    # Iterates through all visits
    for patientNum in patients:
        for visit in patients[patientNum]:
            #iterates through visit^

            #Splits up dates of every visit, and adds the visit to the visits list if it meets the year/month filter
            date = visit[0].split("-")
            if int(date[0]) == year and month == None:
                visits.append(tuple((patientNum,visit)))
            if int(date[0]) == year and int(date[1]) == month:
                visits.append(tuple((patientNum, visit)))


    return visits

def findPatientsWhoNeedFollowUp(patients):
    """
    Find patients who need follow-up visits based on abnormal vital signs.

    patients: A dictionary of patient IDs, where each patient has a list of visits.
    return: A list of patient IDs that need follow-up visits to abnormal health stats.
    """
    followup_patients = []
    # Iterate through all the visits
    for patientNum in patients:
        for visit in patients[patientNum]:
            heartRate = visit[2]
            sysBP = visit[4]
            diaBP = visit[5]
            oxySat = visit[6]
            # If a patient has a value outside the normal, add their ID to the list
            if heartRate > 100 or heartRate < 60 or sysBP > 140 or diaBP > 90 or oxySat < 90:
                followup_patients.append(patientNum)

    return followup_patients

def deleteAllVisitsOfPatient(patients, patientId, filename):
    """
    Delete all visits of a particular patient.

    patients: The dictionary of patient IDs, where each patient has a list of visits, to delete data from.
    patientId: The ID of the patient to delete data for.
    filename: The name of the file to save the updated patient data.
    return: None
    """

    # Checks if there is a deletable patient
    if patientId not in patients:
        print(f"No data found for patient with ID {patientId}")
        return

    # Removes patient from dict 'Patients'
    patients.pop(patientId)

    #opens file, and iterates through new 'Patients' dict, re-writing all the existing patients info
    patientFile = open(filename, "w")

    for patientNum in patients:
        for visit in patients[patientNum]:
            patientFile.write(f"{patientNum},{visit[0]},{visit[1]},{visit[2]},{visit[3]},{visit[4]},{visit[5]},{visit[6]}\n")



    print(f"Data for patient {patientId} has been deleted.")


###########################################################################
###########################################################################
#   The following code is being provided to you. Please don't modify it.  #
#   If this doesn't work for you, use Google Colab,                       #
#   where these libraries are already installed.                          #
###########################################################################
###########################################################################

def main():
    patients = readPatientsFromFile('patients.txt')
    while True:
        print("\n\nWelcome to the Health Information System\n\n")
        print("1. Display all patient data")
        print("2. Display patient data by ID")
        print("3. Add patient data")
        print("4. Display patient statistics")
        print("5. Find visits by year, month, or both")
        print("6. Find patients who need follow-up")
        print("7. Delete all visits of a particular patient")
        print("8. Quit\n")

        choice = input("Enter your choice (1-8): ")
        if choice == '1':
            displayPatientData(patients)
        elif choice == '2':
            patientID = int(input("Enter patient ID: "))
            displayPatientData(patients, patientID)
        elif choice == '3':
            patientID = int(input("Enter patient ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                temp = float(input("Enter temperature (Celsius): "))
                hr = int(input("Enter heart rate (bpm): "))
                rr = int(input("Enter respiratory rate (breaths per minute): "))
                sbp = int(input("Enter systolic blood pressure (mmHg): "))
                dbp = int(input("Enter diastolic blood pressure (mmHg): "))
                spo2 = int(input("Enter oxygen saturation (%): "))
                addPatientData(patients, patientID, date, temp, hr, rr, sbp, dbp, spo2, 'patients.txt')
            except ValueError:
                print("Invalid input. Please enter valid data.")
        elif choice == '4':
            patientID = input("Enter patient ID (or '0' for all patients): ")
            displayStats(patients, patientID)
        elif choice == '5':
            year = input("Enter year (YYYY) (or 0 for all years): ")
            month = input("Enter month (MM) (or 0 for all months): ")
            visits = findVisitsByDate(patients, int(year) if year != '0' else None,
                                      int(month) if month != '0' else None)
            if visits:
                for visit in visits:
                    print("Patient ID:", visit[0])
                    print(" Visit Date:", visit[1][0])
                    print("  Temperature:", "%.2f" % visit[1][1], "C")
                    print("  Heart Rate:", visit[1][2], "bpm")
                    print("  Respiratory Rate:", visit[1][3], "bpm")
                    print("  Systolic Blood Pressure:", visit[1][4], "mmHg")
                    print("  Diastolic Blood Pressure:", visit[1][5], "mmHg")
                    print("  Oxygen Saturation:", visit[1][6], "%")
            else:
                print("No visits found for the specified year/month.")
        elif choice == '6':
            followup_patients = findPatientsWhoNeedFollowUp(patients)
            if followup_patients:
                print("Patients who need follow-up visits:")
                for patientId in followup_patients:
                    print(patientId)
            else:
                print("No patients found who need follow-up visits.")
        elif choice == '7':
            patientID = input("Enter patient ID: ")
            deleteAllVisitsOfPatient(patients, int(patientID), "patients.txt")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()