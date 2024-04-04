import os
import struct
import errno

# Define the equivalent structure in Python
class COMPLEX:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

# Define the dimensions of the matrix
ROWS = 3
COLS = 3
DEPTH = 114

myfifo = '/tmp/myfifo'

# Open the FIFO pipe for reading
read_pipe = os.open(myfifo, os.O_RDONLY)

# Read binary data from the pipe
data_buffer = os.read(read_pipe, ROWS * COLS * DEPTH * struct.calcsize('ii'))

# Unpack the binary data into the 3x3x114 matrix of type COMPLEX
csi_matrix = []
for i in range(ROWS):
    row = []
    for j in range(COLS):
        complex_array = []
        for k in range(DEPTH):
            index = (i * COLS * DEPTH + j * DEPTH + k) * struct.calcsize('ii')
            data = struct.unpack('ii', data_buffer[index:index + struct.calcsize('ii')])
            complex_array.append(COMPLEX(*data))
        row.append(complex_array)
    csi_matrix.append(row)

# Print the values
for i in range(ROWS):
    for j in range(COLS):
        for k in range(DEPTH):
            print(f"({csi_matrix[i][j][k].real}, {csi_matrix[i][j][k].imag})", end=' ')
        print()
    print()

# Close the pipe
os.close(read_pipe)


'''
import errno
import os
import struct

# Define the equivalent structure in Python
class COMPLEX:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

myfifo = '/tmp/myfifo'
try:
    os.mkfifo(myfifo, mode=0o777)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

# Open the FIFO pipe for reading
read_pipe = open(myfifo, 'rb')
print('Opened pipes')

while True:
    # Read binary data from the pipe
    data = read_pipe.read(struct.calcsize('ff'))

    # Check if data is available
    if data:
        # Unpack the binary data into real and imag variables
        real, imag = struct.unpack('ii', data)

        # Create COMPLEX object
        complex_data = COMPLEX(real, imag)

        # Print the values
        print("Received: Real =", complex_data.real, ", Imag =", complex_data.imag)


'''