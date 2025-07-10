# Mapping logic for Teema_Sample_Data.csv to Parts_Template.csv
# Each entry maps a Parts_Template column to a Teema_Sample_Data column
MAPPING = {
    'Part Code': 'Sku',            # Teema column A -> Parts column A
    'Desc1': 'Description',        # Teema column B -> Parts column B
    'Desc2': 'Description',        # Teema column B -> Parts column C
    'HS Code': 'US H.S Codes',     # Teema column F -> Parts column D
    'Cert Org Code': 'US H.S Codes',  # Teema column F -> Parts column AK
    'Vend Price': 'Cost',          # Teema column C -> Parts column R
}
