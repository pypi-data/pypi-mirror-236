//
import { phpGenerator as PHP } from 'blockly/php';


export function getPHPFunctions(generator) {
  var funcs = {};

//
funcs['text_nocrlf_print'] = function(block) {
  const msg = generator.valueToCode(block, 'TEXT', PHP.ORDER_NONE) || "''";
  return 'print(' + msg +');\n';
};

  //
  return funcs;
}
