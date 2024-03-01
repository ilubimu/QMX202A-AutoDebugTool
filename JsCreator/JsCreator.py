# ******************************************************************************
#  Copyright (c) 2021-2024. KHTC Cooperation.                                  *
#  AUTOMATED INCENTIVE GENERATION TOOLS.                                       *
#  @File: JsCreator.py.                                                        *
#  @Author: @RuoDu.                                                            *
#  All rights reserved.                                                        *
# ******************************************************************************

import copy
import Monitor
import typing


# === Abstract Builder
class JsBuilder:
    def emulator_init(self, emulator_params_dict):
        raise NotImplementedError

    def function(self, function_params_dict):
        raise NotImplementedError

    def end_process(self, end_params_dict):
        raise NotImplementedError

    def __repr__(self):
        return "check all step"


# === 1: LoadExport
class LoadExport(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        time_sleep = emulator_params_dict['time_sleep']
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        running_ctrl = emulator_params_dict['running_ctrl']
        session_config = emulator_params_dict["session_config"].replace("\\", "/")
        emulator_context = '''
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)

// Main variable
var script = ScriptingEnvironment.instance();

// Main flow
try {{
    var DeviceCCXMLFile = "{0}";
    var Core0_out = "replace::out_file";
    script.traceBegin("replace::xml_path/TestLog.xml", "replace::xml_path/DefaultStylesheet.xsl");
    script.setScriptTimeout({1});
    // log set
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceSetFileLevel(TraceLevel.INFO);
    var ds = script.getServer( "DebugServer.1" );
    ds.setConfig( DeviceCCXMLFile );
    ds.stop();
    // open Session
    Thread.sleep({2});
    var debugSession_0 = {3};  // support for openSession("*", "*")
    debugSession_0.target.connect();
    debugSession_0.beginCIOLogging("replace::cio_file");
    // debugSession_0.target.getResetType({4}).issueReset();  // could do some other supported reset
    debugSession_0.target.reset();
'''.format(ccxml_file, running_ctrl['Timeout'], time_sleep, session_config, running_ctrl['Reset'])
        return emulator_context

    def function(self, function_params_dict):
        time_sleep = function_params_dict['time_sleep']
        running_ctrl = function_params_dict['running_ctrl']
        running_stop_flag = copy.deepcopy(function_params_dict['running_stop_flag'])

        memory_save_list = function_params_dict['memory_save']
        memory_result_folder = function_params_dict['result_folder'].replace('\\', '/')
        __memory_save_frame = 'debugSession_0.memory.saveData2({0}, 0, {1}, "{2}/{3}.dat", 15, false);'
        _memory_save_context = '\n\t'.join([__memory_save_frame.format(
            x['StartAddress'], x['AddressLength'], memory_result_folder, x['Name'])
            for x in memory_save_list])

        __breakpoint_add_frame = '''
    var {0} = debugSession_0.symbol.getAddress("{1}");
    var {2} = {0}.toString(16);
    debugSession_0.breakpoint.add("{1}");
'''
        __right_stop_break = __breakpoint_add_frame.format(
            'Right_Stop_addr', running_stop_flag.pop('RightStop_flag'), 'right_pc')
        __error_stop_break = __breakpoint_add_frame.format(
            'Error_Stop_addr', running_stop_flag.pop('ErrorStop_flag'), 'error_pc')
        __other_stop_break = '\n\t'.join([__breakpoint_add_frame.format(
            '{}_addr'.format(key), value, key) for key, value in running_stop_flag.items()])
        _breakpoint_add_context = __right_stop_break + __error_stop_break + __other_stop_break

        function_context = '''
    //Function: Run and get PCvalue
    // *******************************************************
    Thread.sleep({0});
    debugSession_0.memory.loadProgram( Core0_out );
    Thread.sleep({0});
    debugSession_0.breakpoint.removeAll();
    {1}
    Thread.sleep(200);
    // *******************************************************
    {2}
    // *******************************************************
    debugSession_0.breakpoint.removeAll();
    replace::reserve_save_text
    Thread.sleep(200);
'''.format(time_sleep, _memory_save_context, _breakpoint_add_context)
        return function_context

    def end_process(self, end_params_dict):
        end_context = '''
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("TEST SUCCEEDED!");
    // Stop logging and exit
    debugSession_0.endCIOLogging();
    debugSession_0.breakpoint.removeAll();
    debugSession_0.target.disconnect();
}
catch (ex) {
    script.traceWrite(ex);
    script.traceWrite("JS file runtime error");
}
finally {
    script.traceEnd();
    quit();
}
'''
        return end_context


# === 2: LoadRun
class LoadRun(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        time_sleep = emulator_params_dict['time_sleep']
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        running_ctrl = emulator_params_dict['running_ctrl']
        session_config = emulator_params_dict["session_config"].replace("\\", "/")
        emulator_context = '''
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)

// Main variable
var script = ScriptingEnvironment.instance();

// Main flow
try {{
    var DeviceCCXMLFile = "{0}";
    var Core0_out = "replace::out_file";
    script.traceBegin("replace::xml_path/TestLog.xml", "replace::xml_path/DefaultStylesheet.xsl");
    script.setScriptTimeout({1});
    // log set
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceSetFileLevel(TraceLevel.INFO);
    var ds = script.getServer( "DebugServer.1" );
    ds.setConfig( DeviceCCXMLFile );
    ds.stop();
    // open Session
    Thread.sleep({2});
    debugSession_0 = {3};  // support for openSession("*", "*")
    debugSession_0.target.connect();
    debugSession_0.beginCIOLogging("replace::cio_file");
    // debugSession_0.target.getResetType({4}).issueReset();  // could do some other supported reset
    debugSession_0.target.reset();
'''.format(ccxml_file, running_ctrl['Timeout'], time_sleep, session_config, running_ctrl['Reset'])
        return emulator_context

    def function(self, function_params_dict):
        time_sleep = function_params_dict['time_sleep']
        running_ctrl = function_params_dict['running_ctrl']
        running_stop_flag = copy.deepcopy(function_params_dict['running_stop_flag'])

        __breakpoint_add_frame = '''
    var {0} = debugSession_0.symbol.getAddress("{1}");
    var {2} = {0}.toString(16);
    debugSession_0.breakpoint.add("{1}");
'''
        __right_stop_break = __breakpoint_add_frame.format(
            'Right_Stop_addr', running_stop_flag.pop('RightStop_flag'), 'right_pc')
        __error_stop_break = __breakpoint_add_frame.format(
            'Error_Stop_addr', running_stop_flag.pop('ErrorStop_flag'), 'error_pc')
        __other_stop_break = '\n\t'.join([__breakpoint_add_frame.format(
            '{}_addr'.format(key), value, key) for key, value in running_stop_flag.items()])
        _breakpoint_add_context = __right_stop_break + __error_stop_break + __other_stop_break

        _running_mode = 'var StepMode = debugSession_0.target.{}();'.format(running_ctrl['RunningMode'].lower())

        function_context = '''
    //Function: Run and get PCvalue
    // *******************************************************
    Thread.sleep({0});
    debugSession_0.memory.loadProgram( Core0_out );
    Thread.sleep({0});
    debugSession_0.breakpoint.removeAll();
    Thread.sleep(200);
    // *******************************************************
    {1}
    
    function_test:
        do {{
            {2}
            var PC_value = debugSession_0.memory.readRegister("PC");
            var PC = PC_value.toString(16);
            switch(PC) {{
                case right_pc:
                    script.traceWrite("Right_Stop_pc: 0x" + right_pc);
                    break function_test;
                case error_pc:
                    script.traceWrite("Error_Stop_pc: 0x" + error_pc);
                    break function_test;
                default:
                    continue
            }}
        }} while(1)
    
    // *******************************************************
    debugSession_0.breakpoint.removeAll();
    var PCvalue = debugSession_0.memory.readRegister("PC");
    var PC = PCvalue.toString(16);
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("StopPC: 0x" + PC);
    replace::reserve_save_text
    Thread.sleep(200);
'''.format(time_sleep, _breakpoint_add_context, _running_mode)
        return function_context

    def end_process(self, end_params_dict):
        end_context = '''
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("TEST SUCCEEDED!");
    // Stop logging and exit
    debugSession_0.endCIOLogging();
    debugSession_0.breakpoint.removeAll();
    debugSession_0.target.disconnect();
}
catch (ex) {
    script.traceWrite(ex);
    script.traceWrite("JS file runtime error");
}
finally {
    script.traceEnd();
    quit();
}
'''
        return end_context


# === 3: LoadExportRun
class LoadExportRun(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        time_sleep = emulator_params_dict['time_sleep']
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        running_ctrl = emulator_params_dict['running_ctrl']
        session_config = emulator_params_dict["session_config"].replace("\\", "/")
        emulator_context = '''
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)

// Main variable
var script = ScriptingEnvironment.instance();

// Main flow
try {{
    var DeviceCCXMLFile = "{0}";
    var Core0_out = "replace::out_file";
    script.traceBegin("replace::xml_path/TestLog.xml", "replace::xml_path/DefaultStylesheet.xsl");
    script.setScriptTimeout({1});
    // log set
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceSetFileLevel(TraceLevel.INFO);
    var ds = script.getServer( "DebugServer.1" );
    ds.setConfig( DeviceCCXMLFile );
    ds.stop();
    // open Session
    Thread.sleep({2});
    debugSession_0 = {3};  // support for openSession("*", "*")
    debugSession_0.target.connect();
    debugSession_0.beginCIOLogging("replace::cio_file");
    // debugSession_0.target.getResetType({4}).issueReset();  // could do some other supported reset
    debugSession_0.target.reset();
'''.format(ccxml_file, running_ctrl['Timeout'], time_sleep, session_config, running_ctrl['Reset'])
        return emulator_context

    def function(self, function_params_dict):
        time_sleep = function_params_dict['time_sleep']
        running_ctrl = function_params_dict['running_ctrl']
        running_stop_flag = copy.deepcopy(function_params_dict['running_stop_flag'])

        memory_save_list = function_params_dict['memory_save']
        memory_result_folder = function_params_dict['result_folder'].replace('\\', '/')
        __memory_save_frame = 'debugSession_0.memory.saveData2({0}, 0, {1}, "{2}/{3}.dat", 15, false);'
        _memory_save_context = '\n\t'.join([__memory_save_frame.format(
            x['StartAddress'], x['AddressLength'], memory_result_folder, x['Name'])
            for x in memory_save_list])

        __breakpoint_add_frame = '''
    var {0} = debugSession_0.symbol.getAddress("{1}");
    var {2} = {0}.toString(16);
    debugSession_0.breakpoint.add("{1}");
'''
        __right_stop_break = __breakpoint_add_frame.format(
            'Right_Stop_addr', running_stop_flag.pop('RightStop_flag'), 'right_pc')
        __error_stop_break = __breakpoint_add_frame.format(
            'Error_Stop_addr', running_stop_flag.pop('ErrorStop_flag'), 'error_pc')
        __other_stop_break = '\n\t'.join([__breakpoint_add_frame.format(
            '{}_addr'.format(key), value, key) for key, value in running_stop_flag.items()])
        _breakpoint_add_context = __right_stop_break + __error_stop_break + __other_stop_break

        _running_mode = 'var StepMode = debugSession_0.target.{}();'.format(running_ctrl['RunningMode'].lower())

        function_context = '''
    //Function: Run and get PCvalue
    // *******************************************************
    Thread.sleep({0});
    debugSession_0.memory.loadProgram( Core0_out );
    Thread.sleep({0});
    debugSession_0.breakpoint.removeAll();
    {1}
    Thread.sleep(200);
    // *******************************************************
    {2}
    
    function_test:
        do {{
            {3}
            var PC_value = debugSession_0.memory.readRegister("PC");
            var PC = PC_value.toString(16);
            switch(PC) {{
                case right_pc:
                    script.traceWrite("Right_Stop_pc: 0x" + right_pc);
                    break function_test;
                case error_pc:
                    script.traceWrite("Error_Stop_pc: 0x" + error_pc);
                    break function_test;
                default:
                    continue
            }}
        }} while(1)
    
    // *******************************************************
    debugSession_0.breakpoint.removeAll();
    var PCvalue = debugSession_0.memory.readRegister("PC");
    var PC = PCvalue.toString(16);
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("StopPC: 0x" + PC);
    replace::reserve_save_text
    Thread.sleep(200);
'''.format(time_sleep, _memory_save_context, _breakpoint_add_context, _running_mode)
        return function_context

    def end_process(self, end_params_dict):
        end_context = '''
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("TEST SUCCEEDED!");
    // Stop logging and exit
    debugSession_0.endCIOLogging();
    debugSession_0.breakpoint.removeAll();
    debugSession_0.target.disconnect();
}
catch (ex) {
    script.traceWrite(ex);
    script.traceWrite("JS file runtime error");
}
finally {
    script.traceEnd();
    quit();
}
'''
        return end_context


# === 4: LoadRunExport
class LoadRunExport(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        time_sleep = emulator_params_dict['time_sleep']
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        running_ctrl = emulator_params_dict['running_ctrl']
        session_config = emulator_params_dict["session_config"].replace("\\", "/")
        emulator_context = '''
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)

// Main variable
var script = ScriptingEnvironment.instance();

// Main flow
try {{
    var DeviceCCXMLFile = "{0}";
    var Core0_out = "replace::out_file";
    script.traceBegin("replace::xml_path/TestLog.xml", "replace::xml_path/DefaultStylesheet.xsl");
    script.setScriptTimeout({1});
    // log set
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceSetFileLevel(TraceLevel.INFO);
    var ds = script.getServer( "DebugServer.1" );
    ds.setConfig( DeviceCCXMLFile );
    ds.stop();
    // open Session
    Thread.sleep({2});
    debugSession_0 = {3};  // support for openSession("*", "*")
    debugSession_0.target.connect();
    debugSession_0.beginCIOLogging("replace::cio_file");
    // debugSession_0.target.getResetType({4}).issueReset();  // could do some other supported reset
    debugSession_0.target.reset();
'''.format(ccxml_file, running_ctrl['Timeout'], time_sleep, session_config, running_ctrl['Reset'])
        return emulator_context

    def function(self, function_params_dict):
        time_sleep = function_params_dict['time_sleep']
        running_ctrl = function_params_dict['running_ctrl']
        running_stop_flag = copy.deepcopy(function_params_dict['running_stop_flag'])

        memory_save_list = function_params_dict['memory_save']
        memory_result_folder = function_params_dict['result_folder'].replace('\\', '/')
        __memory_save_frame = 'debugSession_0.memory.saveData2({0}, 0, {1}, "{2}/{3}.dat", 15, false);'
        _memory_save_context = '\n\t'.join([__memory_save_frame.format(
            x['StartAddress'], x['AddressLength'], memory_result_folder, x['Name'])
            for x in memory_save_list])

        __breakpoint_add_frame = '''
    var {0} = debugSession_0.symbol.getAddress("{1}");
    var {2} = {0}.toString(16);
    debugSession_0.breakpoint.add("{1}");
'''
        __right_stop_break = __breakpoint_add_frame.format(
            'Right_Stop_addr', running_stop_flag.pop('RightStop_flag'), 'right_pc')
        __error_stop_break = __breakpoint_add_frame.format(
            'Error_Stop_addr', running_stop_flag.pop('ErrorStop_flag'), 'error_pc')
        __other_stop_break = '\n\t'.join([__breakpoint_add_frame.format(
            '{}_addr'.format(key), value, key) for key, value in running_stop_flag.items()])
        _breakpoint_add_context = __right_stop_break + __error_stop_break + __other_stop_break

        _running_mode = 'var StepMode = debugSession_0.target.{}();'.format(running_ctrl['RunningMode'].lower())

        function_context = '''
    //Function: Run and get PCvalue
    // *******************************************************
    Thread.sleep({0});
    debugSession_0.memory.loadProgram( Core0_out );
    Thread.sleep({0});
    debugSession_0.breakpoint.removeAll();
    // *******************************************************
    {1}
    
    function_test:
        do {{
            {2}
            var PC_value = debugSession_0.memory.readRegister("PC");
            var PC = PC_value.toString(16);
            switch(PC) {{
                case right_pc:
                    script.traceWrite("Right_Stop_pc: 0x" + right_pc);
                    break function_test;
                case error_pc:
                    script.traceWrite("Error_Stop_pc: 0x" + error_pc);
                    break function_test;
                default:
                    continue
            }}
        }} while(1)
    
    // *******************************************************
    {3}
    Thread.sleep(200);
    // *******************************************************
    debugSession_0.breakpoint.removeAll();
    var PCvalue = debugSession_0.memory.readRegister("PC");
    var PC = PCvalue.toString(16);
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("StopPC: 0x" + PC);
    replace::reserve_save_text
    Thread.sleep(200);
'''.format(time_sleep, _breakpoint_add_context, _running_mode, _memory_save_context)
        return function_context

    def end_process(self, end_params_dict):
        end_context = '''
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("TEST SUCCEEDED!");
    // Stop logging and exit
    debugSession_0.endCIOLogging();
    debugSession_0.breakpoint.removeAll();
    debugSession_0.target.disconnect();
}
catch (ex) {
    script.traceWrite(ex);
    script.traceWrite("JS file runtime error");
}
finally {
    script.traceEnd();
    quit();
}
'''
        return end_context


# for connect function test
class ConnectiontVerify(JsBuilder):
    def emulator_init(self, emulator_params_dict):
        time_sleep = emulator_params_dict['time_sleep']
        ccxml_file = emulator_params_dict["ccxml_file"].replace("\\", "/")
        running_ctrl = emulator_params_dict['running_ctrl']
        session_config = emulator_params_dict["session_config"].replace("\\", "/")
        emulator_context = '''
// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting)
importPackage(Packages.com.ti.ccstudio.scripting.environment)
importPackage(Packages.java.lang)

// Main variable
var script = ScriptingEnvironment.instance();

// Main flow
try {{
    var DeviceCCXMLFile = "{0}";
    script.traceBegin("replace::xml_path/TestLog.xml", "replace::xml_path/DefaultStylesheet.xsl");
    script.setScriptTimeout({1});
    // log set
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceSetFileLevel(TraceLevel.INFO);
    var ds = script.getServer( "DebugServer.1" );
    ds.setConfig( DeviceCCXMLFile );
    ds.stop();
    // open Session
    Thread.sleep({2});
    debugSession_0 = {3};  // support for openSession("*", "*")
    debugSession_0.target.connect();
    debugSession_0.beginCIOLogging("replace::cio_file");
    // debugSession_0.target.getResetType({4}).issueReset();  // could do some other supported reset
    debugSession_0.target.reset();
'''.format(ccxml_file, running_ctrl['Timeout'], time_sleep, session_config, running_ctrl['Reset'])
        return emulator_context

    def function(self, function_params_dict):
        memory_save_list = function_params_dict['memory_save']
        memory_result_folder = function_params_dict['result_folder'].replace('\\', '/')
        __memory_save_frame = 'debugSession_0.memory.saveData2({0}, 0, {1}, "{2}/{3}.dat", 15, false);'
        _memory_save_context = '\n\t'.join([__memory_save_frame.format(
            x['StartAddress'], x['AddressLength'], memory_result_folder, x['Name'])
            for x in memory_save_list])

        function_context = '''
    // *******************************************************
    {0}
    Thread.sleep(200);
    // *******************************************************
    debugSession_0.breakpoint.removeAll();
    var PCvalue = debugSession_0.memory.readRegister("PC");
    var PC = PCvalue.toString(16);
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("Right_Stop_pc: 0x" + PC)
    replace::reserve_save_text
    Thread.sleep(200);
'''.format(_memory_save_context)
        return function_context

    def end_process(self, end_params_dict):
        end_context = '''
    script.traceSetConsoleLevel(TraceLevel.INFO);
    script.traceWrite("TEST SUCCEEDED!");
    // Stop logging and exit
    debugSession_0.endCIOLogging();
    debugSession_0.breakpoint.removeAll();
    debugSession_0.target.disconnect();
}
catch (ex) {
    script.traceWrite(ex);
    script.traceWrite("JS file runtime error");
}
finally {
    script.traceEnd();
    quit();
}
'''
        return end_context


class RunningModeArch:
    Str_or_Int = typing.TypeVar('Str_or_Int', str, int)

    def __init__(self, mode: Str_or_Int):
        # 参数
        self.__mode__ = str(mode)
        self.__arch_mode = None
        # 赋值
        self.__mode_set()

    def __repr__(self):
        """ 直接打印或输出时执行返回 """
        return self.__mode__

    def __mode_set(self):
        _base_mode_config = {
            '-1': 'ConnectiontVerify',
            '1': 'LoadExportRun',
            '2': 'LoadExport',
            '3': 'LoadRun',
            '4': 'LoadRunExport'
        }
        _mode_num_set, _mode_set = zip(*_base_mode_config.items())
        if self.__mode__ in _mode_set:  # value
            pass
        elif self.__mode__ in _mode_num_set:  # key
            self.__mode__ = _base_mode_config[self.__mode__]
        else:
            _err_inf = "Running mode set error, " \
                       "only for 'LoadExportRun(1), LoadExport(2), LoadRun(3), LoadRunExport(4)'"
            raise Monitor.UserException.RunningModeError(_err_inf)
        self.__arch_mode = eval(self.__mode__)

    def mode_cls(self):
        return self.__arch_mode

    def mode_name(self):
        return self.__repr__()
