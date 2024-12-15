import ftplib
HOSTNAME = "10.1.67.193"
USERNAME = "user"
PASSWORD = "pwd"
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"
filename = "login.txt"
with open(filename, "rb") as file:
    ftp_server.storbinary(f"STOR {filename}", file)
ftp_server.dir()
ftp_server.quit()
