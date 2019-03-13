clc, clear all, close all


a = Node(1,1,2,200,1,2);
b = Node(2,5,6,200,1,2);
c = Node(3,8,9,200,1,3);
c.CHstatus = 1;

[a, result] = a.connect(b);
disp(result);
[a, result] = a.connect(c);
disp(result);
[c, result] = c.connect(a);
disp(result);
