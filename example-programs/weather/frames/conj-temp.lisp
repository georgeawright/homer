(define conj-temp-sub-frame-1-input
  (def-contextual-space :name "conj-temp-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-temp-sub-frame-1-output
  (def-contextual-space :name "conj-temp-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-temp-sub-frame-1
  (def-sub-frame :name "conj-temp-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conj-temp-sub-frame-1-input
    :output_space conj-temp-sub-frame-1-output))
(define conj-temp-sub-frame-2-input
  (def-contextual-space :name "conj-temp-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-temp-sub-frame-2-output
  (def-contextual-space :name "conj-temp-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-temp-sub-frame-2
  (def-sub-frame :name "conj-temp-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conj-temp-sub-frame-2-input
    :output_space conj-temp-sub-frame-2-output))

(define conj-temp-sentence-input
  (def-contextual-space :name "conj-temp.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-temp-sentence-output
  (def-contextual-space :name "conj-temp.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-temp-sentence
  (def-frame :name "conj-temp" :parent_concept sentence-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet conj-temp-sub-frame-1 conj-temp-sub-frame-2)
    :concepts (StructureSet)
    :input_space conj-temp-sentence-input
    :output_space conj-temp-sentence-output))

(define chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) conj-temp-sub-frame-1-input)
			      (Location (list) conj-temp-sentence-input))
    :parent_space conj-temp-sub-frame-1-input))
(define chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) conj-temp-sub-frame-1-input)
			      (Location (list) conj-temp-sentence-input))
    :parent_space conj-temp-sub-frame-1-input))
(define chunk-3
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) conj-temp-sub-frame-2-input)
			      (Location (list) conj-temp-sentence-input))
    :parent_space conj-temp-sub-frame-2-input))
(define chunk-4
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) conj-temp-sub-frame-2-input)
			      (Location (list) conj-temp-sentence-input))
    :parent_space conj-temp-sub-frame-2-input))
(define less-time-relation-1
  (def-relation :start chunk-1 :end chunk-3 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) conj-temp-sentence-input))
    :is_interspatial_relation True
    :parent_space None
    :conceptual_space time-space))
(define less-time-relation-2
  (def-relation :start chunk-2 :end chunk-4 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) conj-temp-sentence-input))
    :is_interspatial_relation True
    :parent_space None
    :conceptual_space time-space))
(define not-more-time-relation
  (def-relation :start chunk-2 :end chunk-3 :parent_concept not-more-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) conj-temp-sentence-input))
    :is_interspatial_relation True
    :parent_space None
    :conceptual_space time-space))
((getattr (getattr conj-temp-sentence "interspatial_relations") "add") less-time-relation-1)
((getattr (getattr conj-temp-sentence "interspatial_relations") "add") less-time-relation-2)
((getattr (getattr conj-temp-sentence "interspatial_relations") "add") not-more-time-relation)
(setattr conj-temp-sentence "early_chunk" chunk-1)
(setattr conj-temp-sentence "late_chunk" chunk-4)
(setattr conj-temp-sub-frame-1 "early_chunk" chunk-1)
(setattr conj-temp-sub-frame-1 "late_chunk" chunk-2)
(setattr conj-temp-sub-frame-2 "early_chunk" chunk-3)
(setattr conj-temp-sub-frame-2 "late_chunk" chunk-4)

(define conj-temp-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-1-output))
    :parent_space conj-temp-sub-frame-1-output))
(define conj-temp-subject-1-grammar-label
  (def-label :start conj-temp-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conj-temp-sub-frame-1-output))))
(define conj-temp-verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-1-output))
    :parent_space conj-temp-sub-frame-1-output))
(define conj-temp-verb-1-grammar-label
  (def-label :start conj-temp-verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conj-temp-sub-frame-1-output))))
(define conj-temp-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-1-output))
    :parent_space conj-temp-sub-frame-1-output))
(define conj-temp-predicate-1-grammar-label
  (def-label :start conj-temp-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conj-temp-sub-frame-1-output))))
(define conj-temp-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-1-output))
    :left_branch (StructureSet conj-temp-verb-1)
    :right_branch (StructureSet conj-temp-predicate-1)
    :parent_space conj-temp-sub-frame-1-output))
(define conj-temp-vp-1-grammar-label
  (def-label :start conj-temp-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conj-temp-sub-frame-1-output))))
(define conj-temp-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-1-output))
    :left_branch (StructureSet conj-temp-subject-1)
    :right_branch (StructureSet conj-temp-vp-1)
    :parent_space conj-temp-sub-frame-1-output))
(define conj-temp-clause-1-grammar-label
  (def-label :start conj-temp-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conj-temp-sub-frame-1-output))))

(define conj-temp
  (def-letter-chunk :name "then"
    :locations (list conj-location
		     (Location (list) conj-temp-sentence-output))
    :parent_space conj-temp-sentence-output
    :abstract_chunk then))

(define conj-temp-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-2-output))
    :parent_space conj-temp-sub-frame-2-output))
(define conj-temp-subject-2-grammar-label
  (def-label :start conj-temp-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conj-temp-sub-frame-2-output))))
(define conj-temp-verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-2-output))
    :parent_space conj-temp-sub-frame-2-output))
(define conj-temp-verb-2-grammar-label
  (def-label :start conj-temp-verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conj-temp-sub-frame-2-output))))
(define conj-temp-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-2-output))
    :parent_space conj-temp-sub-frame-2-output))
(define conj-temp-predicate-2-grammar-label
  (def-label :start conj-temp-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conj-temp-sub-frame-2-output))))
(define conj-temp-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-2-output))
    :left_branch (StructureSet conj-temp-verb-2)
    :right_branch (StructureSet conj-temp-predicate-2)
    :parent_space conj-temp-sub-frame-2-output))
(define conj-temp-vp-2-grammar-label
  (def-label :start conj-temp-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conj-temp-sub-frame-2-output))))
(define conj-temp-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-temp-sentence-output)
		     (Location (list) conj-temp-sub-frame-2-output))
    :left_branch (StructureSet conj-temp-subject-2)
    :right_branch (StructureSet conj-temp-vp-2)
    :parent_space conj-temp-sub-frame-2-output))
(define conj-temp-clause-2-grammar-label
  (def-label :start conj-temp-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conj-temp-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) conj-temp-sentence-output))
    :left_branch (StructureSet conj-temp)
    :right_branch (StructureSet conj-temp-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-temp-sentence-output))
    :left_branch (StructureSet conj-temp-clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start same-concept :end conj-temp-sentence
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end conj-temp-sentence
  :is_bidirectional True :stable_activation 0.5)
