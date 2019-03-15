classdef Sink
    %Sink class
    %  This class is used for the sink. Contains movement of sink and data
    %  packets recieved
    
    properties
        xPos; % Position of mobile sink, x
        yPos; % Position of mobile sink, y
        dataRec; % Amount of packets received by sink
        sizeX;
        sizeY;
        alive;
        energy;
        maxenergy;
        SoC;
        nrjCons;
        ID;
    end
    
    methods
        function obj = Sink(sizex, sizey) 
            %Constructor: Constructs an instance of the class Sink 
            %  Input: sizex = WSN size, x 
            %         sizey = WSN size, y
            %  This method creates an instance of this class
                        
            obj.xPos = sizex/2;  % Initialize by placing sink in the middle of the WSN
            obj.yPos = sizey/2; % Initialize by placing sink in the middle of the WSN
            obj.dataRec = 0; % Initial packets recieved is zero 
            obj.sizeX = sizex;
            obj.sizeY = sizey;
            obj.alive = true;
            obj.energy = inf;
            obj.maxenergy = inf;
            obj.SoC = obj.energy/obj.maxenergy;
            obj.nrjCons = 0;
            obj.ID = pi;
        end
        
        function obj = move(obj, deltax, deltay)
            %METHOD Move
            %   Input: deltax = sink movement in x
            %          deltay = sink movement in y
            %   The method moves the sink and stores the updated position
            %   of the sink in obj.pos
            %   return: obj = Sink object 
            %   If the sink "tries" to go out of bounds, it is placed at the
            %   border of the grid.
           
            if(obj.xPos + deltax > obj.sizeX)
                obj.xPos = obj.sizeX;
            end
            if(obj.xPos + deltax < 0)
                obj.xPos = 0;
            end
            if(obj.yPos + deltay > obj.sizeY)
                obj.yPos = obj.sizeY;
            end
            if(obj.yPos + deltay < 0)
                obj.yPos = 0;
            end 
            if((obj.xPos + deltax <= obj.sizeX && obj.xPos + deltax >= 0) && (obj.yPos + deltay <= obj.sizeY && obj.yPos + deltay >= 0))
                obj.xPos = obj.xPos+deltax;
                obj.yPos = obj.yPos+deltay;
            end
           
        end
        
        function packRec = getDataRec(obj)
            %METHID getDataRec
            %   Output: Total amount of bits received by the sink 
           packRec = obj.dataRec; 
        end
        
        function [xpos, ypos] = getPos(obj)
            xpos = obj.xPos;
            ypos = obj.yPos;
        end
        
        function obj = updateSoC(obj)
            obj.SoC = obj.energy/obj.maxenergy;
        end
    end
end

