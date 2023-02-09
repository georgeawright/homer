(define conjunction-sub-frame-1-input
  (def-contextual-space :name "conjunction-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conjunction-sub-frame-1-output
  (def-contextual-space :name "conjunction-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conjunction-sub-frame-1
  (def-sub-frame :name "conjunction-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conjunction-sub-frame-1-input
    :output_space conjunction-sub-frame-1-output))
(define conjunction-sub-frame-2-input
  (def-contextual-space :name "conjunction-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conjunction-sub-frame-2-output
  (def-contextual-space :name "conjunction-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conjunction-sub-frame-2
  (def-sub-frame :name "conjunction-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conjunction-sub-frame-2-input
    :output_space conjunction-sub-frame-2-output))

(define conjunction-sentence-input
  (def-contextual-space :name "conjunction.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conjunction-sentence-output
  (def-contextual-space :name "conjunction.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conjunction-sentence
  (def-frame :name "conjunction" :parent_concept conjunction-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet conjunction-sub-frame-1 conjunction-sub-frame-2)
    :concepts (StructureSet)
    :input_space conjunction-sentence-input
    :output_space conjunction-sentence-output))

(define conjunction-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-1-output))
    :parent_space conjunction-sub-frame-1-output))
(define conjunction-subject-1-grammar-label
  (def-label :start conjunction-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conjunction-sub-frame-1-output))))
(define conjunction-verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-1-output))
    :parent_space conjunction-sub-frame-1-output))
(define conjunction-verb-1-grammar-label
  (def-label :start conjunction-verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conjunction-sub-frame-1-output))))
(define conjunction-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-1-output))
    :parent_space conjunction-sub-frame-1-output))
(define conjunction-predicate-1-grammar-label
  (def-label :start conjunction-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conjunction-sub-frame-1-output))))
(define conjunction-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-1-output))
    :left_branch (StructureSet conjunction-verb-1)
    :right_branch (StructureSet conjunction-predicate-1)
    :parent_space conjunction-sub-frame-1-output))
(define conjunction-vp-1-grammar-label
  (def-label :start conjunction-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conjunction-sub-frame-1-output))))
(define conjunction-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-1-output))
    :left_branch (StructureSet conjunction-subject-1)
    :right_branch (StructureSet conjunction-vp-1)
    :parent_space conjunction-sub-frame-1-output))
(define conjunction-clause-1-grammar-label
  (def-label :start conjunction-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conjunction-sub-frame-1-output))))

(define conjunction-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-2-output))
    :parent_space conjunction-sub-frame-2-output))
(define conjunction-subject-2-grammar-label
  (def-label :start conjunction-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conjunction-sub-frame-2-output))))
(define conjunction-verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-2-output))
    :parent_space conjunction-sub-frame-2-output))
(define conjunction-verb-2-grammar-label
  (def-label :start conjunction-verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conjunction-sub-frame-2-output))))
(define conjunction-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-2-output))
    :parent_space conjunction-sub-frame-2-output))
(define conjunction-predicate-2-grammar-label
  (def-label :start conjunction-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conjunction-sub-frame-2-output))))
(define conjunction-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-2-output))
    :left_branch (StructureSet conjunction-verb-2)
    :right_branch (StructureSet conjunction-predicate-2)
    :parent_space conjunction-sub-frame-2-output))
(define conjunction-vp-2-grammar-label
  (def-label :start conjunction-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conjunction-sub-frame-2-output))))
(define conjunction-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conjunction-sentence-output)
		     (Location (list) conjunction-sub-frame-2-output))
    :left_branch (StructureSet conjunction-subject-2)
    :right_branch (StructureSet conjunction-vp-2)
    :parent_space conjunction-sub-frame-2-output))
(define conjunction-clause-2-grammar-label
  (def-label :start conjunction-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conjunction-sub-frame-2-output))))

(def-relation :start same-concept :end conjunction-sentence
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end conjunction-sentence
  :is_bidirectional True :stable_activation 0.5)
