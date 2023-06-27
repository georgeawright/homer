(define subject-relation-concept
  (def-concept :name "" :is_slot True :parent_space same-different-space))

(define temporal-parallelism-sub-1-input
  (def-contextual-space :name "temporal-parallelism-sub-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-parallelism-sub-1-output
  (def-contextual-space :name "temporal-parallelism-sub-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet string-space grammar-space)))
(define temporal-parallelism-sub-1
  (def-sub-frame :name "temporal-parallelism-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space temporal-parallelism-sub-1-input
    :output_space temporal-parallelism-sub-1-output))
(define temporal-parallelism-sub-2-input
  (def-contextual-space :name "temporal-parallelism-sub-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-parallelism-sub-2-output
  (def-contextual-space :name "temporal-parallelism-sub-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet string-space grammar-space)))
(define temporal-parallelism-sub-2
  (def-sub-frame :name "temporal-parallelism-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space temporal-parallelism-sub-2-input
    :output_space temporal-parallelism-sub-2-output))

(define temporal-parallelism-input
  (def-contextual-space :name "temporal-parallelism.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define temporal-parallelism-output
  (def-contextual-space :name "temporal-parallelism.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet string-space grammar-space)))
(define temporal-parallelism
  (def-frame :name "temporal-parallelism" :parent_concept conjunction-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet temporal-parallelism-sub-1 temporal-parallelism-sub-2)
    :concepts (StructureSet subject-relation-concept)
    :input_space temporal-parallelism-input
    :output_space temporal-parallelism-output))

(define chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-parallelism-sub-1-input)
			      (Location (list) temporal-parallelism-input))
    :parent_space temporal-parallelism-sub-1-input))
(define sub-frame-1-least-time
  (def-label :start chunk-1 :parent_concept least-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-parallelism-sub-1-input))
    :is_cross_view True))
(define chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-parallelism-sub-1-input)
			      (Location (list) temporal-parallelism-input))
    :parent_space temporal-parallelism-sub-1-input))
(define sub-frame-1-most-time
  (def-label :start chunk-2 :parent_concept most-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-parallelism-sub-1-input))
    :is_cross_view True))
(define chunk-3
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-parallelism-sub-2-input)
			      (Location (list) temporal-parallelism-input))
    :parent_space temporal-parallelism-sub-2-input))
(define sub-frame-2-least-time
  (def-label :start chunk-3 :parent_concept least-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-parallelism-sub-2-input))
    :is_cross_view True))
(define chunk-4
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) temporal-parallelism-sub-2-input)
			      (Location (list) temporal-parallelism-input))
    :parent_space temporal-parallelism-sub-2-input))
(define sub-frame-2-most-time
  (def-label :start chunk-4 :parent_concept most-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) temporal-parallelism-sub-2-input))
    :is_cross_view True))
(define same-time-relation-1
  (def-relation :start chunk-1 :end chunk-3 :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) temporal-parallelism-input))
    :is_cross_view True
    :parent_space None
    :conceptual_space time-space))
(define same-time-relation-2
  (def-relation :start chunk-2 :end chunk-4 :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) temporal-parallelism-input))
    :is_cross_view True
    :parent_space None
    :conceptual_space time-space))

(define subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-1-output))
    :parent_space temporal-parallelism-sub-1-output))
(define subject-1-grammar-label
  (def-label :start subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) temporal-parallelism-sub-1-output))
    :is_cross_view True))
(define subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-2-output))
    :parent_space temporal-parallelism-sub-2-output))
(define subject-2-grammar-label
  (def-label :start subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) temporal-parallelism-sub-2-output))
    :is_cross_view True))
(define subject-relation
  (def-relation :start subject-1 :end subject-2 :parent_concept subject-relation-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) string-space)
		     (TwoPointLocation (list) (list) temporal-parallelism-output))
    :is_cross_view True
    :parent_space None
    :conceptual_space string-space))

((getattr (getattr temporal-parallelism "cross_view_links") "add") sub-frame-1-least-time)
((getattr (getattr temporal-parallelism "cross_view_links") "add") sub-frame-1-most-time)
((getattr (getattr temporal-parallelism "cross_view_links") "add") sub-frame-2-least-time)
((getattr (getattr temporal-parallelism "cross_view_links") "add") sub-frame-2-most-time)
((getattr (getattr temporal-parallelism "cross_view_links") "add") same-time-relation-1)
((getattr (getattr temporal-parallelism "cross_view_links") "add") same-time-relation-2)
((getattr (getattr temporal-parallelism "cross_view_links") "add") subject-1-grammar-label)
((getattr (getattr temporal-parallelism "cross_view_links") "add") subject-2-grammar-label)
((getattr (getattr temporal-parallelism "cross_view_links") "add") subject-relation)

(define verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-1-output))
    :parent_space temporal-parallelism-sub-1-output))
(define verb-1-grammar-label
  (def-label :start verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) temporal-parallelism-sub-1-output))))
(define predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-1-output))
    :parent_space temporal-parallelism-sub-1-output))
(define predicate-1-grammar-label
  (def-label :start predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) temporal-parallelism-sub-1-output))))
(define vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-1-output))
    :left_branch (StructureSet verb-1)
    :right_branch (StructureSet predicate-1)
    :parent_space temporal-parallelism-sub-1-output))
(define vp-1-grammar-label
  (def-label :start vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) temporal-parallelism-sub-1-output))))
(define clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-1-output))
    :left_branch (StructureSet subject-1)
    :right_branch (StructureSet vp-1)
    :parent_space temporal-parallelism-sub-1-output))
(define clause-1-grammar-label
  (def-label :start clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) temporal-parallelism-sub-1-output))))

(define conj-word
  (def-letter-chunk :name "meanwhile"
    :locations (list conj-location
		     (Location (list) temporal-parallelism-output))
    :parent_space temporal-parallelism-output
    :abstract_chunk meanwhile))

(define verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-2-output))
    :parent_space temporal-parallelism-sub-2-output))
(define verb-2-grammar-label
  (def-label :start verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) temporal-parallelism-sub-2-output))))
(define predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-2-output))
    :parent_space temporal-parallelism-sub-2-output))
(define predicate-2-grammar-label
  (def-label :start predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) temporal-parallelism-sub-2-output))))
(define vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-2-output))
    :left_branch (StructureSet verb-2)
    :right_branch (StructureSet predicate-2)
    :parent_space temporal-parallelism-sub-2-output))
(define vp-2-grammar-label
  (def-label :start vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) temporal-parallelism-sub-2-output))))
(define clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-parallelism-output)
		     (Location (list) temporal-parallelism-sub-2-output))
    :left_branch (StructureSet subject-2)
    :right_branch (StructureSet vp-2)
    :parent_space temporal-parallelism-sub-2-output))
(define clause-2-grammar-label
  (def-label :start clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) temporal-parallelism-sub-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) temporal-parallelism-output))
    :left_branch (StructureSet conj-word)
    :right_branch (StructureSet clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) temporal-parallelism-output))
    :left_branch (StructureSet clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start same-time-cross_view-concept :end temporal-parallelism
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end temporal-parallelism
  :is_bidirectional True :stable_activation 0.5)
