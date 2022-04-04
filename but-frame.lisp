(define conceptual-space-1-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space-1
  (def-conceptual-space :name "" :parent_concept conceptual-space-1-parent-concept
    :possible_instances (StructureCollection temperature-space)
    :no_of_dimensions 1))
(define but-sub-frame-1-input
  (def-contextual-space :name "but-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sub-frame-1-output
  (def-contextual-space :name "but-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sub-frame-1
  (def-sub-frame :name "s-but-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space but-sub-frame-1-input
    :output_space but-sub-frame-1-output))
(define but-sub-frame-2-input
  (def-contextual-space :name "but-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sub-frame-2-output
  (def-contextual-space :name "but-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sub-frame-2
  (def-sub-frame :name "s-but-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space but-sub-frame-2-input
    :output_space but-sub-frame-2-output))

(define but-sentence-input
  (def-contextual-space :name "s-but.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sentence-output
  (def-contextual-space :name "s-but.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sentence
  (def-frame :name "s-but" :parent_concept sentence-concept :parent_frame None
    :depth 8
    :sub_frames (StructureCollection but-sub-frame-1 but-sub-frame-2)
    :concepts (StructureCollection)
    :input_space but-sentence-input
    :output_space but-sentence-output))

(define input-chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space-1)
			       (Location (list) but-sub-frame-1-input)
			       (Location (list) but-sentence-input))
    :parent_space but-sub-frame-1-input))
(define input-chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space-1)
			       (Location (list) but-sub-frame-2-input)
			       (Location (list) but-sentence-input))
    :parent_space but-sub-frame-2-input))
(def-relation :start input-chunk-1 :end input-chunk-2 :parent_concept different-concept
  :locations (list (Location (list) but-sentence-input)
		   (Location (list (list Nan)) same-different-space)
		   (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space-1))
  :parent_space but-sentence-input)

(define s-but-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-subject-1-grammar-label
  (def-label :start s-but-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) but-sub-frame-1-output))))
(define s-but-verb-1
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-verb-1-grammar-label
  (def-label :start s-but-verb-1 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) but-sub-frame-1-output))))
(define s-but-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-predicate-1-grammar-label
  (def-label :start s-but-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) but-sub-frame-1-output))))
(define s-but-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :left_branch (StructureCollection s-but-verb-1)
    :right_branch (StructureCollection s-but-predicate-1)
    :parent_space but-sub-frame-1-output))
(define s-but-vp-1-grammar-label
  (def-label :start s-but-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) but-sub-frame-1-output))))
(define s-but-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :left_branch (StructureCollection s-but-subject-1)
    :right_branch (StructureCollection s-but-vp-1)
    :parent_space but-sub-frame-1-output))
(define s-but-clause-1-grammar-label
  (def-label :start s-but-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) but-sub-frame-1-output))))

(define s-but
  (def-letter-chunk :name "but"
    :locations (list conj-location
		     (Location (list) but-sentence-output))
    :parent_space but-sentence-output
    :abstract_chunk but))

(define s-but-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-subject-2-grammar-label
  (def-label :start s-but-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) but-sub-frame-2-output))))
(define s-but-verb-2
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-verb-2-grammar-label
  (def-label :start s-but-verb-2 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) but-sub-frame-2-output))))
(define s-but-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-predicate-2-grammar-label
  (def-label :start s-but-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) but-sub-frame-2-output))))
(define s-but-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :left_branch (StructureCollection s-but-verb-2)
    :right_branch (StructureCollection s-but-predicate-2)
    :parent_space but-sub-frame-2-output))
(define s-but-vp-2-grammar-label
  (def-label :start s-but-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) but-sub-frame-2-output))))
(define s-but-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :left_branch (StructureCollection s-but-subject-2)
    :right_branch (StructureCollection s-but-vp-2)
    :parent_space but-sub-frame-2-output))
(define s-but-clause-2-grammar-label
  (def-label :start s-but-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) but-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) but-sentence-output))
    :left_branch (StructureCollection s-but)
    :right_branch (StructureCollection s-but-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) but-sentence-output))
    :left_branch (StructureCollection s-but-clause-1)
    :right_branch (StructureCollection conjunction-super-chunk)))

(def-relation :start different-concept :end but-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start conj-concept :end but-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start but :end but-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end but-sentence
  :is_bidirectional True :activation 1.0)

