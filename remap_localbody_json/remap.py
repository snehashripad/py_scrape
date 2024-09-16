import json

# Load the original JSON data
original_json = {
    "Gram Panchayat: Akkalkuwa (अक्कलकुवा)": {
        "Gram Panchayat": "Akkalkuwa",
        "Sarpanch": {
            "Name": "Rajeshwari Indravadan Valvi",
            "Phone Number": "9307106400"
        },
        "Secretary": {
            "Name": "Ganesh Jalamsing Vasave",
            "Phone Number": "8275702836"
        }
    }
}

restructured_data = {}
Phone_numbers = []

# Extract the gram panchayat name from the original data
gram_panchayat_name = list(original_json.keys())[0]
gram_panchayat_info = original_json[gram_panchayat_name]


for post, details in gram_panchayat_info.items():
    if post != "Gram Panchayat":
        phone_number = details["Phone Number"]
        restructured_data[phone_number] = {
            # "AC_Name" : 001,
            "Name": details["Name"],
            "Gram Panchayat": gram_panchayat_info["Gram Panchayat"],
            "Post": post,
        }


print(json.dumps(restructured_data, indent=4))

# Optionally, save the restructured data to a new JSON file
with open(r'D:\restructured_data.json', 'w') as file:
    json.dump(restructured_data, file, indent=4)

