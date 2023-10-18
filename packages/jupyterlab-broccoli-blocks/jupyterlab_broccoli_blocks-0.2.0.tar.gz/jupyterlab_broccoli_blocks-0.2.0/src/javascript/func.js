//
import { javascriptGenerator as Js } from 'blockly/javascript';

//const notImplementedMsg = 'Not implemented at this Kernel';


export function getJsFunctions(generator) {
  var funcs = {};

//
funcs['text_print'] = function(block) {
  const msg = generator.valueToCode(block, 'TEXT', Js.ORDER_NONE) || "''";
  return 'console.log(' + msg + ');\n';
};

//
funcs['text_nocrlf_print'] = function(block) {
  const msg = generator.valueToCode(block, 'TEXT', Js.ORDER_NONE) || "''";
  return 'process.stdout.write(' + msg +');\n';
};

  //
  return funcs;
}
