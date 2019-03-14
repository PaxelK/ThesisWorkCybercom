classdef Sink
    %Sink class
    %  This class is used for the sink. Contains movement of sink and data
    %  packets recieved
    
    properties
        xPos; % Position of mobile sink, x
        yPos; % Position of mobile sink, y
        dataRec; % Amount of packets received by sink
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
        end
        
        function obj = move(obj, deltax, deltay)
            %METHOD Move
            %   Input: deltax = sink movement in x
            %          deltay = sink movement in y
            %   The method moves the sink and stores the updated position
            %   of the sink in obj.pos
            %   return: obj = Sink object 
            
            obj.xPos = obj.xPos+deltax;
            obj.yPos = obj.yPos+deltay;
        end
        
        function packRec = getDataRec(obj)
            %METHID getDataRec
            %   Output: Total amount of bits received by the sink 
           packRec = obj.dataRec; 
        end
   
    end
end

