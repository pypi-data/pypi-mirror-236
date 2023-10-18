//
import { dartGenerator as Dart } from 'blockly/dart';

//
export function getDartFunctions(generator) {
  var funcs = {};

//
funcs['text_nocrlf_print'] = function(block) {
  const msg = generator.valueToCode(block, 'TEXT', Dart.ORDER_NONE) || "''";
  return 'stdout.write(' + msg +');\n';
};

  //
  return funcs;
}
