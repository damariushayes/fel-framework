;; Isolate direct assignments to global state or configuration objects
(assignment_expression
  left: [
    (identifier) @mutation.target (#match? @mutation.target "(STATE|GLOBAL|CONFIG|DB)")
    (field_expression argument: (identifier) field: (field_identifier) @mutation.target)
  ]
  operator: "=") @mutation.expr

;; Track raw memory mutations and buffer manipulations
(call_expression
  function: (identifier) @call.target (#match? @call.target "(memcpy|memset|memmove|strcpy|strcat)")
  arguments: (argument_list) @mutation.args) @mutation.expr

;; Isolate inline assembly injections executing direct hardware/OS mutations
(asm_statement) @mutation.asm
