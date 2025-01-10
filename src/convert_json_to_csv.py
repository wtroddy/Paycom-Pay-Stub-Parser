"""Convert a JSON Payload from the PayCom pay stub website into a CSV
"""
 
from pathlib import Path 
import json 
import csv 

from pydantic_models import PaystubSection, Deductions, Taxes, NetPay

def read_payload_data(payload_json_file: Path) -> dict:
    with open(payload_json_file, 'r') as f:
        json_data = f.read()

    return json.loads(json_data) 

def flatten_paystub_section(SectionModel: PaystubSection, section_data: dict) -> list[PaystubSection]:
    section_flattened = []
    
    for section_code in section_data:
        d = SectionModel(**section_data[section_code], section_code=section_code)
        section_flattened.append(d.model_dump())

    return section_flattened

def write_to_csv(SectionModel: PaystubSection, output_path: Path, flattened_data: list) -> None:
    with open(output_path, 'w', newline='') as deductions_csv:
        fieldnames = list(SectionModel.model_fields.keys())
        writer = csv.DictWriter(deductions_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

def main(payload_json_file):
    payload = read_payload_data(payload_json_file = payload_json_file)
    paystub_data = payload["data"]

    deductions = []
    taxes = []
    net_pay = []

    for paystub in paystub_data:
        deductions.extend(flatten_paystub_section(SectionModel=Deductions, section_data=paystub["DDUCT"]))
        taxes.extend(flatten_paystub_section(SectionModel=Taxes, section_data=paystub["TAX"]))
        net_pay.extend(flatten_paystub_section(SectionModel=NetPay, section_data=paystub["NET"]))

    # output
    # TODO: parameterize these outputs 
    write_to_csv(SectionModel=Deductions, output_path=Path("data").joinpath("deductions.csv"), flattened_data=deductions)
    write_to_csv(SectionModel=Taxes, output_path=Path("data").joinpath("taxes.csv"), flattened_data=taxes)
    write_to_csv(SectionModel=NetPay, output_path=Path("data").joinpath("net_pay.csv"), flattened_data=net_pay)


if __name__ == "__main__":
    # TODO: parameterize the input 
    main(payload_json_file = Path("data").joinpath("2024_paystubs.json"))
