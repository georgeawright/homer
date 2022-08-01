(define and-sub-frame-1-input
  (def-contextual-space :name "and-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sub-frame-1-output
  (def-contextual-space :name "and-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sub-frame-1
  (def-sub-frame :name "s-and-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space and-sub-frame-1-input
    :output_space and-sub-frame-1-output))
(define and-sub-frame-2-input
  (def-contextual-space :name "and-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sub-frame-2-output
  (def-contextual-space :name "and-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sub-frame-2
  (def-sub-frame :name "s-and-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space and-sub-frame-2-input
    :output_space and-sub-frame-2-output))

(define and-sentence-input
  (def-contextual-space :name "s-and.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sentence-output
  (def-contextual-space :name "s-and.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sentence
  (def-frame :name "s-and" :parent_concept sentence-concept :parent_frame None
    :depth 8
    :sub_frames (StructureCollection and-sub-frame-1 and-sub-frame-2)
    :concepts (StructureCollection)
    :input_space and-sentence-input
    :output_space and-sentence-output))

(define s-and-subject-1
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-subject-1-grammar-label
  (def-label :start s-and-subject-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) and-sub-frame-1-output))))
(define s-and-verb-1
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-verb-1-grammar-label
  (def-label :start s-and-verb-1 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) and-sub-frame-1-output))))
(define s-and-predicate-1
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-predicate-1-grammar-label
  (def-label :start s-and-predicate-1 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) and-sub-frame-1-output))))
(define s-and-vp-1
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :left_branch (StructureCollection s-and-verb-1)
    :right_branch (StructureCollection s-and-predicate-1)
    :parent_space and-sub-frame-1-output))
(define s-and-vp-1-grammar-label
  (def-label :start s-and-vp-1 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) and-sub-frame-1-output))))
(define s-and-clause-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :left_branch (StructureCollection s-and-subject-1)
    :right_branch (StructureCollection s-and-vp-1)
    :parent_space and-sub-frame-1-output))
(define s-and-clause-1-grammar-label
  (def-label :start s-and-clause-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) and-sub-frame-1-output))))

(define s-and
  (def-letter-chunk :name "and"
    :locations (list conj-location
		     (Location (list) and-sentence-output))
    :parent_space and-sentence-output
    :abstract_chunk and))

(define s-and-subject-2
  (def-letter-chunk :name None
    :locations (list nsubj-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-subject-2-grammar-label
  (def-label :start s-and-subject-2 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) and-sub-frame-2-output))))
(define s-and-verb-2
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-verb-2-grammar-label
  (def-label :start s-and-verb-2 :parent_concept v-concept
    :locations (list v-location
		     (Location (list) and-sub-frame-2-output))))
(define s-and-predicate-2
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-predicate-2-grammar-label
  (def-label :start s-and-predicate-2 :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) and-sub-frame-2-output))))
(define s-and-vp-2
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :left_branch (StructureCollection s-and-verb-2)
    :right_branch (StructureCollection s-and-predicate-2)
    :parent_space and-sub-frame-2-output))
(define s-and-vp-2-grammar-label
  (def-label :start s-and-vp-2 :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) and-sub-frame-2-output))))
(define s-and-clause-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :left_branch (StructureCollection s-and-subject-2)
    :right_branch (StructureCollection s-and-vp-2)
    :parent_space and-sub-frame-2-output))
(define s-and-clause-2-grammar-label
  (def-label :start s-and-clause-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) and-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) and-sentence-output))
    :left_branch (StructureCollection s-and)
    :right_branch (StructureCollection s-and-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) and-sentence-output))
    :left_branch (StructureCollection s-and-clause-1)
    :right_branch (StructureCollection conjunction-super-chunk)))

(def-relation :start same-concept :end and-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start conj-concept :end and-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start and :end and-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end and-sentence
  :is_bidirectional True :activation 1.0)
