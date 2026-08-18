import os

base_dir = r"c:\Users\Raufb\Desktop\portfolio-main\portfolio-main\assets\research\ssh-pivoting"

# Map extracted filenames to descriptive names based on PDF page structure
renames = {
    "page02_img1.png": "01-lab-topology.png",
    "page04_img1.png": "02-kali-network-config-1.png",
    "page04_img2.png": "03-kali-network-config-2.png",
    "page06_img1.png": "04-ubuntu-setup-1.png",
    "page06_img2.png": "05-ubuntu-setup-2.png",
    "page08_img1.png": "06-ubuntu-pivot-config.png",
    "page10_img1.png": "07-static-ip-config-1.png",
    "page10_img2.png": "08-static-ip-config-2.png",
    "page12_img1.png": "09-metasploitable-config-1.png",
    "page12_img2.png": "10-metasploitable-config-2.png",
    "page14_img1.png": "11-connectivity-ping-test.png",
    "page16_img1.png": "12-ssh-connection-1.png",
    "page16_img2.png": "13-ssh-connection-2.png",
    "page18_img1.png": "14-proxychains-config.png",
    "page18_img2.png": "15-proxychains-nc-test.png",
    "page20_img1.png": "16-final-ssh-metasploitable.png",
}

for old_name, new_name in renames.items():
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
    else:
        print(f"Missing: {old_name}")

print("\nDone!")