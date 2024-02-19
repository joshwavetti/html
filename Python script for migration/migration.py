from bs4 import BeautifulSoup
import os
import shutil
import json

# Create a folder called "Migrated Icons"
os.makedirs("Migrated Icons", exist_ok=True)

# Read the HTML file
with open("tab.html", "r") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find the table
table = soup.find("table")

# Iterate over each row in the table
for row in table.find_all("tr")[1:]:  # Skip the header row
    # Extract data from each cell in the row
    cells = row.find_all("td")
    id_, product, biom, package_id, draft_img, final_img, order_type, tags, state, description, name, resolutions, version_number, requirements, requester, icon_location, needed_until, requester_mail, iterations = [cell.get_text().strip() for cell in cells]

    # Create a folder with the name in the "Name" cell of that row
    folder_name = os.path.join("Migrated Icons", name)
    os.makedirs(folder_name, exist_ok=True)

    # Copy the png file from "Draft" column to a subfolder named "Draft"
    draft_folder = os.path.join(folder_name, "Draft")
    os.makedirs(draft_folder, exist_ok=True)
    if draft_img and draft_img.find("img"):
        draft_img_src = draft_img.find("img")["src"]
        shutil.copy(draft_img_src, draft_folder)

    # Copy the png file from "Final" column to the folder
    if final_img and final_img.find("img"):
        final_img_src = final_img.find("img")["src"]
        shutil.copy(final_img_src, folder_name)

    # Create a JSON file for that row
    json_data = {
        "Id": id_,
        "Product": product,
        "Biom": biom,
        "PackageID": package_id,
        "OrderType": order_type,
        "Tags": tags,
        "State": state,
        "Description": description,
        "Name": name,
        "Resolutions": resolutions,
        "VersionNumber": version_number,
        "Requirements": requirements,
        "Requester": requester,
        "IconLocation": icon_location,
        "NeededUntil": needed_until,
        "RequesterMail": requester_mail,
        "Iterations": iterations
    }
    json_file_path = os.path.join(folder_name, f"{name}.json")
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

print("Processing completed.")
