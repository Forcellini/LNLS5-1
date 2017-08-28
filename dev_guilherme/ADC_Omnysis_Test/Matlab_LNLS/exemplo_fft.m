load data

nbits = 16;
Fs = 118.23;

data_fs = data/2^(nbits-1);

[Y,f] = fourierseries(data_fs, Fs);

figure
plot(f, 20*log10(Y));
xlabel('MHz');
ylabel('dBFS');
grid on;
axis([f(1) f(end) -180 0]);