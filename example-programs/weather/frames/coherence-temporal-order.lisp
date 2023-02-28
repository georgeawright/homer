(define temporal-order-sub-1-input
  (def-contextual-space :name "temporal-order-sub-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-order-sub-1-output
  (def-contextual-space :name "temporal-order-sub-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define temporal-order-sub-1
  (def-sub-frame :name "temporal-order-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space temporal-order-sub-1-input
    :output_space temporal-order-sub-1-output))
(define temporal-order-sub-2-input
  (def-contextual-space :name "temporal-order-sub-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-order-sub-2-output
  (def-contextual-space :name "temporal-order-sub-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define temporal-order-sub-2
  (def-sub-frame :name "temporal-order-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space temporal-order-sub-2-input
    :output_space temporal-order-sub-2-output))

(define temporal-order-input
  (def-contextual-space :name "temporal-order.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-order-output
  (def-contextual-space :name "temporal-order.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define temporal-order
  (def-frame :name "temporal-order" :parent_concept conjunction-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet temporal-order-sub-1 temporal-order-sub-2)
    :concepts (StructureSet)
    :input_space temporal-order-input
    :output_space temporal-order-output))

(define chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-order-sub-1-input)
			      (Location (list) temporal-order-input))
    :parent_space temporal-order-sub-1-input))
(define sub-frame-1-least-time
  (def-label :start chunk-1 :parent_concept least-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-order-sub-1-input))
    :is_interspatial True))
(define chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-order-sub-1-input)
			      (Location (list) temporal-order-input))
    :parent_space temporal-order-sub-1-input))
(define sub-frame-1-most-time
  (def-label :start chunk-2 :parent_concept most-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-order-sub-1-input))
    :is_interspatial True))
(define chunk-3
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-order-sub-2-input)
			      (Location (list) temporal-order-input))
    :parent_space temporal-order-sub-2-input))
(define sub-frame-2-least-time
  (def-label :start chunk-3 :parent_concept least-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-order-sub-2-input))
    :is_interspatial True))
(define chunk-4
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-order-sub-2-input)
			      (Location (list) temporal-order-input))
    :parent_space temporal-order-sub-2-input))
(define sub-frame-2-most-time
  (def-label :start chunk-4 :parent_concept most-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-order-sub-2-input))
    :is_interspatial True))
(define less-time-relation-1
  (def-relation :start chunk-1 :end chunk-3 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) temporal-order-input))
    :is_interspatial True
    :parent_space None
    :conceptual_space time-space))
(define less-time-relation-2
  (def-relation :start chunk-2 :end chunk-4 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) temporal-order-input))
    :is_interspatial True
    :parent_space None
    :conceptual_space time-space))
(define not-more-time-relation
  (def-relation :start chunk-2 :end chunk-3 :parent_concept not-more-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) temporal-order-input))
    :is_interspatial True
    :parent_space None
    :conceptual_space time-space))
((getattr (getattr temporal-order "interspatial_links") "add") sub-frame-1-least-time)
((getattr (getattr temporal-order "interspatial_links") "add") sub-frame-1-most-time)
((getattr (getattr temporal-order "interspatial_links") "add") sub-frame-2-least-time)
((getattr (getattr temporal-order "interspatial_links") "add") sub-frame-2-most-time)
((getattr (getattr temporal-order "interspatial_links") "add") less-time-relation-1)
((getattr (getattr temporal-order "interspatial_links") "add") less-time-relation-2)
((getattr (getattr temporal-order "interspatial_links") "add") not-more-time-relation)

(define subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-1-output))
    :parent_space temporal-order-sub-1-output))
(define subject-1-grammar-label
  (def-label :start subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) temporal-order-sub-1-output))))
(define verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-1-output))
    :parent_space temporal-order-sub-1-output))
(define verb-1-grammar-label
  (def-label :start verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) temporal-order-sub-1-output))))
(define predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-1-output))
    :parent_space temporal-order-sub-1-output))
(define predicate-1-grammar-label
  (def-label :start predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) temporal-order-sub-1-output))))
(define vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-1-output))
    :left_branch (StructureSet verb-1)
    :right_branch (StructureSet predicate-1)
    :parent_space temporal-order-sub-1-output))
(define vp-1-grammar-label
  (def-label :start vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) temporal-order-sub-1-output))))
(define clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-1-output))
    :left_branch (StructureSet subject-1)
    :right_branch (StructureSet vp-1)
    :parent_space temporal-order-sub-1-output))
(define clause-1-grammar-label
  (def-label :start clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) temporal-order-sub-1-output))))

(define conj-word
  (def-letter-chunk :name "then"
    :locations (list conj-location
		     (Location (list) temporal-order-output))
    :parent_space temporal-order-output
    :abstract_chunk then))

(define subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-2-output))
    :parent_space temporal-order-sub-2-output))
(define subject-2-grammar-label
  (def-label :start subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) temporal-order-sub-2-output))))
(define verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-2-output))
    :parent_space temporal-order-sub-2-output))
(define verb-2-grammar-label
  (def-label :start verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) temporal-order-sub-2-output))))
(define predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-2-output))
    :parent_space temporal-order-sub-2-output))
(define predicate-2-grammar-label
  (def-label :start predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) temporal-order-sub-2-output))))
(define vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-2-output))
    :left_branch (StructureSet verb-2)
    :right_branch (StructureSet predicate-2)
    :parent_space temporal-order-sub-2-output))
(define vp-2-grammar-label
  (def-label :start vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) temporal-order-sub-2-output))))
(define clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-order-output)
		     (Location (list) temporal-order-sub-2-output))
    :left_branch (StructureSet subject-2)
    :right_branch (StructureSet vp-2)
    :parent_space temporal-order-sub-2-output))
(define clause-2-grammar-label
  (def-label :start clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) temporal-order-sub-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) temporal-order-output))
    :left_branch (StructureSet conj-word)
    :right_branch (StructureSet clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-order-output))
    :left_branch (StructureSet clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start less-time-concept :end temporal-order
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end temporal-order
  :is_bidirectional True :stable_activation 0.5)
