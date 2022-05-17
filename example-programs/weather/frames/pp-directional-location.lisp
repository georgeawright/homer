(define early-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define late-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-ablative-input
  (def-contextual-space :name "ablative-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space)))
(define pp-ablative-output
  (def-contextual-space :name "ablative-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space time-space)))
(define pp-ablative-sub-frame
  (def-sub-frame :name "pp-ablative-sub"
    :parent_concept pp-ablative-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-ablative-input
    :output_space pp-ablative-output))

(define pp-allative-input
  (def-contextual-space :name "allative-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space)))
(define pp-allative-output
  (def-contextual-space :name "allative-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space time-space)))
(define pp-allative-sub-frame
  (def-sub-frame :name "pp-allative-sub"
    :parent_concept pp-allative-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-allative-input
    :output_space pp-allative-output))

(define pp-directional-location-input
  (def-contextual-space :name "pp[from-to-location].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space)))
(define pp-directional-location-output
  (def-contextual-space :name "pp[from-to-location].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space time-space)))
(define pp-directional-location
  (def-frame :name "pp[from-to-location]"
    :parent_concept pp-directional-location-concept
    :parent_frame None
    :sub_frames (StructureCollection pp-ablative-sub-frame pp-allative-sub-frame)
    :concepts (StructureCollection early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-directional-location-input
    :output_space pp-directional-location-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-ablative-input)
			      (Location (list) pp-allative-input)
			      (Location (list) pp-directional-location-input))
    :parent_space pp-ablative-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-ablative-input)
			      (Location (list) pp-allative-input)
			      (Location (list) pp-directional-location-input))
    :parent_space pp-allative-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-ablative-input)
		     (Location (list) pp-allative-input))
    :parent_space pp-ablative-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-ablative-input)
		     (Location (list) pp-allative-input))
    :parent_space pp-allative-input))
(define early-chunk-location-label
  (def-label :start early-chunk :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-input)
		     (Location (list) pp-allative-input))
    :parent_space pp-ablative-input))
(define late-chunk-location-label
  (def-label :start late-chunk :parent_concept late-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-input)
		     (Location (list) pp-allative-input))
    :parent_space pp-allative-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-ablative-input)
		     (TwoPointLocation (list) (list) pp-allative-input)
		     (TwoPointLocation (list) (list) pp-directional-location-input))
    :conceptual_space time-space))

(define pp-1
  (def-letter-chunk :name None
    :locations (list prep-location
		     (Location (list) pp-ablative-output)
		     (Location (list) pp-directional-location-output))
    :parent_space pp-ablative-output))
(define pp-1-grammar-label
  (def-label :start pp-1 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) pp-ablative-output))))
(define pp-2
  (def-letter-chunk :name None
    :locations (list prep-location
		     (Location (list) pp-allative-output)
		     (Location (list) pp-directional-location-output))
    :parent_space pp-allative-output))
(define pp-2-grammar-label
  (def-label :start pp-2 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) pp-allative-output))))

(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-directional-location-output))
    :parent_space pp-directional-location-output
    :left_branch (StructureCollection pp-1)
    :right_branch (StructureCollection pp-2)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) pp-directional-location-output))))

(def-relation :start label-concept :end pp-directional-location
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-directional-location
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-directional-location
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-directional-location
  :is_bidirectional True :activation 1.0)
