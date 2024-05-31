import pandas as pd
import ipaddress

csv_file_path = 'ips.csv'  # Replace with your CSV file path
column_name = 'Address'  # Replace with your CSV column name containing IP addresses


def calculate_subnet_ranges(ip_list, ip_class):
    # Set to store unique subnets
    subnet_ranges = set()

    # Define class ranges and subnet masks
    if ip_class == 'A':
        subnet_range_start = ipaddress.IPv4Address('1.0.0.0')
        subnet_range_end = ipaddress.IPv4Address('127.0.0.0')
        subnet_mask = '255.0.0.0'
    elif ip_class == 'B':
        subnet_range_start = ipaddress.IPv4Address('128.0.0.0')
        subnet_range_end = ipaddress.IPv4Address('191.255.0.0')
        subnet_mask = '255.255.0.0'
    elif ip_class == 'C':
        subnet_range_start = ipaddress.IPv4Address('192.0.0.0')
        subnet_range_end = ipaddress.IPv4Address('223.255.255.0')
        subnet_mask = '255.255.255.0'
    else:
        return []

    for ip in ip_list:
        try:
            # Parse the IP address
            ip_obj = ipaddress.ip_address(ip)
            # Check if the IP address is within the specified class range
            if subnet_range_start <= ip_obj <= subnet_range_end:
                # Determine the subnet range
                subnet = ipaddress.ip_network(f"{ip_obj}/{subnet_mask}", strict=False)
                # Add the subnet range to the set
                subnet_ranges.add(str(subnet))
        except ValueError:
            print(f"Invalid IP address: {ip}")

    # Convert set to list
    return list(subnet_ranges)


def read_ip_addresses_from_csv(file_path, column_name):
    # Read the CSV file
    df = pd.read_csv(file_path)
    # Extract the IP addresses from the specified column
    ip_list = df[column_name].dropna().tolist()  # Drop any NaN values and convert to list
    return ip_list


def main():
    # Read IP addresses from CSV
    ip_list = read_ip_addresses_from_csv(csv_file_path, column_name)

    # Calculate unique subnets for each class
    class_a_subnets = calculate_subnet_ranges(ip_list, 'A')
    class_b_subnets = calculate_subnet_ranges(ip_list, 'B')
    class_c_subnets = calculate_subnet_ranges(ip_list, 'C')

    # Export unique subnets to a text file
    with open('unique_subnets.txt', 'w') as file:
        file.write("Class A Subnets:\n")
        for subnet in class_a_subnets:
            file.write(f"{subnet}\n")

        file.write("\nClass B Subnets:\n")
        for subnet in class_b_subnets:
            file.write(f"{subnet}\n")

        file.write("\nClass C Subnets:\n")
        for subnet in class_c_subnets:
            file.write(f"{subnet}\n")

    print("Unique subnets have been written to unique_subnets.txt")


if __name__ == "__main__":
    main()
