clear all
close all
clc

x = Sink(100, 100);

x = x.move(2, 30);
x = x.move(30, 30);



for i=1:10;
 x = x.packRec(100 + (i*4));
end 

x