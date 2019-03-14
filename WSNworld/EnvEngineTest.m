clc, clear all, close all

EE = EnvironmentEngine();

[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(20, 20, 1);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(40, 40, 50);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(-40, -40, 50);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
EE = EE.updateEnv(-1000, -1000, 50);
[x y] = EE.sink.getPos();
fprintf('x = %d, y = %d\n', x, y);
