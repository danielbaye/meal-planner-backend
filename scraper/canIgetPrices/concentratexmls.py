import os
import zipfile
import xml.etree.ElementTree as ET
import csv


def extract_xml_from_gz(gz_file):
    """Extract XML content from a .gz file."""
    string = ''
    with zipfile.ZipFile(gz_file, 'r') as z:
        # Assuming there's only one XML file in the zip
        for xml_file in z.namelist():
            if xml_file.endswith('.xml'):
                with z.open(xml_file) as f:
                    string = f.read()
    return string


def parse_xml(xml_content):
    """Parse XML content and extract relevant fields."""
    root = ET.fromstring(xml_content)
    data = []
    chain_id = root.find('ChainId').text
    sub_chain_id = root.find('SubChainId').text
    store_id = root.find('StoreId').text
    bikoret_no = root.find('BikoretNo').text
    # Example: Extract data from XML (adjust based on your XML structure)
    for item in root.findall(
            './/Item'):  # Adjust 'YourItemTag' to your XML structure
        row = {
            'name': item.find('ItemNm').text,
            'price': item.find('ItemPrice').text,
            'barcode': item.find('ItemCode').text,
            'units': item.find('UnitQty').text,
            'updateDate': item.find('PriceUpdateDate').text,
            'store_id': store_id,
            'chain_id': chain_id,
            'sub_chain_id': sub_chain_id,
        }
        data.append(row)

    return data


def main(gz_directory, output_csv):
    all_data = []

    # Iterate through each .gz file in the specified directory
    for filename in os.listdir(gz_directory):
        if filename.endswith('.gz'):
            gz_path = os.path.join(gz_directory, filename)
            xml_content = extract_xml_from_gz(gz_path)
            data = parse_xml(xml_content)
            all_data.extend(data)

    # Write combined data to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=[
                                    'name',
                                    'price',
                                    'barcode',
                                    'updateDate',
                                    'units',
                                    'store_id',
                                    'chain_id',
                                    'sub_chain_id',
                                ])  # Add more field names as needed
        writer.writeheader()
        writer.fieldnames = [
            'name',
            'price',
            'barcode',
            'updateDate',
            'units',
            'store_id',
            'chain_id',
            'sub_chain_id',
        ]
        for row in all_data:
            try:
                writer.writerow(row)
            except:
                pass

    print(f"Combined CSV saved to: {output_csv}")


# Usage
gz_directory = 'goodfarm'  # Update this to your .gz files directory
output_csv = 'combined_data.csv'  # Desired output CSV file name
main(gz_directory, output_csv)
