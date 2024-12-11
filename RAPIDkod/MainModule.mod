MODULE MainModule

    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: Joenn
    !
    ! Version: 1.0
    !
    !***********************************************************
    VAR socketdev serverSocket;
    VAR socketdev clientSocket;
    VAR string ipAddr := "192.168.125.1"; !För anslutning till faktiska roboten
    !VAR string ipAddr := "127.0.0.1"; !För anslutning till simulerade roboten
    VAR num portNmbr := 4000;
    VAR string data;
    VAR string xVal;
    VAR string yVal;
    VAR string zVal;
    VAR num xValue;
    VAR num yValue;
    VAR num zValue;
    VAR string gripValue;
    VAR robtarget home;
    VAR robtarget calcPos;
    VAR robtarget targetPos;
    VAR bool ok;
    VAR num increment := 10;
    VAR num recvNum;
    VAR num ERR_OUTSIDE_REACH := 50050;
    VAR errnum customErrNmr;
    VAR jointtarget jointPos; !För att kolla ifall MoveL är tillåten.
    VAR robtarget currentPos; !Från dokumentationen https://library.e.abb.com/public/688894b98123f87bc1257cc50044e809/Technical%20reference%20manual_RAPID_3HAC16581-1_revJ_en.pdf

    func string grip()
        IF  DOutput(DO10_0) = 1 THEN
                ! TAR IHOP GRIPKLON !
                gripValue := "gripActive";
                ReSet DO10_0;
                Set DO10_1;
                RETURN gripValue;
        ELSE
             !SLÄPPER GRIPKLON !
             gripValue := "gripInactive";
            ReSet DO10_1;
            Set DO10_0; 
            RETURN gripValue;
        ENDIF
    ENDfunc
   
   FUNC bool MoveHome()
        currentPos := getCurrentPos();
        !Hem position x600 y0 z340 q1 0 q2 0.7 q3 -0.7 q4 0
        home := [[600,0,340],[0,0.7,-0.7,0],currentPos.robconf,currentPos.extax];
        TPWrite "Homing..";
        MoveL home,v1000,z50,tool0;
        WaitUntil \InPos,TRUE;
        RETURN TRUE;
   ENDFUNC
   FUNC bool offset(String data)
        extractvalues data;
        currentPos := getCurrentPos();
        targetPos := [[currentPos.trans.x+xValue,currentPos.trans.y+yValue,currentPos.trans.z+zValue],[0,-0.04708,-0.99889,0],currentPos.robconf,currentPos.extax];
        MoveL targetPos ,v100,z50,tool0;
        WaitUntil \InPos, TRUE;
        RETURN TRUE;    
   ENDFUNC
   
   FUNC bool movement()
       currentPos := getCurrentPos();
       TEST data
            CASE "xpos": !Increment X-pos
                currentPos.trans.x := currentPos.trans.x + increment;

            CASE "xneg": !Increment X-neg
                currentPos.trans.x := currentPos.trans.x - increment;

            CASE "ypos": !Increment y-pos
                currentPos.trans.y := currentPos.trans.y + increment;

            CASE "yneg": !Increment y-neg
                currentPos.trans.y := currentPos.trans.y - increment;
                
            CASE "zpos": !Increment z-pos
                currentPos.trans.z := currentPos.trans.z + increment;
                
            CASE "zneg": !Increment z-neg
                currentPos.trans.z := currentPos.trans.z - increment;        
       ENDTEST
       jointPos := CalcJointT(currentPos,tool0\WObj:=wobj0\ErrorNumber:=customErrNmr);
       TPWrite ValToStr(customErrNmr);
       IF customErrNmr = ERR_ROBLIMIT OR customErrNmr = 1146 THEN
            TPWrite "Försökte flytta utanför reach";
            SocketSend clientSocket\Str:="Outside of reach";
            RETURN FALSE;
       ELSE
            MoveL currentPos,v100,z50,tool0;
            WaitUntil \InPos,TRUE;
            SocketSend clientSocket\Str:="ReadyForInput";
            RETURN TRUE;
       ENDIF
   ENDFUNC
   
   
   FUNC robtarget getCurrentPos()
       currentPos:=CRobT(\Tool:=tool0,\WObj:=wobj0);
       RETURN currentPos;
   ENDFUNC
   
   PROC extractvalues(string data)
        VAR string xStr;
        VAR string yStr;
        VAR string zStr;
        VAR num comma1;
        VAR num comma2;
        VAR num comma3;
        TPWrite data;
        
        ! Find the positions of the commas
        comma1 := StrFind(data, 1, ",");
        comma2 := StrFind(data, comma1 + 1, ",");
        comma3 := StrFind(data, comma2 + 1, "," );

        ! Extract the substrings
        xStr := StrPart(data, 1, comma1 - 1);
        yStr := StrPart(data, comma1 + 1, comma2 - comma1 - 1);
        zStr := StrPart(data, comma2 + 1, StrLen(data) - comma2 -1);
        
        ! Extracing the values from string to num
        ok := StrToVal(xStr, xValue);
        ok := StrToVal(yStr, yValue);
        ok := StrToVal(zStr, zValue); 
        ENDPROC
    
    PROC main()
        SocketCreate serverSocket;
        SocketBind serverSocket,ipAddr,portNmbr;
        SocketListen serverSocket;
        TPWrite "Väntar på connection...";
        SocketAccept serverSocket,clientSocket,\Time:=200;
        TPWrite "Sending Connection established to python script";
        SocketSend clientSocket\Str:="Connection established";
        TPWrite "Successfully sent msg to python script";
        
        WHILE TRUE DO
            TPWrite "Waiting for instructions from python script";
            SocketReceive clientSocket\Str:=data; !Från Python-appen
            
            TEST data
                CASE "Grip":
                gripValue := grip();
                TPWrite gripValue;
                SocketSend clientSocket\Str:=gripValue;
                
                CASE "Change increment":
                    SocketSend clientSocket\Str:="Please input a new incrementation value";
                    SocketReceive clientSocket\Str:=data;
                    TPWrite "Increment är nu "+data;
                    ok := StrToVal(data,increment);
                    SocketSend clientSocket\Str:="Value successfully changed!";
                    
                CASE "StartKeyboardMovement":
                    SocketSend clientSocket\Str:="Entering keyboard mode";
                    SocketReceive clientSocket\Str:=data;
                    WHILE NOT data = "DONE" DO
                        ok := movement();
                        SocketReceive clientSocket\Str:=data;
                    ENDWHILE
                    SocketSend clientSocket\Str:="Finished keyboard movement";
                
                CASE "Home":
                    SocketSend clientSocket\Str:="Homing";
                    ok := MoveHome();
                    
                    
                CASE "moveToPickup":
                    currentPos := getCurrentPos();
                    targetPos := [[150.8,677.4,282.3],[0.0168,0.67691,-0.73585,-0.00723],currentPos.robconf,currentPos.extax];
                    TPWrite "Flyttar till pluppen";
                    MoveL targetPos,v1000,z50,tool0;
                    WaitUntil \InPos,TRUE;
                    WaitTime 1;
                    targetPos := [[150.8,677.4,244.3],[0.0168,0.67691,-0.73585,-0.00723],currentPos.robconf,currentPos.extax];
                    MoveL targetPos,v100,z50,tool0;
                    WaitUntil \InPos,TRUE;
                    WaitTime 1;
                    gripValue := grip();
                    WaitUntil \InPos,TRUE;
                    WaitTime 1;
                    targetPos := [[150.8,677.4,300.0],[0.0168,0.67691,-0.73585,-0.00723],currentPos.robconf,currentPos.extax];
                    MoveL targetPos,v100,z50,tool0;
                    WaitUntil \InPos,TRUE;
                    WaitTime 1;
                    ok := MoveHome();
                    WaitUntil \InPos,TRUE;
                    targetPos := [[600,0,249],[0,0.70712,-0.70712,0],currentPos.robconf,currentPos.extax];
                    WaitUntil \InPos,TRUE;
                    SocketSend clientSocket\Str:="Offset";
                    SocketReceive clientSocket\Str:=data;
                    WHILE NOT data = "DONE" DO
                        ok := offset(data);
                        SocketSend clientSocket \Str:="ReadyNextMeasurement";
                        SocketReceive clientSocket\Str:=data;
                    ENDWHILE
                    SocketSend clientSocket \Str:="Done";

                CASE "Exit":
                    TPWrite "Tog emot Exit. Avslutar programmet";
                    Stop;
                    
            ENDTEST
        ENDWHILE
        
        WaitTime 1;
        
    ERROR          
        
        IF ERRNO = ERR_SOCK_TIMEOUT THEN
            RETRY;
        ELSEIF ERRNO = ERR_SOCK_CLOSED THEN
            socketClose clientSocket;
            SocketClose serverSocket;
            SocketCreate serverSocket;
            SocketBind serverSocket,ipAddr,portNmbr;
            SocketListen serverSocket;
            SocketAccept serverSocket,clientSocket,\Time:=200;
            RETRY;
        ENDIF
    ENDPROC

ENDMODULE