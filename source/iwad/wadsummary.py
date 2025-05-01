import struct
import csv
import sys

# WAD header structure (4 bytes for ID, 4 bytes for lump count, and 4 bytes for directory offset)
WAD_HEADER_FORMAT = '4sii'
WAD_HEADER_SIZE = struct.calcsize(WAD_HEADER_FORMAT)

# Directory entry structure (4 bytes for lump offset, 4 bytes for lump size, 4 bytes for lump name)
LUMP_ENTRY_FORMAT = 'ii4s'
LUMP_ENTRY_SIZE = struct.calcsize(LUMP_ENTRY_FORMAT)

# Lump names we're interested in
LUMP_NAMES = [
    b"THINGS", b"LINEDEFS", b"SIDEDEFS", b"VERTEXES", b"SEGS", b"SSECTORS",
    b"NODES", b"SECTORS", b"REJECT", b"BLOCKMAP"
]

def parse_wad(file_path):
    with open(file_path, 'rb') as f:
        # Read the WAD header
        header = f.read(WAD_HEADER_SIZE)
        wad_id, lump_count, directory_offset = struct.unpack(WAD_HEADER_FORMAT, header)

        # Check if it's a valid WAD file
        if wad_id != b'IWAD' and wad_id != b'PWAD':
            raise ValueError("Not a valid WAD file.")

        # Read the lump directory entries
        f.seek(directory_offset)
        lumps = []
        for _ in range(lump_count):
            entry = f.read(LUMP_ENTRY_SIZE)
            offset, size, name = struct.unpack(LUMP_ENTRY_FORMAT, entry)
            lumps.append((offset, size, name.strip(b'\0')))

        return lumps

def extract_lump_sizes(file_path):
    lumps = parse_wad(file_path)

    # Create a dictionary to store lump sizes per map
    map_lump_sizes = {}

    for offset, size, name in lumps:
        if name in LUMP_NAMES:
            # Find the map name from the lump (assuming the lumps are sorted by map)
            map_name = name.decode('ascii')

            # If the map isn't already in the dictionary, create a new entry
            if map_name not in map_lump_sizes:
                map_lump_sizes[map_name] = {}

            # Add the lump size to the map entry
            map_lump_sizes[map_name][name.decode('ascii')] = size

    return map_lump_sizes

def save_to_csv(data, output_path):
    # Create CSV file
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Writing header row
        header = ['Map'] + LUMP_NAMES
        writer.writerow(header)

        # Writing map lump sizes
        for map_name, lump_sizes in data.items():
            row = [map_name] + [lump_sizes.get(name.decode('ascii'), 0) for name in LUMP_NAMES]
            writer.writerow(row)

if __name__ == "__main__":
    # Replace with your WAD file path
    input_wad_path = sys.argv[1]
    output_csv_path = "map_lump_sizes.csv"

    # Extract lump sizes from the WAD file
    lump_sizes_data = extract_lump_sizes(input_wad_path)

    # Save the data to a CSV file
    save_to_csv(lump_sizes_data, output_csv_path)
    print(f"CSV file saved to {output_csv_path}")
