(define then-sub-frame-1-input
  (def-contextual-space :name "then-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define then-sub-frame-1-output
  (def-contextual-space :name "then-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define then-sub-frame-1
  (def-sub-frame :name "s-then-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space then-sub-frame-1-input
    :output_space then-sub-frame-1-output))
(define then-sub-frame-2-input
  (def-contextual-space :name "then-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define then-sub-frame-2-output
  (def-contextual-space :name "then-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define then-sub-frame-2
  (def-sub-frame :name "s-then-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space then-sub-frame-2-input
    :output_space then-sub-frame-2-output))

(define then-sentence-input
  (def-contextual-space :name "s-then.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define then-sentence-output
  (def-contextual-space :name "s-then.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define then-sentence
  (def-frame :name "s-then" :parent_concept sentence-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet then-sub-frame-1 then-sub-frame-2)
    :concepts (StructureSet)
    :input_space then-sentence-input
    :output_space then-sentence-output))

(define chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) then-sub-frame-1-input)
			      (Location (list) then-sentence-input))
    :parent_space then-sentence-input))
(define chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) then-sub-frame-1-input)
			      (Location (list) then-sentence-input))
    :parent_space then-sentence-input))
(define chunk-3
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) then-sub-frame-2-input)
			      (Location (list) then-sentence-input))
    :parent_space then-sentence-input))
(define chunk-4
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) then-sub-frame-2-input)
			      (Location (list) then-sentence-input))
    :parent_space then-sentence-input))
(define less-time-relation-1
  (def-relation :start chunk-1 :end chunk-3 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) then-sentence-input))
    :parent_space then-sentence-input
    :conceptual_space time-space))
(define less-time-relation-2
  (def-relation :start chunk-2 :end chunk-4 :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) then-sentence-input))
    :parent_space then-sentence-input
    :conceptual_space time-space))
(define not-more-time-relation
  (def-relation :start chunk-2 :end chunk-3 :parent_concept not-more-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) then-sentence-input))
    :parent_space then-sentence-input
    :conceptual_space time-space))
(setattr then-sentence "early_chunk" chunk-1)
(setattr then-sentence "late_chunk" chunk-4)
(setattr then-sub-frame-1 "early_chunk" chunk-1)
(setattr then-sub-frame-1 "late_chunk" chunk-2)
(setattr then-sub-frame-2 "early_chunk" chunk-3)
(setattr then-sub-frame-2 "late_chunk" chunk-4)

(define s-then-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-1-output))
    :parent_space then-sub-frame-1-output))
(define s-then-subject-1-grammar-label
  (def-label :start s-then-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) then-sub-frame-1-output))))
(define s-then-verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-1-output))
    :parent_space then-sub-frame-1-output))
(define s-then-verb-1-grammar-label
  (def-label :start s-then-verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) then-sub-frame-1-output))))
(define s-then-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-1-output))
    :parent_space then-sub-frame-1-output))
(define s-then-predicate-1-grammar-label
  (def-label :start s-then-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) then-sub-frame-1-output))))
(define s-then-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-1-output))
    :left_branch (StructureSet s-then-verb-1)
    :right_branch (StructureSet s-then-predicate-1)
    :parent_space then-sub-frame-1-output))
(define s-then-vp-1-grammar-label
  (def-label :start s-then-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) then-sub-frame-1-output))))
(define s-then-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-1-output))
    :left_branch (StructureSet s-then-subject-1)
    :right_branch (StructureSet s-then-vp-1)
    :parent_space then-sub-frame-1-output))
(define s-then-clause-1-grammar-label
  (def-label :start s-then-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) then-sub-frame-1-output))))

(define s-then
  (def-letter-chunk :name "then"
    :locations (list conj-location
		     (Location (list) then-sentence-output))
    :parent_space then-sentence-output
    :abstract_chunk then))

(define s-then-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-2-output))
    :parent_space then-sub-frame-2-output))
(define s-then-subject-2-grammar-label
  (def-label :start s-then-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) then-sub-frame-2-output))))
(define s-then-verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-2-output))
    :parent_space then-sub-frame-2-output))
(define s-then-verb-2-grammar-label
  (def-label :start s-then-verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) then-sub-frame-2-output))))
(define s-then-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-2-output))
    :parent_space then-sub-frame-2-output))
(define s-then-predicate-2-grammar-label
  (def-label :start s-then-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) then-sub-frame-2-output))))
(define s-then-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-2-output))
    :left_branch (StructureSet s-then-verb-2)
    :right_branch (StructureSet s-then-predicate-2)
    :parent_space then-sub-frame-2-output))
(define s-then-vp-2-grammar-label
  (def-label :start s-then-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) then-sub-frame-2-output))))
(define s-then-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) then-sentence-output)
		     (Location (list) then-sub-frame-2-output))
    :left_branch (StructureSet s-then-subject-2)
    :right_branch (StructureSet s-then-vp-2)
    :parent_space then-sub-frame-2-output))
(define s-then-clause-2-grammar-label
  (def-label :start s-then-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) then-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) then-sentence-output))
    :left_branch (StructureSet s-then)
    :right_branch (StructureSet s-then-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) then-sentence-output))
    :left_branch (StructureSet s-then-clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start same-concept :end then-sentence
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end then-sentence
  :is_bidirectional True :stable_activation 0.5)
