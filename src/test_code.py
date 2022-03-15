x = [1, 2, 3, 4, 5, 6]
y = [1, 2, 3, 4, 5, 6]
theta1 = []
theta2 = []
    
# Convert G code to Thetas
for i in range(len(y)):
    theta2.append((y[i]/.0622)*16384)                         #rotations
    theta1.append((x[i]/(4.852*y[i] + 2.315))*16384/6.28318)      #degrees
print(x)
print(theta1)
print(y)
print(theta2)