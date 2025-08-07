# Mapping logic for Teema_Sample_Data.csv to Parts_Template.csv
# Each entry maps a Parts_Template column to a Teema_Sample_Data column
MAPPING = {
    'Part Code': 'Sku',            # Input column A -> Parts column A
    'Desc1': 'Description',        # Input column B -> Parts column B
    'Desc2': 'Description',        # Input column B -> Parts column C
    'HS Code': 'US H.S Codes',     # Input column F -> Parts column D
    'COO Code': 'Country of origin',
    'Vend Price': 'Cost',
    'Cli Code': "_GEN",
    'Vend Code': "_GEN",          # Input column C -> Parts column R
    'COE': "_GN",
    'TT': "02",
    'Cust Ctry': "CA",
    'TaxRefNum': "001",
    'Sls UOM Code': "KGM",
    'Ext Fibre Coverage': "NO",
    'KWeight UOM': "KGM",
    'TPL Possible': "NO",
    'Cert Sts': "OK"
}
