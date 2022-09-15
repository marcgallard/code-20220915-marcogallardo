"""
    Description: This script is used to test the functions contained within
    'groupBMI.py' script. Assumes it's in the same folder as the tested
    script and has a subfolder called "tests".
"""

## IMPORTS
import json # For reading JSON-format text files
import unittest # Unit testing

## FUNCTIONS TO TEST
from groupBMI import (
    readJSON,
    validateJSONSchema as validate,
    calculateBMI,
    groupByCategory,
    writeJSON
)


## CLASSES
class TestCalculate(unittest.TestCase): # Test main script

    ## CONSTANTS
    basePath = "./tests" # Where test data is stored in

    ## FUNCTIONS
    def testRead(self): # Make sure JSON read is done correctly
        dataPath = f'{self.basePath}/dummyJSON.txt'
        readData = readJSON(dataPath)

        # Expected data
        expectedData = {
            "firstKey": {
            "test1": 1,
            "test2": 2
            },
            "secondKey": {
                "test1": 11,
                "test2": 22,
                "test3": 3
            },
            "thirdKey": {}
        }

        # Assert both are identical
        self.assertEqual(readData, expectedData, "Data should be same")

        # Change expected to verify again
        expectedData["thirdKey"] = 4

        # Assert both are not identical
        failMsg = "Read should be different from expected"
        self.assertNotEqual(readData, expectedData, failMsg)

    def testValidate(self): # Checks JSON schema validation is correct
        # First read in dummy schema
        validSchemaPath = f'{self.basePath}/dummySchema.txt'
        validSchema = readJSON(validSchemaPath)

        # Then dummy data
        dataPath = f'{self.basePath}/dummyJSON.txt'
        readData = readJSON(dataPath)

        # Finally invalid schema
        invalidSchemaPath = f'{self.basePath}/faultySchema.txt'
        invalidSchema = readJSON(invalidSchemaPath)

        # Asserting dummy JSON fits our dummy schema
        self.assertTrue(validate(readData, validSchema))

        # Assert exception is raised when JSON does not fit invalid schema
        self.assertRaises(Exception, validate(readData, invalidSchema))

    def testCalculateBMI(self): # Checks calculation is accurate
        # First read in dummy BMI data
        BMIDataPath = f'{self.basePath}/dummyBMIData.txt'
        readData = readJSON(BMIDataPath)

        # First sample check, should be good
        mass = readData[0]['WeightKg']
        height = readData[0]['HeightCm'] / 100
        sampleBMI = calculateBMI(mass, height)
        expectedBMI = 32.8
        self.assertEqual(sampleBMI, expectedBMI)

        # Second sample check, should raise exception due to mass < 0
        mass = readData[1]['WeightKg']
        height = readData[1]['HeightCm'] / 100
        with self.assertRaises(OSError):
            calculateBMI(mass, height)

        # Third sample check, should raise exception due to BMI being 0
        mass = readData[2]['WeightKg']
        height = readData[2]['HeightCm'] / 100
        with self.assertRaises(OSError):
            calculateBMI(mass, height)

        # Fourth sample check, should raise exception due to mass and height < 0
        mass = readData[3]['WeightKg']
        height = readData[3]['HeightCm'] / 100
        with self.assertRaises(OSError):
            calculateBMI(mass, height)

    def testGroupCategory(self): # Checks 'Moderately obese' is counted correctly
        # First read in dummy BMI data
        BMIDataPath = f'{self.basePath}/dummyBMIData.txt'
        readData = readJSON(BMIDataPath)

        # Then read in valid BMI schema
        validSchemaPath = f'{self.basePath}/validSchema.txt'
        validSchema = readJSON(validSchemaPath)

        # Then valid BMI table
        tablePath = f'{self.basePath}/validTable.txt'
        validTable = readJSON(tablePath)

        # Finally invalid schema
        invalidSchemaPath = f'{self.basePath}/faultySchema.txt'
        invalidSchema = readJSON(invalidSchemaPath)

        # Do a run of grouping with valid schema
        groupedData, numberInvalid = groupByCategory(readData, validSchema, validTable)
        self.assertEqual(numberInvalid, 3) # 3 samples should have been invalid
        self.assertEqual(len(groupedData['Moderately obese']), 1)

        # Then do run with invalid schema, yielding all 4 as invalid
        groupedData, numberInvalid = groupByCategory(readData, invalidSchema, validTable)
        self.assertEqual(numberInvalid, 4) # 3 samples should have been invalid
        self.assertEqual(len(groupedData['Moderately obese']), 0)

    def testWriteJSON(self): # Checks written JSON corresponds to stored JSON
        # First create dummy JSON to test
        dummyJSON = {'first': 1, 'second': {'a': 0, 'b': -1}}

        # Then determine file to write (and later read) to
        writeJSON(dummyJSON, self.basePath)
        filePath = f'{self.basePath}/categorizedData.txt'
        readData = readJSON(filePath)

        # Check what's written is the same as what's expected
        self.assertEqual(dummyJSON, readData)

## TESTING
if __name__ == '__main__':
    print("\nBeginning testing...\n")
    unittest.main()