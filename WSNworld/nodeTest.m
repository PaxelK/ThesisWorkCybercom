clc, clear all, close all

parameters = struct;
parameters.ps = 200;
parameters.maxNrj = 2;
parameters.Elec = 50*10^(-9);
parameters.Eamp = 100*10^(-12);
parameters.EDA = 5*10^(-9);



a = Node(1, 1, 2, 1, parameters);    % Normal non-CH node
b = Node(2, 5, 6, 1, parameters);    % Normal non-CH node

c = Node(3, 8, 9, 0.5, parameters);    % Normal CH node
c.CHstatus = 1;

d = Node(4, 11, 12, 0, parameters);    % Normal dead node

e = Node(5, 15, 16, 0, parameters);    % dead CH node
e.CHstatus = 1;


%{
Testing the connect function
%}
[a, result] = a.sendMsg(b);     % Normal to normal
disp(result);                   % Boolean return
[b, result] = b.sendMsg(a);     % Normal to normal reversed
                
[a, result] = a.sendMsg(c);     % Normal to CH
[c, result] = c.sendMsg(b);     % CH to normal (fails)
disp(result);           
        
[a, result] = a.sendMsg(d);     % Normal to dead normal
[a, result] = a.sendMsg(e);     % Normal to dead CH