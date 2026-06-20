;; Capture direct data mutations via MOVE statements
(move_statement
  sending: [
    (literal)
    (identifier)
  ]
  receiving: (identifier) @mutation.target) @mutation.expr

;; Capture structural file/database modifications
(write_statement
  record: (identifier) @mutation.target) @mutation.expr

(rewrite_statement
  record: (identifier) @mutation.target) @mutation.expr

(compute_statement
  giving: (identifier) @mutation.target) @mutation.expr
