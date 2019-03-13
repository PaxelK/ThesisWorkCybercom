classdef Sink
    %Sink class
    %  This class is used for the sink. Contains movement of sink and data
    %  packets recieved
    
    properties
        pos; % Position of mobile sink
        packRecieved; % Amount of packets recieved by sink
    end
    
    methods
        function obj = Sink(sizex, sizey) 
            %Constructor: Constructs an instance of the class Sink 
            %  Input: sizex = WSN size, x 
            %         sizey = WSN size, y
            %  This method creates an instance of this class
                        
            obj.pos = [sizex/2, sizey/2] ; % Initialize by placing sink in the middle of the WSN
            obj.packRecieved = 0; % Initial packets recieved is zero 
        end
        
        function obj = move(obj, deltax, deltay)
            %METHOD Move
            %   Input: deltax = sink movement in x
            %          deltay = sink movement in y
            %   The method moves the sink and stores the updated position
            %   of the sink in obj.pos
            %   return: obj = Sink object 
            
            sinkPos = [obj.pos(1)+deltax, obj.pos(2)+deltay];
            obj.pos = sinkPos;
        end
        
        function obj = packRec(obj, packSize)
             %METHOD packRec
             %   Input: Packsize = Size of package that was recieved 
             
             %   This method updates the aamount of packages that the sink
             %   has recieved
             %   return: packetsRec = The total amount of packets that have
             %   been sent
            obj.packRecieved = obj.packRecieved + packSize;
            %packetsRec = obj.packRecieved;
        end 
        
   
    end
end

