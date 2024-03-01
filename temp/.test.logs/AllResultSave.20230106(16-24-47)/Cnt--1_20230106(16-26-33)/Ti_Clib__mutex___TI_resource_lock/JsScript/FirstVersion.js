//******************************************************************************
// Copyright (c) 2021-2024. KHTC Cooperation.                                  *
// AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
// @File: FirstVersion.js.                                                     *
// @Author: @RuoDu.                                                            *
// All rights reserved.                                                        *
//******************************************************************************

// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)
var DeviceCCXMLFile = "C:/Users/dell/ti/CCSTargetConfigurations/28335_XDS100V2.ccxml";
var Core0_out = "D:/WorkSpace/CCSV7.4/AutoTool_Debug/Clib-STDC-Manu-ProgramsFolder/_mutex.h/Ti_Clib__mutex___TI_resource_lock/Debug/Ti_Clib__mutex___TI_resource_lock.out";
var script = ScriptingEnvironment.instance();
script.traceBegin("D:/WorkSpace/CCSV7.4/AutoTool_Debug/RunningResult/XML/TestLog.xml", "D:/WorkSpace/CCSV7.4/AutoTool_Debug/RunningResult/XML/DefaultStylesheet.xsl")
script.setScriptTimeout(15000)
// log set
script.traceSetConsoleLevel(TraceLevel.INFO)
script.traceSetFileLevel(TraceLevel.INFO)
var ds = script.getServer("DebugServer.1");
ds.setConfig(DeviceCCXMLFile);
ds.stop();
// open Session
Thread.sleep(500);
debugSession_0 = ds.openSession("Texas Instruments XDS100v2 USB Debug Probe_0", "C28xx")
debugSession_0.target.connect();
debugSession_0.beginCIOLogging("D:/WorkSpace/CCSV7.4/AutoTool_Debug/RunningResult/CIO/CIOFile.txt");
debugSession_0.target.getResetType(0).issueReset();

//Function: Run and get PCvalue
// *******************************************************
Thread.sleep(500);
debugSession_0.memory.loadProgram(Core0_out);
Thread.sleep(500);
debugSession_0.breakpoint.removeAll()
Thread.sleep(200);
// *******************************************************

var Right_Stop_addr = debugSession_0.symbol.getAddress("RightStop");
var right_pc = Right_Stop_addr.toString(16);
debugSession_0.breakpoint.add("RightStop");

var Error_Stop_addr = debugSession_0.symbol.getAddress("ErrorStop");
var error_pc = Error_Stop_addr.toString(16);
debugSession_0.breakpoint.add("ErrorStop");


function_test:
    do {
        var StepMode = debugSession_0.target.run();
        var PC_value = debugSession_0.memory.readRegister("PC");
        var PC = PC_value.toString(16);
        switch (PC) {
            case right_pc:
                script.traceWrite("Right_Stop_pc: 0x" + right_pc)
                break function_test;
            case error_pc:
                script.traceWrite("Error_Stop_pc: 0x" + error_pc)
                break function_test;
            default:
                continue
        }
    } while (1)

// *******************************************************
debugSession_0.breakpoint.removeAll()
var PCvalue = debugSession_0.memory.readRegister("PC");
var PC = PCvalue.toString(16);
script.traceSetConsoleLevel(TraceLevel.INFO)
script.traceWrite("StopPC: 0x" + PC)

Thread.sleep(200);

script.traceSetConsoleLevel(TraceLevel.INFO)
script.traceWrite("TEST SUCCEEDED!")
// Stop logging and exit
script.traceEnd()
debugSession_0.endCIOLogging();
debugSession_0.breakpoint.removeAll();
debugSession_0.target.disconnect();
