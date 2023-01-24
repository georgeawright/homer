(define conj-null-sub-frame-1-input
  (def-contextual-space :name "conj-null-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-null-sub-frame-1-output
  (def-contextual-space :name "conj-null-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-null-sub-frame-1
  (def-sub-frame :name "conj-null-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conj-null-sub-frame-1-input
    :output_space conj-null-sub-frame-1-output))
(define conj-null-sub-frame-2-input
  (def-contextual-space :name "conj-null-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-null-sub-frame-2-output
  (def-contextual-space :name "conj-null-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-null-sub-frame-2
  (def-sub-frame :name "conj-null-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space conj-null-sub-frame-2-input
    :output_space conj-null-sub-frame-2-output))

(define conj-null-sentence-input
  (def-contextual-space :name "conj-null.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define conj-null-sentence-output
  (def-contextual-space :name "conj-null.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define conj-null-sentence
  (def-frame :name "conj-null" :parent_concept sentence-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet conj-null-sub-frame-1 conj-null-sub-frame-2)
    :concepts (StructureSet)
    :input_space conj-null-sentence-input
    :output_space conj-null-sentence-output))

(define conj-null-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-1-output))
    :parent_space conj-null-sub-frame-1-output))
(define conj-null-subject-1-grammar-label
  (def-label :start conj-null-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conj-null-sub-frame-1-output))))
(define conj-null-verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-1-output))
    :parent_space conj-null-sub-frame-1-output))
(define conj-null-verb-1-grammar-label
  (def-label :start conj-null-verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conj-null-sub-frame-1-output))))
(define conj-null-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-1-output))
    :parent_space conj-null-sub-frame-1-output))
(define conj-null-predicate-1-grammar-label
  (def-label :start conj-null-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conj-null-sub-frame-1-output))))
(define conj-null-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-1-output))
    :left_branch (StructureSet conj-null-verb-1)
    :right_branch (StructureSet conj-null-predicate-1)
    :parent_space conj-null-sub-frame-1-output))
(define conj-null-vp-1-grammar-label
  (def-label :start conj-null-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conj-null-sub-frame-1-output))))
(define conj-null-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-1-output))
    :left_branch (StructureSet conj-null-subject-1)
    :right_branch (StructureSet conj-null-vp-1)
    :parent_space conj-null-sub-frame-1-output))
(define conj-null-clause-1-grammar-label
  (def-label :start conj-null-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conj-null-sub-frame-1-output))))

(define conj-null
  (def-letter-chunk :name "and"
    :locations (list conj-location
		     (Location (list) conj-null-sentence-output))
    :parent_space conj-null-sentence-output
    :abstract_chunk and))

(define conj-null-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-2-output))
    :parent_space conj-null-sub-frame-2-output))
(define conj-null-subject-2-grammar-label
  (def-label :start conj-null-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) conj-null-sub-frame-2-output))))
(define conj-null-verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-2-output))
    :parent_space conj-null-sub-frame-2-output))
(define conj-null-verb-2-grammar-label
  (def-label :start conj-null-verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) conj-null-sub-frame-2-output))))
(define conj-null-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-2-output))
    :parent_space conj-null-sub-frame-2-output))
(define conj-null-predicate-2-grammar-label
  (def-label :start conj-null-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) conj-null-sub-frame-2-output))))
(define conj-null-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-2-output))
    :left_branch (StructureSet conj-null-verb-2)
    :right_branch (StructureSet conj-null-predicate-2)
    :parent_space conj-null-sub-frame-2-output))
(define conj-null-vp-2-grammar-label
  (def-label :start conj-null-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) conj-null-sub-frame-2-output))))
(define conj-null-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-null-sentence-output)
		     (Location (list) conj-null-sub-frame-2-output))
    :left_branch (StructureSet conj-null-subject-2)
    :right_branch (StructureSet conj-null-vp-2)
    :parent_space conj-null-sub-frame-2-output))
(define conj-null-clause-2-grammar-label
  (def-label :start conj-null-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) conj-null-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) conj-null-sentence-output))
    :left_branch (StructureSet conj-null)
    :right_branch (StructureSet conj-null-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) conj-null-sentence-output))
    :left_branch (StructureSet conj-null-clause-1)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start same-concept :end conj-null-sentence
  :is_bidirectional True :stable_activation 0.5)
(def-relation :start sentence-concept :end conj-null-sentence
  :is_bidirectional True :stable_activation 0.5)
