//
import { pythonGenerator as Python } from 'blockly/python';
/*
Python.ORDER_ATOMIC = 0;             // 0 "" ...
Python.ORDER_COLLECTION = 1;         // tuples, lists, dictionaries
Python.ORDER_STRING_CONVERSION = 1;  // `expression...`
Python.ORDER_MEMBER = 2.1;           // . []
Python.ORDER_FUNCTION_CALL = 2.2;    // ()
Python.ORDER_EXPONENTIATION = 3;     // **
Python.ORDER_UNARY_SIGN = 4;         // + -
Python.ORDER_BITWISE_NOT = 4;        // ~
Python.ORDER_MULTIPLICATIVE = 5;     // * / // %
Python.ORDER_ADDITIVE = 6;           // + -
Python.ORDER_BITWISE_SHIFT = 7;      // << >>
Python.ORDER_BITWISE_AND = 8;        // &
Python.ORDER_BITWISE_XOR = 9;        // ^
Python.ORDER_BITWISE_OR = 10;        // |
Python.ORDER_RELATIONAL = 11;        // in, not in, is, is not,
                                     //     <, <=, >, >=, <>, !=, ==
Python.ORDER_LOGICAL_NOT = 12;       // not
Python.ORDER_LOGICAL_AND = 13;       // and
Python.ORDER_LOGICAL_OR = 14;        // or
Python.ORDER_CONDITIONAL = 15;       // if else
Python.ORDER_LAMBDA = 16;            // lambda
Python.ORDER_NONE = 99;              // (...)
/**/
//
//const notImplementedMsg = 'Not implemented at this Kernel';
export function getPythonFunctions(generator) {
    var funcs = {};
    //
    funcs['text_nocrlf_print'] = function (block) {
        const msg = generator.valueToCode(block, 'TEXT', Python.ORDER_NONE) || "''";
        return 'print(' + msg + ', end = "")\n';
    };
    //
    funcs['color_hsv2rgb'] = function (block) {
        let hh = generator.valueToCode(block, 'H', Python.ORDER_NONE) || "0";
        let ss = generator.valueToCode(block, 'S', Python.ORDER_NONE) || "0.45";
        let vv = generator.valueToCode(block, 'V', Python.ORDER_NONE) || "0.65";
        hh = hh % 360;
        if (hh < 0.0)
            hh = hh + 360;
        if (ss < 0.0)
            ss = 0.0;
        else if (ss > 1.0)
            ss = 1.0;
        if (vv < 0.0)
            vv = 0.0;
        else if (vv > 1.0)
            vv = 1.0;
        let aa = vv;
        let bb = vv - vv * ss;
        let rc = 0;
        let gc = 0;
        let bc = 0;
        //
        if (hh >= 0 && hh < 60) {
            rc = aa;
            gc = (hh / 60) * (aa - bb) + bb;
            bc = bb;
        }
        else if (hh >= 60 && hh < 120) {
            rc = (120 - hh) / 60 * (aa - bb) + bb;
            gc = aa;
            bc = bb;
        }
        else if (hh >= 120 && hh < 180) {
            rc = bb;
            gc = aa;
            bc = (hh - 120) / 60 * (aa - bb) + bb;
        }
        else if (hh >= 180 && hh < 240) {
            rc = bb;
            gc = (240 - hh) / 60 * (aa - bb) + bb;
            bc = aa;
        }
        else if (hh >= 240 && hh < 300) {
            rc = (hh - 240) / 60 * (aa - bb) + bb;
            gc = bb;
            bc = aa;
        }
        else { // hh>=300 and hh<360
            rc = aa;
            gc = bb;
            bc = (360 - hh) / 50 * (aa - bb) + bb;
        }
        //
        rc = Math.trunc(rc * 255);
        gc = Math.trunc(gc * 255);
        bc = Math.trunc(bc * 255);
        //
        const rgb = '#' + rc.toString(16) + gc.toString(16) + bc.toString(16);
        const code = Python.quote_(rgb);
        return [code, Python.ORDER_FUNCTION_CALL];
    };
    //
    return funcs;
}
//# sourceMappingURL=func.js.map