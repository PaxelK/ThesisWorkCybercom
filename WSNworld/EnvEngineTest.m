clc, clear all, close all

EE = EnvironmentEngine();

[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(30, 30, 1);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(40, 40, 50);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(-40, -40, 50);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(-1000, -1000, 50);
[x y d] = EE.sinkStatus();
EE = EE.updateEnv(20, 20, 50);
[x y d] = EE.sinkStatus();
fprintf('x = %d, y = %d, dataRec = %d\n', x, y, d);

states = EE.getStates();


EE.rnd = 15;
EE = EE.cluster();
EE = EE.communicate();