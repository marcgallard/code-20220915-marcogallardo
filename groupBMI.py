"""
    Description: The script takes in JSON data representing several people,
    calculates each individual's BMI, and counts how many of them are overweight
    according to set criteria (refer to CONSTANTS comment section for more info)
    and presents it as a displayed table.

    Input: JSON data file, each element representing a person's gender, height
    in cm, and weight in Kg

    Output: Number of overweight people from input according to set criteria, as
    well as number of malformatted data samples from given data
"""

## IMPORTS
import argparse # For parsing arguments passed to script
import json # For reading JSON-format text files
from jsonschema import validate # Validates JSON data with specified schema

## HELPER FUNCTIONS
def calculateBMI(mass, height):
    """
        Passed someone's mass and height, then uses BMI formula
        'BMI (kg/m^2) = mass (kg) / height (m)^2'
        to calculate the resulting BMI

        Args:
          mass - Float in assumed units of kilograms
          height - Float in assumed units of meters

        Returns: Float representing BMI number, rounded to first decimal
    """
    if mass <= 0 or height <= 0: # Quick data check
        raise OSError() # Mass or height should never be 0 or below
    BMIResult = mass / height ** 2
    if BMIResult <= 0:
        raise OSError() # BMI should never be negative or below 0
    return round(BMIResult, 1)

def groupByCategory(jsonData, jsonSchema, BMITable):
    """
        Reads in BMI table & BMI data & data schema, validates data, calculates
        each sample's BMI (if applicable), appends 3 new columns with relevant
        info to each valid sample, then counts which of them pass our specified
        desired category filter ('Overweight' by default)

        Args:
          jsonData - Array of dicts representing individuals
          jsonSchema - JSON dict to validate individuals' info is right format
          BMITable - JSON dict to capture BMI categories and health risk

        Returns: Tuple of grouped data and number of invalid samples
    """
    # Iterate through given JSON Data
    numberInvalid = 0
    groupedData = {key:[] for key in BMITable} # JSON data grouped by category
    for sample in jsonData:
        try:
            # Validate data
            validateJSONSchema(sample, jsonSchema)

            # Data is valid so calculate BMI
            height = sample['HeightCm'] / 100
            mass = sample['WeightKg']
            sampleBMI = calculateBMI(mass, height)

            # Determine BMI category the sample belongs to
            matchedCategory = None
            for BMICategory in BMITable: # Check all categories
                BMILowerLimit = BMITable[BMICategory]['BMILowerLimit']
                BMIUpperLimit = BMITable[BMICategory]['BMIUpperLimit']
                if BMIUpperLimit == 'inf' and sampleBMI >= BMILowerLimit:
                    matchedCategory = BMICategory
                    break
                elif sampleBMI >= BMILowerLimit and sampleBMI <= BMIUpperLimit:
                    matchedCategory = BMICategory
                    break

            # Then add sample if a matched category was found
            if matchedCategory:
                healthRisk = BMITable[BMICategory]['healthRisk']
                newInfo = (
                    {
                        'BMI': sampleBMI,
                        'BMICategory': matchedCategory,
                        'HealthRisk': healthRisk
                    }
                )
                updatedSample = sample | newInfo # Append 3 new columns
                groupedData[matchedCategory].append(updatedSample)
            else:
                raise IOError() # No BMI table match, skip sample

        except Exception: # Schema mismatch, BMI invalid, or no BMI Table match
            numberInvalid += 1

    # Return stats
    return (groupedData, numberInvalid)

def printResults(groupedData, filterCategory='Overweight'):
    """
        Displays number of people in specified category, 'Overweight' by default

        Args:
          groupedData - Dict of BMI categories, each category being an array of
          dicts where each dict represents an individual's information
          filterCategory - Key to search for in groupedData, 'Overweight' by
          default

        Returns: Integer representing number of people in the specified BMI
        category
    """
    matched = len(groupedData.get(filterCategory, {}))
    statsMessage = (
        f'Script has finished!\nThe number of people that match the '
        f'BMI category \'{filterCategory}\' is {matched}'
    )
    print(statsMessage)

def readJSON(fileLocation=None):
    """
        Tries to read in a JSON file and stores data.

        Args:
          String denoting file location of JSON data

        Returns: List of Dict or Dict, depending on JSON data
    """
    with open(fileLocation) as jsonFile:
        data = json.load(jsonFile)
        return data

def scriptParse():
    """
        Tries to parse args passed to script

        Returns: Object with script's arguments as attribs of its namespace
    """
    # Meta info
    scriptDescription = (
        f'Calculates folks\' BMI from JSON data then displays how many of them '
        f'are considered to be a part of the specified BMI category, '
        f'\'Overweight\' by default'
    )
    fileLocationHelp = f'File location of JSON data relative to script location'
    schemaLocationHelp = (
        f'Schema location relative to script location for validating JSON input'
        f' data'
    )
    tableLocationHelp = (
        f'Table location relative to script location for assigning BMI category'
        f' and health risk to BMI Range'
    )

    # Parse args
    try:
        parser = argparse.ArgumentParser(scriptDescription)
        parser.add_argument('--fileLocation', type=str, help=fileLocationHelp)
        parser.add_argument('--schemaLocation', type=str, help=schemaLocationHelp)
        parser.add_argument('--tableLocation', type=str, help=tableLocationHelp)
        args = parser.parse_args()
        return args
    except Exception:
        raise IOError("Error reading script arguments, refer to --help")

def validateJSONSchema(sample, jsonSchema):
    """
        Validates given JSON data according to specified schema

        Args:
          sample - JSON dict to validate
          jsonSchema - JSON dict to validate sample against

        Returns: True if valid, else raise exception
    """
    validate(instance=sample, schema=jsonSchema)
    return True

def writeJSON(rawData, fileLocation='.'):
    """
        Serializes data then writes JSON to a text file, saved in the same
        location as the script by default.

        Args:
          rawData - Raw data to serialize then store

        Returns: None as text file is created
    """
    # Serialize data to JSON
    jsonData = json.dumps(rawData, indent=4)

    # Write JSON data to text file
    with open(f"{fileLocation}/categorizedData.txt", "w") as outFile:
        outFile.write(jsonData)

## MAIN
if __name__ == "__main__":

    try:
        # Read in script args
        args = scriptParse()

        # Read JSON data file
        jsonData = readJSON(args.fileLocation)

        # Read in table of BMI Category and Health Risk
        BMITable = readJSON(args.tableLocation)

        # Validate data matches schema then group data
        jsonSchema = readJSON(args.schemaLocation)
        groupedData, invalidCount = groupByCategory(jsonData, jsonSchema, BMITable)
        print(f'\nFound {invalidCount} invalid BMI samples! Skipping those\n')

        # Write valid, grouped data to a new JSON file in script's location
        writeJSON(groupedData)

        # Display number of people in a specified category, 'Overweight' default
        printResults(groupedData)

    except Exception as error:
        print(f'Error! Script failed to execute properly due to error: {error}')
