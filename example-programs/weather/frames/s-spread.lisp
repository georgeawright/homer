(define spread-word
  (def-letter-chunk :name "spread" :parent_space grammar-space
    :locations (list vb-location)))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureCollection temperature-space height-space goodness-space)
    :no_of_dimensions 1))

(define ap-sub-frame-input
  (def-contextual-space :name "ap-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define ap-sub-frame
  (def-sub-frame :name "s-spread-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))

(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-spread-location-sub"
    :parent_concept pp-directional-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-spread-location-sub"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define spread-sentence-input
  (def-contextual-space :name "s-spread.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space conceptual-space)))
(define spread-sentence-output
  (def-contextual-space :name "s-spread.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space time-space conceptual-space)))
(define spread-sentence
  (def-frame :name "s-spread" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureCollection ap-sub-frame location-sub-frame time-sub-frame)
    :concepts (StructureCollection)
    :input_space spread-sentence-input
    :output_space spread-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) spread-sentence-input))
    :parent_space spread-sentence-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) spread-sentence-input))
    :parent_space spread-sentence-input))
(define time-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept more-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) spread-sentence-input))
    :parent_space spread-sentence-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) spread-sentence-input))
    :parent_space spread-sentence-input
    :conceptual_space location-space))
(define size-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept more-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) size-space)
		     (TwoPointLocation (list) (list) spread-sentence-input))
    :parent_space spread-sentence-input
    :conceptual_space conceptual-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) spread-sentence-input))
    :parent_space spread-sentence-input
    :conceptual_space conceptual-space))
  
(define sentence-word-1
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :abstract_chunk the))
(define sentence-word-2
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) spread-sentence-output))
    :parent_space ap-sub-frame-output))
(define ap-chunk-grammar-label
  (def-label :start sentence-word-2 :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output))))
(define sentence-word-3
  (def-letter-chunk :name "temperatures"
    :locations (list nn-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-4
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :abstract_chunk will))
(define sentence-word-5
  (def-letter-chunk :name "spread"
    :locations (list vb-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :abstract_chunk spread-word))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) spread-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-6 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-7
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) spread-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-7 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection sentence-word-2)
    :right_branch (StructureCollection sentence-word-3)))
(define np-super-chunk-label
  (def-label :start np-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) spread-sentence-output))))
(define np-super-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection sentence-word-1)
    :right_branch (StructureCollection np-super-chunk)))
(define np-super-super-chunk-label
  (def-label :start np-super-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) spread-sentence-output))))
(define np-super-super-chunk-nsubj-label
  (def-label :start np-super-super-chunk :parent_concept nsubj-concept
    :locations (list np-location
		     (Location (list) spread-sentence-output))))
(define vb-super-chunk
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection sentence-word-4)
    :right_branch (StructureCollection sentence-word-5)))
(define vb-super-chunk-label
  (def-label :start vb-super-chunk :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) spread-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection sentence-word-6)
    :right_branch (StructureCollection sentence-word-7)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) spread-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection vb-super-chunk)
    :right_branch (StructureCollection pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) spread-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) spread-sentence-output))
    :parent_space spread-sentence-output
    :left_branch (StructureCollection np-super-super-chunk)
    :right_branch (StructureCollection vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) spread-sentence-output))))

(def-relation :start label-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start relation-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start nn-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jj-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jjr-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start rp-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end spread-sentence
  :is_bidirectional True :activation 1.0)
