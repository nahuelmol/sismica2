import matplotlib.pyplot as plt
import numpy as np

A = 20
w0 = 20 * np.pi;
phi = 0;
t = np.linspace(0, 2 * np.pi, 1000);
a = 20;

W = A * np.sin( w0 * t + phi) * np.exp( -a * t);
W1 = W[:60] #recorto la señal para hacer un zoom
t1 = t[:60] #aca tambien

plt.figure(figsize=(12,6))

plt.subplot(2,2,1)
plt.plot(t1,W1);
plt.xlabel("frec")
plt.ylabel("Amplitud")

plt.subplot(2,2,2)
plt.stem(t1,W1);
plt.xlabel("frec")
plt.ylabel("Amplitud")

plt.show()
