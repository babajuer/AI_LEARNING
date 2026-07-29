from IPython.display import display, HTML
import requests



print("Hello AI!")

with open("email.txt", "r") as f:
    email = f.read()
    print(email)


for i in range(5):
    print(i)

#download the file from the internet
url = "https://www.languageguide.org/french/vocabulary/alphabet/"
response = requests.get(url)
if response.status_code == 200: 
    with open("email.txt", "wb") as f:
        f.write(response.content)
    print("File downloaded successfully.")


def download_file(url, filename):
    response = requests.get(url)

    with open(filename, "wb") as f:
        f.write(response.content)


download_url = "https://scontent-cdg6-1.cdninstagram.com/v/t51.82787-15/754142585_18607105162048681_7457630162797837069_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=106&ig_cache_key=Mzk0Njc4NzU3NTMwODYxMTM4Mw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMzA3Mi5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=amLD-Z7z-GcQ7kNvwHVb_Jb&_nc_oc=AdqmT9TkgG4M_xmz8GgZq4xNu9heyQYRBzHvFM59dlbvERqIhmDjDTX0kL4vx3s5c6Ja10kgcq22P8dXGLBADf5Y&_nc_zt=23&_nc_ht=scontent-cdg6-1.cdninstagram.com&_nc_gid=WhC9eWb0FtedA2TfU2hqBw&_nc_ss=7b689&oh=00_AQBTy3PGVbzn1r8W3ELz_9mDjr8nPjT12BhizhL45pO2kg&oe=6A66F41F"

download_file(download_url, "ins.jpg")