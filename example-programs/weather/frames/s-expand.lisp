(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureCollection temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define size-label-concept
  (def-concept :name "" :is_slot True :parent_space size-space
    :locations (list (Location (list (list Nan)) size-space))))
(define size-comparison-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start size-label-concept :end size-comparison-concept
  :parent_concept more-concept :activation 1.0)
(define conceptual-label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))

(define ap-sub-frame-input
  (def-contextual-space :name "ap-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define ap-sub-frame
  (def-sub-frame :name "s-expand-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection conceptual-label-concept)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))

(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-expand-location-sub"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-concept)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-expand-time-sub"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define expand-sentence-input
  (def-contextual-space :name "s-expand.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space conceptual-space)))
(define expand-sentence-output
  (def-contextual-space :name "s-expand.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space time-space
					    size-space conceptual-space)))
(define expand-sentence
  (def-frame :name "s-expand" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureCollection ap-sub-frame location-sub-frame time-sub-frame)
    :concepts (StructureCollection size-label-concept size-comparison-concept
				   conceptual-label-concept)
    :input_space expand-sentence-input
    :output_space expand-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list (list Nan)) size-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) expand-sentence-input))
    :parent_space expand-sentence-input))
(define early-chunk-conceptual-label
  (def-label :start early-chunk :parent_concept conceptual-label-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) ap-sub-frame-input)
		     (Location (list) expand-sentence-input))
    :parent_space ap-sub-frame-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list (list Nan)) size-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) expand-sentence-input))
    :parent_space expand-sentence-input))
(define late-chunk-size-label
  (def-label :start early-chunk :parent_concept size-label-concept
    :locations (list (Location (list (list Nan)) size-space)
		     (Location (list) expand-sentence-input))
    :parent_space expand-sentence-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) time-sub-frame-input)
		     (TwoPointLocation (list) (list) expand-sentence-input))
    :parent_space time-sub-frame-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept not-different-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) expand-sentence-input))
    :parent_space expand-sentence-input
    :conceptual_space location-space))
(define size-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept size-comparison-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) size-space)
		     (TwoPointLocation (list) (list) expand-sentence-input))
    :parent_space expand-sentence-input
    :conceptual_space size-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) expand-sentence-input))
    :parent_space expand-sentence-input
    :conceptual_space conceptual-space))
  
(define sentence-word-1
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :abstract_chunk the))
(define sentence-word-2
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) expand-sentence-output))
    :parent_space ap-sub-frame-output))
(define ap-chunk-grammar-label
  (def-label :start sentence-word-2 :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output))))
(define sentence-word-3
  (def-letter-chunk :name "temperatures"
    :locations (list nn-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) expand-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :abstract_chunk will))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output))
(define size-word-grammar-label
  (def-label :start sentence-word-6 :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) expand-sentence-output))))
(define size-word-meaning-label
  (def-label :start sentence-word-6 :parent_concept size-label-concept
    :locations (list (Location (list (list Nan)) size-space)
		     (Location (list) expand-sentence-output))))
(define sentence-word-7
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) expand-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-7 :parent_concept pp-directional-time-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))
(define sentence-word-8
  (def-letter-chunk :name ""
    :locations (list null-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :abstract_chunk null))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection sentence-word-2)
    :right_branch (StructureCollection sentence-word-3)))
(define np-super-chunk-label
  (def-label :start np-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) expand-sentence-output))))
(define np-super-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection sentence-word-1)
    :right_branch (StructureCollection np-super-chunk)))
(define np-super-super-chunk-label
  (def-label :start np-super-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) expand-sentence-output))))
(define np-super-super-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection np-super-super-chunk)
    :right_branch (StructureCollection sentence-word-4)))
(define np-super-super-super-chunk-label
  (def-label :start np-super-super-super-chunk :parent_concept np-concept
    :locations (list np-location
		     (Location (list) expand-sentence-output))))
(define np-super-super-super-chunk-nsubj-label
  (def-label :start np-super-super-super-chunk :parent_concept nsubj-concept
    :locations (list np-location
		     (Location (list) expand-sentence-output))))
(define v-super-chunk
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection sentence-word-5)
    :right_branch (StructureCollection sentence-word-6)))
(define v-super-chunk-label
  (def-label :start v-super-chunk :parent_concept v-concept
    :locations (list v-location
		     (Location (list) expand-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection sentence-word-7)
    :right_branch (StructureCollection sentence-word-8)))
(define pred-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) expand-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection v-super-chunk)
    :right_branch (StructureCollection pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) expand-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) expand-sentence-output))
    :parent_space expand-sentence-output
    :left_branch (StructureCollection np-super-super-super-chunk)
    :right_branch (StructureCollection vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) expand-sentence-output))))

(def-relation :start pp-inessive-location-concept :end expand-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start pp-directional-time-concept :end expand-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start ap-concept :end expand-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start large-concept :end expand-sentence
  :is_bidirectional True :stable_activation 0.3)
(def-relation :start small-concept :end expand-sentence
  :is_bidirectional True :stable_activation 0.3)

