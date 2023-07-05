(load "conceptual-spaces/oppositeness.lisp")
(load "conceptual-spaces/grammar.lisp")
(load "conceptual-spaces/negativeness.lisp")
(load "conceptual-spaces/more-less.lisp")
(load "conceptual-spaces/same-different.lisp")
(load "conceptual-spaces/magnitude.lisp")
(load "conceptual-spaces/height.lisp")
(load "conceptual-spaces/goodness.lisp")
(load "conceptual-spaces/size.lisp")
(load "conceptual-spaces/lateness.lisp")
(load "conceptual-spaces/extremeness.lisp")
(load "conceptual-spaces/temperature.lisp")
(load "conceptual-spaces/peripheralness.lisp")
(load "conceptual-spaces/location.lisp")
(load "conceptual-spaces/time.lisp")

(load "frames/ap-jj.lisp")

(load "frames/pp-inessive-time.lisp")
(load "frames/pp-between-times.lisp")

(load "frames/pp-inessive-location.lisp")
(load "frames/pp-from-to-different-locations.lisp")
(load "frames/pp-from-wards-locations.lisp")

(load "frames/s-be.lisp")
(load "frames/s-increase.lisp")
(load "frames/s-expand.lisp")
(load "frames/s-move.lisp")
(load "frames/s-spread.lisp")

(load "frames/coherence-temporal-order.lisp")
(load "frames/coherence-temporal-parallelism.lisp")
(load "frames/coherence-text-order.lisp")
(load "frames/coherence-parallelism.lisp")
(load "frames/coherence-disanalogy-1.lisp")
(load "frames/coherence-disanalogy-2.lisp")

(def-relation
  :start disanalogy-1 :end temporal-order
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start disanalogy-2 :end temporal-order
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start parallelism :end temporal-order
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start textual-order :end temporal-order
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start disanalogy-1 :end temporal-parallelism
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start disanalogy-2 :end temporal-parallelism
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start parallelism :end temporal-parallelism
  :parent_concept more-concept :conceptual_space grammar-space)
(def-relation
  :start textual-order :end temporal-parallelism
  :parent_concept more-concept :conceptual_space grammar-space)

(define input-space
  (def-contextual-space
    :name "input" :parent_concept input-concept :is_main_input True
    :conceptual_spaces (StructureSet
			temperature-space location-space time-space size-space)))
