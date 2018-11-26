import socket                   # Import socket module
# import ffmpeg-python                   #import ffmpeg

ffmpeg = __import__("ffmpeg-python")

s = socket.socket()             # Create a socket object
host = "localhost"  #Ip address that the TCPServer  is there
port = 50000                     # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect((host, port))
s.send(b'Hello server!')
# filename = s.recv(16)
# filename = s.recv(filename)
with open('movie.mp4', 'wb') as f:
    print ('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')

print('Applying overlay')

in_file = ffmpeg.input('movie.mp4')
overlay_file = ffmpeg.input('overlay.jpg')
(
    ffmpeg
    .concat(
        in_file.trim(start_frame=10, end_frame=20),
        in_file.trim(start_frame=30, end_frame=40),
    )
    .overlay(overlay_file.hflip())
    .drawbox(50, 50, 120, 120, color='red', thickness=5)
    .output('out.mp4')
    .run()
)
