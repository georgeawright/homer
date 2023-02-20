(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet north-south-space
				      west-east-space
				      nw-se-space
				      ne-sw-space
				      peripheralness-space
				      time-space
				      temperature-space
				      height-space
				      goodness-space)
    :no_of_dimensions 1))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define comparison-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :possible_instances (StructureSet more-concept less-concept)
    :locations (list (Location (list) more-less-space))))
 
(define textual-order-sub-1-input
  (def-contextual-space :name "textual-order-sub-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define textual-order-sub-1-output
  (def-contextual-space :name "textual-order-sub-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define textual-order-sub-1
  (def-sub-frame :name "textual-order-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space textual-order-sub-1-input
    :output_space textual-order-sub-1-output))
(define textual-order-sub-2-input
  (def-contextual-space :name "textual-order-sub-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define textual-order-sub-2-output
  (def-contextual-space :name "textual-order-sub-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define textual-order-sub-2
  (def-sub-frame :name "textual-order-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space textual-order-sub-2-input
    :output_space textual-order-sub-2-output))

(define textual-order-input
  (def-contextual-space :name "textual-order.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define textual-order-output
  (def-contextual-space :name "textual-order.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define textual-order
  (def-frame :name "textual-order" :parent_concept sentence-concept :parent_frame None
    :is_secondary True
    :depth 8
    :sub_frames (StructureSet textual-order-sub-1 textual-order-sub-2)
    :concepts (StructureSet)
    :input_space textual-order-input
    :output_space textual-order-output))

(define letter-chunk-1
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) textual-order-sub-1-output)
			      (Location (list) textual-order-output))
    :parent_space textual-order-sub-1-output))
(define sub-frame-1-first-label
  (def-label :start letter-chunk-1 :parent_concept first-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) textual-order-sub-1-output))
    :is_interspatial True))
(define letter-chunk-2
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) textual-order-sub-1-output)
			      (Location (list) textual-order-output))
    :parent_space textual-order-sub-1-output))
(define sub-frame-1-last-label
  (def-label :start letter-chunk-2 :parent_concept last-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) textual-order-sub-1-output))
    :is_interspatial True))
(define letter-chunk-3
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) textual-order-sub-2-output)
			      (Location (list) textual-order-output))
    :parent_space textual-order-sub-2-output))
(define sub-frame-2-first-label
  (def-label :start letter-chunk-3 :parent_concept first-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) textual-order-sub-2-output))
    :is_interspatial True))
(define letter-chunk-4
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) textual-order-sub-2-output)
			      (Location (list) textual-order-output))
    :parent_space textual-order-sub-2-output))
(define sub-frame-2-last-label
  (def-label :start letter-chunk-4 :parent_concept last-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) textual-order-sub-2-output))
    :is_interspatial True))
(define relation-1-3
  (def-relation :start letter-chunk-1 :end letter-chunk-3 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) textual-order-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space conceptual-space))
(define relation-2-4
  (def-relation :start letter-chunk-2 :end letter-chunk-4 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) textual-order-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space conceptual-space))
(define relation-2-3
  (def-relation :start letter-chunk-2 :end letter-chunk-3 :parent_concept not-more-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) textual-order-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space conceptual-space))
((getattr (getattr textual-order "interspatial_links") "add") sub-frame-1-first-label)
((getattr (getattr textual-order "interspatial_links") "add") sub-frame-1-last-label)
((getattr (getattr textual-order "interspatial_links") "add") sub-frame-2-first-label)
((getattr (getattr textual-order "interspatial_links") "add") sub-frame-2-last-label)
((getattr (getattr textual-order "interspatial_links") "add") relation-1-3)
((getattr (getattr textual-order "interspatial_links") "add") relation-2-4)
((getattr (getattr textual-order "interspatial_links") "add") relation-2-3)

(define subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-1-output))
    :parent_space textual-order-sub-1-output))
(define subject-1-grammar-label
  (def-label :start subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) textual-order-sub-1-output))))
(define verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-1-output))
    :parent_space textual-order-sub-1-output))
(define verb-1-grammar-label
  (def-label :start verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) textual-order-sub-1-output))))
(define predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-1-output))
    :parent_space textual-order-sub-1-output))
(define predicate-1-grammar-label
  (def-label :start predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) textual-order-sub-1-output))))
(define vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-1-output))
    :left_branch (StructureSet verb-1)
    :right_branch (StructureSet predicate-1)
    :parent_space textual-order-sub-1-output))
(define vp-1-grammar-label
  (def-label :start vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) textual-order-sub-1-output))))
(define clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-1-output))
    :left_branch (StructureSet subject-1)
    :right_branch (StructureSet vp-1)
    :parent_space textual-order-sub-1-output))
(define clause-1-grammar-label
  (def-label :start clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) textual-order-sub-1-output))))

(define conj-word
  (def-letter-chunk :name "and"
    :locations (list conj-location
		     (Location (list) textual-order-output))
    :parent_space textual-order-output
    :abstract_chunk and))

(define subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-2-output))
    :parent_space textual-order-sub-2-output))
(define subject-2-grammar-label
  (def-label :start subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) textual-order-sub-2-output))))
(define verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-2-output))
    :parent_space textual-order-sub-2-output))
(define verb-2-grammar-label
  (def-label :start verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) textual-order-sub-2-output))))
(define predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-2-output))
    :parent_space textual-order-sub-2-output))
(define predicate-2-grammar-label
  (def-label :start predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) textual-order-sub-2-output))))
(define vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-2-output))
    :left_branch (StructureSet verb-2)
    :right_branch (StructureSet predicate-2)
    :parent_space textual-order-sub-2-output))
(define vp-2-grammar-label
  (def-label :start vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) textual-order-sub-2-output))))
(define clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) textual-order-output)
		     (Location (list) textual-order-sub-2-output))
    :left_branch (StructureSet subject-2)
    :right_branch (StructureSet vp-2)
    :parent_space textual-order-sub-2-output))
(define clause-2-grammar-label
  (def-label :start clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) textual-order-sub-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) textual-order-output))
    :left_branch (StructureSet conj-word)
    :right_branch (StructureSet clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) textual-order-output))
    :left_branch (StructureSet clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start same-concept :end textual-order
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end textual-order
  :is_bidirectional True :stable_activation 0.5)
