(var fib
  (function (n)
    (loop (a b count) (1 0 n)
      (if (= count 0)
        b
        (recur (+ a b) a (- count 1))))))
    
(console.log (fib 10))