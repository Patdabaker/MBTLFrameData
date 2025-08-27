import pandas as pd
import json
import os

def xlsx_to_json_per_sheet(xlsx_file, output_dir):
    xls = pd.ExcelFile(xlsx_file)

    for sheet_name in xls.sheet_names:
        if sheet_name == 'template':
            continue

        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Convert everything to string
        df = df.astype(str)

        # Replace "nan" (from empty cells) with "-"
        df = df.replace("nan", "")

        moves = []
        char_full_name = None

        for _, row in df.iterrows():
            # Grab full_name from the first row (assumes same for all moves)
            if char_full_name is None:
                char_full_name = row.get("full_name", sheet_name).strip()

            move = {}
            for col, val in row.items():
                if col == "full_name":
                    continue  # skip adding it to moves
                # Always make it string, strip whitespace
                val = str(val).strip() if val != "" else ""
                move[col] = val
            moves.append(move)

        # Build JSON with wrapper
        json_data = {
            "name": char_full_name,
            "moves": moves
        }

        # Output path
        output_path = os.path.join(output_dir, f"{sheet_name}.json")

        # Save JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        print(f"Saved {output_path}")

if __name__ == "__main__":
    xlsx_to_json_per_sheet("moves.xlsx", "data/characters")
