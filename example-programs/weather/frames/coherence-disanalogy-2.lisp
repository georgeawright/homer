(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet location-space
				      time-space
				      temperature-space
				      height-space
				      goodness-space)
    :no_of_dimensions Nan))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define comparison-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :possible_instances (StructureSet more-concept less-concept)
    :locations (list (Location (list) more-less-space))))
 
(define disanalogy-2-sub-1-input
  (def-contextual-space :name "disanalogy-2-sub-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define disanalogy-2-sub-1-output
  (def-contextual-space :name "disanalogy-2-sub-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define disanalogy-2-sub-1
  (def-sub-frame :name "disanalogy-2-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space disanalogy-2-sub-1-input
    :output_space disanalogy-2-sub-1-output))
(define disanalogy-2-sub-2-input
  (def-contextual-space :name "disanalogy-2-sub-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define disanalogy-2-sub-2-output
  (def-contextual-space :name "disanalogy-2-sub-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define disanalogy-2-sub-2
  (def-sub-frame :name "disanalogy-2-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space disanalogy-2-sub-2-input
    :output_space disanalogy-2-sub-2-output))

(define disanalogy-2-input
  (def-contextual-space :name "disanalogy-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define disanalogy-2-output
  (def-contextual-space :name "disanalogy-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define disanalogy-2
  (def-frame :name "disanalogy-2" :parent_concept conjunction-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet disanalogy-2-sub-1 disanalogy-2-sub-2)
    :concepts (StructureSet)
    :input_space disanalogy-2-input
    :output_space disanalogy-2-output))

(define verb-1
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list (list Nan)) verb-space)
		     (Location (list) disanalogy-2-sub-1-output)
		     (Location (list) disanalogy-2-output))
    :parent_space disanalogy-2-sub-1-output))
(define verb-1-label
  (def-label :start verb-1 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) disanalogy-2-sub-1-output))
    :is_interspatial True))
(define verb-2
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list (list Nan)) verb-space)
		     (Location (list) disanalogy-2-sub-2-output)
		     (Location (list) disanalogy-2-output))
    :parent_space disanalogy-2-sub-2-output))
(define verb-2-label
  (def-label :start verb-2 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) disanalogy-2-sub-2-output))
    :is_interspatial True))
(define verbs-relation
  (def-relation :start verb-1 :end verb-2 :parent_concept opposite-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) oppositeness-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) verb-space)
		     (TwoPointLocation (list) (list) disanalogy-2-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space verb-space))
((getattr (getattr disanalogy-2 "interspatial_links") "add") verb-1-label)
((getattr (getattr disanalogy-2 "interspatial_links") "add") verb-2-label)
((getattr (getattr disanalogy-2 "interspatial_links") "add") verbs-relation)

(define subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-1-output))
    :parent_space disanalogy-2-sub-1-output))
(define subject-1-grammar-label
  (def-label :start subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) disanalogy-2-sub-1-output))))
(define verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-1-output))
    :parent_space disanalogy-2-sub-1-output))
(define verb-1-grammar-label
  (def-label :start verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) disanalogy-2-sub-1-output))))
(define predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-1-output))
    :parent_space disanalogy-2-sub-1-output))
(define predicate-1-grammar-label
  (def-label :start predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) disanalogy-2-sub-1-output))))
(define vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-1-output))
    :left_branch (StructureSet verb-1)
    :right_branch (StructureSet predicate-1)
    :parent_space disanalogy-2-sub-1-output))
(define vp-1-grammar-label
  (def-label :start vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) disanalogy-2-sub-1-output))))
(define clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-1-output))
    :left_branch (StructureSet subject-1)
    :right_branch (StructureSet vp-1)
    :parent_space disanalogy-2-sub-1-output))
(define clause-1-grammar-label
  (def-label :start clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) disanalogy-2-sub-1-output))))

(define conj-word
  (def-letter-chunk :name "but"
    :locations (list conj-location
		     (Location (list) disanalogy-2-output))
    :parent_space disanalogy-2-output
    :abstract_chunk but))

(define subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-2-output))
    :parent_space disanalogy-2-sub-2-output))
(define subject-2-grammar-label
  (def-label :start subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) disanalogy-2-sub-2-output))))
(define verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-2-output))
    :parent_space disanalogy-2-sub-2-output))
(define verb-2-grammar-label
  (def-label :start verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) disanalogy-2-sub-2-output))))
(define predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-2-output))
    :parent_space disanalogy-2-sub-2-output))
(define predicate-2-grammar-label
  (def-label :start predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) disanalogy-2-sub-2-output))))
(define vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-2-output))
    :left_branch (StructureSet verb-2)
    :right_branch (StructureSet predicate-2)
    :parent_space disanalogy-2-sub-2-output))
(define vp-2-grammar-label
  (def-label :start vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) disanalogy-2-sub-2-output))))
(define clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) disanalogy-2-output)
		     (Location (list) disanalogy-2-sub-2-output))
    :left_branch (StructureSet subject-2)
    :right_branch (StructureSet vp-2)
    :parent_space disanalogy-2-sub-2-output))
(define clause-2-grammar-label
  (def-label :start clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) disanalogy-2-sub-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) disanalogy-2-output))
    :left_branch (StructureSet conj-word)
    :right_branch (StructureSet clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) disanalogy-2-output))
    :left_branch (StructureSet clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start opposite-interspatial-concept :end disanalogy-2
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end disanalogy-2
  :is_bidirectional True :stable_activation 0.5)


